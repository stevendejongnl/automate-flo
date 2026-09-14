#!/usr/bin/env python3
"""
Reader/writer for LlamaLab Automate .flo flow files.

Binary format (reverse-engineered from Automate 1.53.2 APK, classes
Q3.c/Q3.d/Q3.f/Q3.g/E0/AbstractStatement/Action, decompiled with jadx):

  int32 BE   magic = 0x4c41466c ("LAFl")
  int16 BE   version (observed: 114)
  varint     next statement id (signed zigzag LEB128, 64-bit range)
  uvarint    block count N
  N x OBJECT top-level blocks (see object encoding below)

OBJECT encoding (Q3.d.g / Q3.c.readObject):
  svarint type_id
    type_id == 0        -> null
    type_id < 0          -> back-reference: index = -type_id - 1 into the
                             flat list of previously-fully-written objects
                             (first-seen order), 0-indexed
    type_id > 0 (first time seen) -> append to seen-list, then dispatch to
                             the type's own field writer/reader

varint encoding:
  uvarint: LEB128, 7 bits/byte, low-to-high, continuation bit 0x80
  svarint: zigzag(uvarint) where zigzag_decode(n) = (n>>1) ^ -(n&1)
           and zigzag_encode(n) = (n << 1) ^ (n >> 31)  [(n<<1)^(n>>63) for 64-bit]
  Fixed-width int/long/short/float/double are big-endian, NOT varint.
  Strings (writeUTF) in this format's mode (flag f6201x0, true when
    version>=5) are: uvarint byte-length + modified-UTF-8 bytes (ASCII
    passes through unchanged, so plain ASCII package names etc. are just
    length + raw ascii bytes).

Every block (B2/AbstractStatement subclass) serializes:
  AbstractStatement.S:  svarint statementId (as long/d()), svarint cellX (as
                         int/c()), svarint cellY (as int/c())
  Action.S (adds):      OBJECT onComplete            (next block, or null)
  PackageAction.S (adds): OBJECT packageName          (expression, usually a
                         literal string wrapper, type id 106 "W")
  FlowBeginning.S (adds, after AbstractStatement+Action):
                         UTF title (possibly empty)
                         byte hidden       (only if version>=66)
                         byte parallel
                         OBJECT varPayload           (usually null)
                         OBJECT varFiberUri          (only if version>=43, usually null)

Confirmed type ids (from Q3.g$d registry, cross-checked against decompiled
block classes AND, where noted, against the live Automate 1.53.2 UI running
on an Android-17 emulator):
  1072  FlowBeginning
  1221  AppKill
  1001  ActivityStart ("App start" in the UI -- confirmed by search + opening
        the real edit screen: field order on screen was exactly Package,
        Activity class, Action, Data URI, MIME type, Category, Extras, Flags,
        matching IntentAction.r()/t() byte-for-byte)
  1046  Delay
  1201  CarModeEnabled ("Car mode enabled?" in the UI -- confirmed via live
        search: searching "car"/"auto"/"usb" in the block picker turns up
        NO dedicated Android-Auto/projection/headunit block at all, and no
        such string exists in strings.xml either. CarModeEnabled is
        Automate's only mechanism that reacts to Android Auto connecting,
        since Android Auto puts the phone into standard UiModeManager car
        mode. This is the block ChatGPT's community-flow reference was
        actually describing.)
  106   W (string literal expression wrapper, implements InterfaceC1601v0)
  104   J (double literal expression wrapper -- plain 8-byte BE double, no
        length prefix; used for Delay's "duration" field, e.g. seconds)
  25    java.lang.String (raw String object, distinct from the "W" expr wrapper
        -- used in some other slots, not needed for our target flow)

Field layouts (fully traced from source):

  ActivityStart(id=1001) extends IntentAction extends Action:
    AbstractStatement header (stmt_id, cell_x, cell_y)
    onComplete
    packageName, className, action, uri, mimeType, categories, extras, flags
      (all OBJECT refs, all null except packageName which is a StringExpr)
    activityOptions   (OBJECT ref, null)
    chooser           (OBJECT ref, null)

  Delay(id=1046) extends IntermittentAction extends Action:
    AbstractStatement header (stmt_id, cell_x, cell_y)
    onComplete
    continuity        (OBJECT ref, boxed Integer, null = default)
    wakeup            (OBJECT ref, null = default true)
    duration          (OBJECT ref, a J-typed (double, id 104) literal in seconds)

  CarModeEnabled(id=1201) extends IntermittentDecision extends Decision
  extends AbstractStatement (NOTE: no onComplete -- Decision has two
  branches instead):
    AbstractStatement header (stmt_id, cell_x, cell_y)
    onPositive        (OBJECT ref -- branch when car mode IS enabled)
    onNegative        (OBJECT ref -- branch when NOT enabled)
    continuity        (OBJECT ref, boxed Integer, null = default)

Round-trip validated byte-for-byte against the real sample
/tmp/android-auto-start-stop.flo (FlowBeginning -> AppKill("nl.flitsmeister")).
The extended writer (ActivityStart/Delay/CarModeEnabled) is NOT validated
against a real device-exported sample of those specific block types -- the
UI automation session that would have produced one hit a stylus-overlay/IME
interaction issue on the emulator before the export could be captured.
Confidence per block: ActivityStart and CarModeEnabled field ORDER is
UI-confirmed (visually verified against the real edit screen / block
picker), but the exact byte encoding of ActivityStart/Delay/CarModeEnabled
was never round-tripped against a real exported .flo the way FlowBeginning/
AppKill was. Treat the extended flow as source-derived-and-UI-corroborated,
not device-verified -- test the generated file on a real phone/emulator
import before trusting it blindly.
"""

import struct


MAGIC = 0x4C41466C
VERSION = 114

TYPE_FLOW_BEGINNING = 1072
TYPE_APP_KILL = 1221
TYPE_ACTIVITY_START = 1001
TYPE_DELAY = 1046
TYPE_CAR_MODE_ENABLED = 1201
TYPE_STRING_EXPR = 106  # K3.W: string literal expression wrapper
TYPE_DOUBLE_EXPR = 104  # K3.J: double literal expression wrapper


def _zz_enc(n: int) -> int:
    # generic zigzag encode for arbitrary-width signed ints, mirrors
    # (n << 1) ^ (n >> 31 or 63) but done in unbounded python ints
    return (n << 1) if n >= 0 else (((-n) << 1) - 1)


def _zz_dec(n: int) -> int:
    return (n >> 1) ^ -(n & 1)


class ByteWriter:
    def __init__(self):
        self.buf = bytearray()

    def write_bytes(self, b: bytes):
        self.buf += b

    def write_u8(self, v: int):
        self.buf.append(v & 0xFF)

    def write_i32(self, v: int):
        self.buf += struct.pack(">i", v)

    def write_i16(self, v: int):
        self.buf += struct.pack(">h", v)

    def write_uvarint(self, v: int):
        assert v >= 0
        while v & ~0x7F:
            self.write_u8((v & 0x7F) | 0x80)
            v >>= 7
        self.write_u8(v & 0x7F)

    def write_svarint(self, v: int):
        self.write_uvarint(_zz_enc(v))

    def write_utf(self, s: str):
        b = s.encode("utf-8") if s else b""
        self.write_uvarint(len(b))
        self.write_bytes(b)

    def write_double(self, v: float):
        self.buf += struct.pack(">d", v)


class ByteReader:
    def __init__(self, data: bytes):
        self.data = data
        self.pos = 0

    def read_bytes(self, n: int) -> bytes:
        b = self.data[self.pos:self.pos + n]
        self.pos += n
        return b

    def read_u8(self) -> int:
        b = self.data[self.pos]
        self.pos += 1
        return b

    def read_i32(self) -> int:
        v = struct.unpack(">i", self.data[self.pos:self.pos + 4])[0]
        self.pos += 4
        return v

    def read_i16(self) -> int:
        v = struct.unpack(">h", self.data[self.pos:self.pos + 2])[0]
        self.pos += 2
        return v

    def read_uvarint(self) -> int:
        result = 0
        shift = 0
        while True:
            b = self.read_u8()
            result |= (b & 0x7F) << shift
            if not (b & 0x80):
                return result
            shift += 7

    def read_svarint(self) -> int:
        return _zz_dec(self.read_uvarint())

    def read_utf(self) -> str:
        n = self.read_uvarint()
        return self.read_bytes(n).decode("utf-8")

    def read_double(self) -> float:
        v = struct.unpack(">d", self.data[self.pos:self.pos + 8])[0]
        self.pos += 8
        return v

    def eof(self) -> bool:
        return self.pos >= len(self.data)


# ---- Block model (only the subset needed for FlowBeginning -> ... -> AppKill flows) ----

class Block:
    """Base: every block has a statement id, a (cellX, cellY) grid position,
    and (for Action subclasses) an onComplete pointer to the next block.

    cell_x/cell_y are editor grid coordinates (each unit is one small grid
    square in the flowchart view), not pixels, and there is no auto-layout:
    packing blocks at consecutive integers (0, 1, 2, ...) draws their cards
    overlapping in the editor. Leave a gap of ~6 units between sequential
    blocks (see the flow built in tests/test_format.py) for a readable
    layout."""
    type_id = None

    def __init__(self, stmt_id, cell_x=0, cell_y=0, on_complete=None):
        self.stmt_id = stmt_id
        self.cell_x = cell_x
        self.cell_y = cell_y
        self.on_complete = on_complete


class FlowBeginning(Block):
    type_id = TYPE_FLOW_BEGINNING

    def __init__(self, stmt_id=1, cell_x=0, cell_y=0, on_complete=None,
                 title="", hidden=False, parallel=False):
        super().__init__(stmt_id, cell_x, cell_y, on_complete)
        self.title = title
        self.hidden = hidden
        self.parallel = parallel


class AppKill(Block):
    type_id = TYPE_APP_KILL

    def __init__(self, stmt_id, package_name, cell_x=0, cell_y=0, on_complete=None):
        super().__init__(stmt_id, cell_x, cell_y, on_complete)
        self.package_name = package_name


class ActivityStart(Block):
    """id 1001, UI name "App start". Extends IntentAction extends Action."""
    type_id = TYPE_ACTIVITY_START

    def __init__(self, stmt_id, package_name, cell_x=0, cell_y=0, on_complete=None,
                 class_name=None, action=None, uri=None, mime_type=None,
                 categories=None, extras=None, flags=None,
                 activity_options=None, chooser=None):
        super().__init__(stmt_id, cell_x, cell_y, on_complete)
        self.package_name = package_name
        self.class_name = class_name
        self.action = action
        self.uri = uri
        self.mime_type = mime_type
        self.categories = categories
        self.extras = extras
        self.flags = flags
        self.activity_options = activity_options
        self.chooser = chooser


class Delay(Block):
    """id 1046. Extends IntermittentAction extends Action."""
    type_id = TYPE_DELAY

    def __init__(self, stmt_id, seconds, cell_x=0, cell_y=0, on_complete=None,
                 continuity=None, wakeup=None):
        super().__init__(stmt_id, cell_x, cell_y, on_complete)
        self.seconds = seconds
        self.continuity = continuity
        self.wakeup = wakeup


class CarModeEnabled(Block):
    """id 1201, UI name "Car mode enabled?". Extends IntermittentDecision
    extends Decision extends AbstractStatement directly -- NOT Action, so
    it has onPositive/onNegative instead of onComplete. on_complete is
    unused for this block; use on_positive/on_negative instead."""
    type_id = TYPE_CAR_MODE_ENABLED

    def __init__(self, stmt_id, cell_x=0, cell_y=0,
                 on_positive=None, on_negative=None, continuity=None):
        super().__init__(stmt_id, cell_x, cell_y, on_complete=None)
        self.on_positive = on_positive
        self.on_negative = on_negative
        self.continuity = continuity


class StringExpr:
    """K3.W -- string literal expression wrapper, type id 106."""
    type_id = TYPE_STRING_EXPR

    def __init__(self, value: str):
        self.value = value


class DoubleExpr:
    """K3.J -- double literal expression wrapper, type id 104. Raw 8-byte
    big-endian double, no length prefix."""
    type_id = TYPE_DOUBLE_EXPR

    def __init__(self, value: float):
        self.value = float(value)


# ---- Serialization ----

class FlowWriter:
    def __init__(self, w: ByteWriter):
        self.w = w
        self.seen = {}  # dedup key -> index in seen-list (0-indexed)
        self.next_index = 0

    @staticmethod
    def _dedup_key(obj):
        # Value literals (StringExpr/DoubleExpr) intern by value, since two
        # call sites building the "same" literal (e.g. the same package name
        # passed to two different blocks) should collapse to one back-
        # referenced object, matching real Automate-exported flows. Every
        # other block is a distinct graph node, keyed by identity.
        if isinstance(obj, StringExpr):
            return ("str", obj.value)
        if isinstance(obj, DoubleExpr):
            return ("dbl", obj.value)
        return ("id", id(obj))

    def write_object(self, obj):
        if obj is None:
            self.w.write_svarint(0)
            return
        key = self._dedup_key(obj)
        if key in self.seen:
            idx = self.seen[key]
            self.w.write_svarint(-(idx + 1))
            return
        self.seen[key] = self.next_index
        self.next_index += 1
        self.w.write_svarint(obj.type_id)
        self._write_fields(obj)

    def _write_fields(self, obj):
        if isinstance(obj, StringExpr):
            self.w.write_utf(obj.value)
            return
        if isinstance(obj, DoubleExpr):
            self.w.write_double(obj.value)
            return

        # AbstractStatement fields (every block has these)
        self.w.write_svarint(obj.stmt_id)
        self.w.write_svarint(obj.cell_x)
        self.w.write_svarint(obj.cell_y)

        if isinstance(obj, CarModeEnabled):
            # Decision, NOT Action: onPositive/onNegative instead of onComplete
            self.write_object(obj.on_positive)
            self.write_object(obj.on_negative)
            self.write_object(obj.continuity)
            return

        # Action fields (onComplete) -- everything else in this model is an Action
        self.write_object(obj.on_complete)

        if isinstance(obj, AppKill):
            self.write_object(StringExpr(obj.package_name))
        elif isinstance(obj, ActivityStart):
            self.write_object(StringExpr(obj.package_name))
            self.write_object(obj.class_name)
            self.write_object(obj.action)
            self.write_object(obj.uri)
            self.write_object(obj.mime_type)
            self.write_object(obj.categories)
            self.write_object(obj.extras)
            self.write_object(obj.flags)          # version 114 >= 45
            self.write_object(obj.activity_options)  # version 114 >= 89
            self.write_object(obj.chooser)            # version 114 >= 38
        elif isinstance(obj, Delay):
            self.write_object(obj.continuity)
            self.write_object(obj.wakeup)
            self.write_object(DoubleExpr(obj.seconds))
        elif isinstance(obj, FlowBeginning):
            self.w.write_utf(obj.title or "")
            self.w.write_u8(1 if obj.hidden else 0)   # version 114 >= 66
            self.w.write_u8(1 if obj.parallel else 0)
            self.write_object(None)  # varPayload
            self.write_object(None)  # varFiberUri (version 114 >= 43)
        else:
            raise NotImplementedError(f"No field writer for {type(obj).__name__}")


def write_flow(blocks, next_id):
    """blocks: list of all top-level Block objects (E0.f14766Z order --
    normally just [flow_beginning] since everything else is reachable via
    onComplete chains, matching what a real Automate export does)."""
    w = ByteWriter()
    w.write_i32(MAGIC)
    w.write_i16(VERSION)
    w.write_svarint(next_id)
    w.write_uvarint(len(blocks))
    fw = FlowWriter(w)
    for b in blocks:
        fw.write_object(b)
    return bytes(w.buf)


class FlowReader:
    def __init__(self, r: ByteReader):
        self.r = r
        self.seen = []  # index-ordered list of fully-parsed objects

    def read_object(self):
        type_id = self.r.read_svarint()
        if type_id == 0:
            return None
        if type_id < 0:
            idx = -type_id - 1
            return self.seen[idx]
        if type_id == TYPE_STRING_EXPR:
            obj = StringExpr.__new__(StringExpr)
            self.seen.append(obj)
            obj.value = self.r.read_utf()
            return obj
        if type_id == TYPE_FLOW_BEGINNING:
            obj = FlowBeginning.__new__(FlowBeginning)
            self.seen.append(obj)
            self._read_stmt_header(obj)
            obj.on_complete = self.read_object()
            obj.title = self.r.read_utf()
            obj.hidden = bool(self.r.read_u8())
            obj.parallel = bool(self.r.read_u8())
            self.read_object()  # varPayload, discarded
            self.read_object()  # varFiberUri, discarded
            return obj
        if type_id == TYPE_APP_KILL:
            obj = AppKill.__new__(AppKill)
            self.seen.append(obj)
            self._read_stmt_header(obj)
            obj.on_complete = self.read_object()
            pkg = self.read_object()
            obj.package_name = pkg.value if pkg is not None else None
            return obj
        if type_id == TYPE_DOUBLE_EXPR:
            obj = DoubleExpr.__new__(DoubleExpr)
            self.seen.append(obj)
            obj.value = self.r.read_double()
            return obj
        if type_id == TYPE_ACTIVITY_START:
            obj = ActivityStart.__new__(ActivityStart)
            self.seen.append(obj)
            self._read_stmt_header(obj)
            obj.on_complete = self.read_object()
            pkg = self.read_object()
            obj.package_name = pkg.value if pkg is not None else None
            obj.class_name = self.read_object()
            obj.action = self.read_object()
            obj.uri = self.read_object()
            obj.mime_type = self.read_object()
            obj.categories = self.read_object()
            obj.extras = self.read_object()
            obj.flags = self.read_object()
            obj.activity_options = self.read_object()
            obj.chooser = self.read_object()
            return obj
        if type_id == TYPE_DELAY:
            obj = Delay.__new__(Delay)
            self.seen.append(obj)
            self._read_stmt_header(obj)
            obj.on_complete = self.read_object()
            obj.continuity = self.read_object()
            obj.wakeup = self.read_object()
            dur = self.read_object()
            obj.seconds = dur.value if dur is not None else None
            return obj
        if type_id == TYPE_CAR_MODE_ENABLED:
            obj = CarModeEnabled.__new__(CarModeEnabled)
            self.seen.append(obj)
            self._read_stmt_header(obj)
            obj.on_complete = None
            obj.on_positive = self.read_object()
            obj.on_negative = self.read_object()
            obj.continuity = self.read_object()
            return obj
        raise NotImplementedError(f"Unknown/unhandled type id {type_id} at byte {self.r.pos}")

    def _read_stmt_header(self, obj):
        obj.stmt_id = self.r.read_svarint()
        obj.cell_x = self.r.read_svarint()
        obj.cell_y = self.r.read_svarint()


def parse_flow(data: bytes):
    r = ByteReader(data)
    magic = r.read_i32()
    if magic != MAGIC:
        raise ValueError(f"Bad magic: {hex(magic & 0xFFFFFFFF)}")
    version = r.read_i16()
    next_id = r.read_svarint()
    count = r.read_uvarint()
    fr = FlowReader(r)
    blocks = [fr.read_object() for _ in range(count)]
    if not r.eof():
        raise ValueError(f"Trailing bytes after parse: {data[r.pos:].hex()}")
    return {"version": version, "next_id": next_id, "blocks": blocks}


def describe(blocks):
    lines = []
    for b in blocks:
        if isinstance(b, FlowBeginning):
            lines.append(f"FlowBeginning(id={b.stmt_id}, title={b.title!r})")
        elif isinstance(b, AppKill):
            lines.append(f"AppKill(id={b.stmt_id}, package={b.package_name!r})")
        elif isinstance(b, ActivityStart):
            lines.append(f"ActivityStart(id={b.stmt_id}, package={b.package_name!r})")
        elif isinstance(b, Delay):
            lines.append(f"Delay(id={b.stmt_id}, seconds={b.seconds!r})")
        elif isinstance(b, CarModeEnabled):
            lines.append(f"CarModeEnabled(id={b.stmt_id})")
    return "\n".join(lines)



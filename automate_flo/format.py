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
  1120  ToastShow ("Show toast message")
  1103  NotificationShow ("Show notification")
  1122  SmsSend ("Send SMS")
  1012  VariableAssign ("Assign variable")
  1146  WifiNetworkConnected ("Wifi network connected?")
  1153  BluetoothDeviceConnected ("Bluetooth device connected?")
  1021  BatteryLevel ("Battery level")
  1087  HttpRequest ("HTTP request")
  1058  ExpressionDecision ("Expression")
  1288  Label ("Label")
  1033  ClipboardSet ("Set clipboard")
  1032  ClipboardGet ("Get clipboard")
  1147  WifiEnabled ("Wifi enabled?")
  1149  WifiSetState ("Set wifi state")
  1155  BluetoothEnabled ("Bluetooth enabled?")
  1156  BluetoothSetState ("Set bluetooth state")
  1113  ScreenBrightness ("Screen brightness")
  1114  ScreenBrightnessSet ("Set screen brightness")
  1115  DeviceKeepAwake ("Keep device awake")
  1093  LogAppend ("Append to log")
  1334  AccessibilityButton ("Accessibility button" -- confirmed via live
        search: opening the real edit screen shows no additional input
        fields, consistent with displayId being valid left null/absent)
  106   W (string literal expression wrapper, implements InterfaceC1601v0)
  104   J (double literal expression wrapper -- plain 8-byte BE double, no
        length prefix; used for Delay's "duration" field, e.g. seconds)
  102   I3.l (mutable-variable reference -- plain UTF name, same wire shape
        as the string wrapper but a distinct type used for variable-name
        fields: VariableAssign.variable, and every block's varXxx output
        fields)
  25    java.lang.String (raw String object, distinct from the "W" expr wrapper
        -- used in some other slots, not needed for our target flow)
  1     Boolean (boxed java.lang.Boolean, single 0/1 byte, no length prefix --
        used directly as a boolean-valued expression, e.g.
        SetStateAction.state)

Field layouts (fully traced from source; "OBJECT ref, null" means the field
is legal to omit -- Automate accepted every generated sample below with
these fields absent):

  AccessibilityButton(id=1334) extends Action:
    AbstractStatement header (stmt_id, cell_x, cell_y)
    onComplete
    displayId (OBJECT ref, null)

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

  ToastShow(id=1120) extends IntermittentAction extends Action:
    header, onComplete, continuity, message (StringExpr), duration (OBJECT
    ref, null = default)

  SmsSend(id=1122) extends IntermittentAction extends Action:
    header, onComplete, continuity, phoneNumber, subscriptionId, message,
    multipartLimit, hidden, varMultipartCount (I3.l or null)

  VariableAssign(id=1012) extends Action:
    header, onComplete, value (expression), variable (I3.l, required --
    Automate throws RequiredVariableMissingException at runtime if null,
    though the file still imports fine without it)

  BatteryLevel(id=1021) extends LevelDecision extends IntermittentDecision
  extends Decision (onPositive/onNegative, not onComplete):
    header, onPositive, onNegative, continuity, minLevel, maxLevel,
    varLevel (I3.l or null)

  WifiNetworkConnected(id=1146) extends IntermittentDecision extends
  Decision (onPositive/onNegative):
    header, onPositive, onNegative, continuity, ssid, bssid,
    varConnectedSsid, varConnectedBssid, varConnectedCapabilities,
    varConnectedLinkSpeed, varConnectedFrequency, varConnectedIpAddress
    (all var* fields I3.l or null)

  BluetoothDeviceConnected(id=1153) extends IntermittentDecision extends
  Decision (onPositive/onNegative):
    header, onPositive, onNegative, continuity, deviceAddress, deviceName,
    deviceClass, pairedOnly, varConnectedDeviceAddress,
    varConnectedDeviceName, varConnectedDeviceClass (leaving
    deviceAddress/deviceName both null matches "any device" in the UI --
    no device-picker interaction needed to build a valid flow)

  NotificationShow(id=1103) extends IntermittentDecision extends Decision
  (onPositive = tapped, onNegative = dismissed/timed out, not onComplete):
    header, onPositive, onNegative, continuity, title, message,
    shortCriticalText, pictureUri, personUri, smallIconUri, largeIconUri,
    primaryLayoutXml, bigLayoutXml, headsUpLayoutXml, color, cancellable,
    ongoing, visibility, category, groupKey, channelId, progress, when,
    varKey (I3.l or null), varInterfaceUri (I3.l or null)
    (source has many `if version >= N` gates for older-format migration;
    all resolve to "always write" at version 114, so the field list above
    is exhaustive for files this library produces)

  HttpRequest(id=1087) extends Action:
    header, onComplete, networkInterface, url, method, account, timeout,
    alias, trust, dontRedirect, contentType, bodyPart, bodyPath, headers,
    saveResponse, responsePath, varResponseCode (I3.l or null),
    varResponseBody (I3.l or null), varResponseHeaders (I3.l or null)

  ExpressionDecision(id=1058) extends Decision (onPositive/onNegative):
    header, onPositive, onNegative, continuity, expression (any expression
    object -- pass a StringExpr/DoubleExpr or None; more complex boolean
    expressions built from expr.func.* nodes are out of scope for this
    library's writer, but the reader will parse whatever type id it finds
    since expression objects round-trip generically through write_object/
    read_object)

  Label(id=1288) extends Action:
    header, onComplete, value (OBJECT ref, the label's name/id expression,
    null legal). Goto (id=1287, the block that jumps to a Label) is NOT
    implemented: its field layout is a uvarint count + N object-refs into
    already-written Label nodes, plus a dynamic labelValue expression --
    meaningfully more involved than everything else in this batch and
    skipped for now. Label is still useful standalone as a connectable
    no-op anchor reachable via any other block's onComplete.

  ClipboardSet(id=1033) extends Action:
    header, onComplete, text, htmlText, uri, mimeType, label, sensitive
    (all OBJECT refs, all null legal except at least one of
    text/htmlText/uri needed for the block to do anything at runtime)

  ClipboardGet(id=1032) extends IntermittentAction extends Action:
    header, onComplete, continuity, varContent (I3.l or null)

  WifiEnabled(id=1147) extends IntermittentDecision extends Decision
  (onPositive/onNegative): header, onPositive, onNegative, continuity --
  no fields beyond the Decision base. BluetoothEnabled(id=1155) is
  identical in shape (same base classes, zero extra fields).

  WifiSetState(id=1149) extends SetStateAction extends Action:
    header, onComplete, state (OBJECT ref, boolean expression).
    BluetoothSetState(id=1156) is identical in shape.

  ScreenBrightness(id=1113) extends LevelDecision extends IntermittentDecision
  extends Decision (onPositive/onNegative):
    header, onPositive, onNegative, continuity, minLevel, maxLevel, varLevel,
    scale, auto, varAuto, varAdjustment

  ScreenBrightnessSet(id=1114) extends Action:
    header, onComplete, level, scale, auto, adjustment

  DeviceKeepAwake(id=1115) extends Action:
    header, onComplete, wakeState, wifiState, wakeup

  LogAppend(id=1093) extends Action:
    header, onComplete, message, whenLogging

Every block above -- including the extended set (ActivityStart, Delay,
CarModeEnabled, ToastShow, SmsSend, VariableAssign, BatteryLevel,
WifiNetworkConnected, BluetoothDeviceConnected, NotificationShow,
HttpRequest, ExpressionDecision, Label, ClipboardSet, ClipboardGet,
WifiEnabled, WifiSetState, BluetoothEnabled, BluetoothSetState,
ScreenBrightness, ScreenBrightnessSet, DeviceKeepAwake, LogAppend) -- has a
fixture in tests/fixtures/ that was pushed to a real Automate 1.53.2 install
on an Android-17 emulator via adb and confirmed
accepted (Automate's own "Import ... flow?" dialog, not a rejection); see
tests/test_emulator_import.py. FlowBeginning->AppKill is additionally
byte-exact-verified against an Automate-exported sample built entirely by
hand in the app UI, independent of this library.
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
TYPE_VARIABLE_EXPR = 102  # I3.l: mutable-variable reference (plain UTF name)
TYPE_BOOLEAN_EXPR = 1  # Q3.g$j: boxed java.lang.Boolean, single 0/1 byte, no length prefix
TYPE_TOAST_SHOW = 1120
TYPE_NOTIFICATION_SHOW = 1103
TYPE_SMS_SEND = 1122
TYPE_VARIABLE_ASSIGN = 1012
TYPE_WIFI_NETWORK_CONNECTED = 1146
TYPE_BLUETOOTH_DEVICE_CONNECTED = 1153
TYPE_BATTERY_LEVEL = 1021
TYPE_HTTP_REQUEST = 1087
TYPE_EXPRESSION_DECISION = 1058
TYPE_LABEL = 1288
TYPE_CLIPBOARD_SET = 1033
TYPE_CLIPBOARD_GET = 1032
TYPE_WIFI_ENABLED = 1147
TYPE_WIFI_SET_STATE = 1149
TYPE_BLUETOOTH_ENABLED = 1155
TYPE_BLUETOOTH_SET_STATE = 1156
TYPE_SCREEN_BRIGHTNESS = 1113
TYPE_SCREEN_BRIGHTNESS_SET = 1114
TYPE_DEVICE_KEEP_AWAKE = 1115
TYPE_LOG_APPEND = 1093
TYPE_ACCESSIBILITY_BUTTON = 1334


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

    def write_bool(self, v: bool):
        self.write_u8(1 if v else 0)


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

    def read_bool(self) -> bool:
        return self.read_u8() != 0

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


class ToastShow(Block):
    """id 1120, UI name "Show toast message". Extends IntermittentAction."""
    type_id = TYPE_TOAST_SHOW

    def __init__(self, stmt_id, message, cell_x=0, cell_y=0, on_complete=None,
                 continuity=None, duration=None):
        super().__init__(stmt_id, cell_x, cell_y, on_complete)
        self.continuity = continuity
        self.message = message
        self.duration = duration


class SmsSend(Block):
    """id 1122, UI name "Send SMS". Extends IntermittentAction."""
    type_id = TYPE_SMS_SEND

    def __init__(self, stmt_id, phone_number, message, cell_x=0, cell_y=0,
                 on_complete=None, continuity=None, subscription_id=None,
                 multipart_limit=None, hidden=None, var_multipart_count=None):
        super().__init__(stmt_id, cell_x, cell_y, on_complete)
        self.continuity = continuity
        self.phone_number = phone_number
        self.subscription_id = subscription_id
        self.message = message
        self.multipart_limit = multipart_limit
        self.hidden = hidden
        self.var_multipart_count = var_multipart_count


class VariableAssign(Block):
    """id 1012, UI name "Assign variable". Extends Action."""
    type_id = TYPE_VARIABLE_ASSIGN

    def __init__(self, stmt_id, variable_name, value, cell_x=0, cell_y=0, on_complete=None):
        super().__init__(stmt_id, cell_x, cell_y, on_complete)
        self.variable_name = variable_name
        self.value = value


class BatteryLevel(Block):
    """id 1021, UI name "Battery level". Extends LevelDecision extends
    IntermittentDecision extends Decision -- onPositive/onNegative, not
    onComplete."""
    type_id = TYPE_BATTERY_LEVEL

    def __init__(self, stmt_id, cell_x=0, cell_y=0, on_positive=None,
                 on_negative=None, continuity=None, min_level=None,
                 max_level=None, var_level=None):
        super().__init__(stmt_id, cell_x, cell_y, on_complete=None)
        self.on_positive = on_positive
        self.on_negative = on_negative
        self.continuity = continuity
        self.min_level = min_level
        self.max_level = max_level
        self.var_level = var_level


class WifiNetworkConnected(Block):
    """id 1146, UI name "Wifi network connected?". Extends
    IntermittentDecision extends Decision -- onPositive/onNegative."""
    type_id = TYPE_WIFI_NETWORK_CONNECTED

    def __init__(self, stmt_id, cell_x=0, cell_y=0, on_positive=None,
                 on_negative=None, continuity=None, ssid=None, bssid=None,
                 var_connected_ssid=None, var_connected_bssid=None,
                 var_connected_capabilities=None, var_connected_link_speed=None,
                 var_connected_frequency=None, var_connected_ip_address=None):
        super().__init__(stmt_id, cell_x, cell_y, on_complete=None)
        self.on_positive = on_positive
        self.on_negative = on_negative
        self.continuity = continuity
        self.ssid = ssid
        self.bssid = bssid
        self.var_connected_ssid = var_connected_ssid
        self.var_connected_bssid = var_connected_bssid
        self.var_connected_capabilities = var_connected_capabilities
        self.var_connected_link_speed = var_connected_link_speed
        self.var_connected_frequency = var_connected_frequency
        self.var_connected_ip_address = var_connected_ip_address


class BluetoothDeviceConnected(Block):
    """id 1153, UI name "Bluetooth device connected?". Extends
    IntermittentDecision extends Decision -- onPositive/onNegative."""
    type_id = TYPE_BLUETOOTH_DEVICE_CONNECTED

    def __init__(self, stmt_id, cell_x=0, cell_y=0, on_positive=None,
                 on_negative=None, continuity=None, device_address=None,
                 device_name=None, device_class=None, paired_only=None,
                 var_connected_device_address=None, var_connected_device_name=None,
                 var_connected_device_class=None):
        super().__init__(stmt_id, cell_x, cell_y, on_complete=None)
        self.on_positive = on_positive
        self.on_negative = on_negative
        self.continuity = continuity
        self.device_address = device_address
        self.device_name = device_name
        self.device_class = device_class
        self.paired_only = paired_only
        self.var_connected_device_address = var_connected_device_address
        self.var_connected_device_name = var_connected_device_name
        self.var_connected_device_class = var_connected_device_class


class NotificationShow(Block):
    """id 1103, UI name "Show notification". Extends IntermittentDecision
    extends Decision -- onPositive fires on tap, onNegative on dismiss/
    timeout (mirrors the real block's two exec outputs)."""
    type_id = TYPE_NOTIFICATION_SHOW

    def __init__(self, stmt_id, title, message, cell_x=0, cell_y=0,
                 on_positive=None, on_negative=None, continuity=None,
                 short_critical_text=None, picture_uri=None, person_uri=None,
                 small_icon_uri=None, large_icon_uri=None, primary_layout_xml=None,
                 big_layout_xml=None, heads_up_layout_xml=None, color=None,
                 cancellable=None, ongoing=None, visibility=None, category=None,
                 group_key=None, channel_id=None, progress=None, when=None,
                 var_key=None, var_interface_uri=None):
        super().__init__(stmt_id, cell_x, cell_y, on_complete=None)
        self.on_positive = on_positive
        self.on_negative = on_negative
        self.continuity = continuity
        self.title = title
        self.message = message
        self.short_critical_text = short_critical_text
        self.picture_uri = picture_uri
        self.person_uri = person_uri
        self.small_icon_uri = small_icon_uri
        self.large_icon_uri = large_icon_uri
        self.primary_layout_xml = primary_layout_xml
        self.big_layout_xml = big_layout_xml
        self.heads_up_layout_xml = heads_up_layout_xml
        self.color = color
        self.cancellable = cancellable
        self.ongoing = ongoing
        self.visibility = visibility
        self.category = category
        self.group_key = group_key
        self.channel_id = channel_id
        self.progress = progress
        self.when = when
        self.var_key = var_key
        self.var_interface_uri = var_interface_uri


class HttpRequest(Block):
    """id 1087, UI name "HTTP request". Extends Action."""
    type_id = TYPE_HTTP_REQUEST

    def __init__(self, stmt_id, url, cell_x=0, cell_y=0, on_complete=None,
                 network_interface=None, method=None, account=None,
                 timeout=None, alias=None, trust=None, dont_redirect=None,
                 content_type=None, body_part=None, body_path=None,
                 headers=None, save_response=None, response_path=None,
                 var_response_code=None, var_response_body=None,
                 var_response_headers=None):
        super().__init__(stmt_id, cell_x, cell_y, on_complete)
        self.network_interface = network_interface
        self.url = url
        self.method = method
        self.account = account
        self.timeout = timeout
        self.alias = alias
        self.trust = trust
        self.dont_redirect = dont_redirect
        self.content_type = content_type
        self.body_part = body_part
        self.body_path = body_path
        self.headers = headers
        self.save_response = save_response
        self.response_path = response_path
        self.var_response_code = var_response_code
        self.var_response_body = var_response_body
        self.var_response_headers = var_response_headers


class ExpressionDecision(Block):
    """id 1058, UI name "Expression". Extends Decision DIRECTLY (not
    IntermittentDecision like the rest of this library's Decision-family
    blocks) -- onPositive/onNegative, plus one generic 'expression' field,
    but NO continuity field. Confirmed by source (class declaration is
    `extends Decision`) and empirically: writing a continuity object here
    (matching the other Decision blocks' shape) misaligned every field
    after it and Automate rejected the file outright."""
    type_id = TYPE_EXPRESSION_DECISION

    def __init__(self, stmt_id, expression, cell_x=0, cell_y=0,
                 on_positive=None, on_negative=None):
        super().__init__(stmt_id, cell_x, cell_y, on_complete=None)
        self.on_positive = on_positive
        self.on_negative = on_negative
        self.expression = expression


class Label(Block):
    """id 1288, UI name "Label". Extends Action -- a jump target for Goto;
    this library doesn't implement Goto (its field layout involves a
    counted array of back-references to Label nodes plus a dynamic
    label-value expression -- meaningfully more complex than the rest of
    this batch, not attempted here). Label itself is just an Action with
    one extra 'value' field (the label's name/id expression) and is useful
    on its own as a connectable no-op anchor."""
    type_id = TYPE_LABEL

    def __init__(self, stmt_id, value=None, cell_x=0, cell_y=0, on_complete=None):
        super().__init__(stmt_id, cell_x, cell_y, on_complete)
        self.value = value


class ClipboardSet(Block):
    """id 1033, UI name "Set clipboard". Extends Action."""
    type_id = TYPE_CLIPBOARD_SET

    def __init__(self, stmt_id, text=None, cell_x=0, cell_y=0, on_complete=None,
                 html_text=None, uri=None, mime_type=None, label=None, sensitive=None):
        super().__init__(stmt_id, cell_x, cell_y, on_complete)
        self.text = text
        self.html_text = html_text
        self.uri = uri
        self.mime_type = mime_type
        self.label = label
        self.sensitive = sensitive


class ClipboardGet(Block):
    """id 1032, UI name "Get clipboard". Extends IntermittentAction."""
    type_id = TYPE_CLIPBOARD_GET

    def __init__(self, stmt_id, var_content=None, cell_x=0, cell_y=0,
                 on_complete=None, continuity=None):
        super().__init__(stmt_id, cell_x, cell_y, on_complete)
        self.continuity = continuity
        self.var_content = var_content


class WifiEnabled(Block):
    """id 1147, UI name "Wifi enabled?". Extends IntermittentDecision
    directly -- no extra fields beyond onPositive/onNegative/continuity."""
    type_id = TYPE_WIFI_ENABLED

    def __init__(self, stmt_id, cell_x=0, cell_y=0, on_positive=None,
                 on_negative=None, continuity=None):
        super().__init__(stmt_id, cell_x, cell_y, on_complete=None)
        self.on_positive = on_positive
        self.on_negative = on_negative
        self.continuity = continuity


class WifiSetState(Block):
    """id 1149, UI name "Set wifi state". Extends SetStateAction (Action +
    one 'state' boolean-expression field)."""
    type_id = TYPE_WIFI_SET_STATE

    def __init__(self, stmt_id, state, cell_x=0, cell_y=0, on_complete=None):
        super().__init__(stmt_id, cell_x, cell_y, on_complete)
        self.state = state


class BluetoothEnabled(Block):
    """id 1155, UI name "Bluetooth enabled?". Same shape as WifiEnabled --
    bare IntermittentDecision, no extra fields."""
    type_id = TYPE_BLUETOOTH_ENABLED

    def __init__(self, stmt_id, cell_x=0, cell_y=0, on_positive=None,
                 on_negative=None, continuity=None):
        super().__init__(stmt_id, cell_x, cell_y, on_complete=None)
        self.on_positive = on_positive
        self.on_negative = on_negative
        self.continuity = continuity


class BluetoothSetState(Block):
    """id 1156, UI name "Set bluetooth state". Same shape as WifiSetState."""
    type_id = TYPE_BLUETOOTH_SET_STATE

    def __init__(self, stmt_id, state, cell_x=0, cell_y=0, on_complete=None):
        super().__init__(stmt_id, cell_x, cell_y, on_complete)
        self.state = state


class ScreenBrightness(Block):
    """id 1113, UI name "Screen brightness". Extends LevelDecision (minLevel,
    maxLevel, varLevel) plus scale/auto/varAuto/varAdjustment."""
    type_id = TYPE_SCREEN_BRIGHTNESS

    def __init__(self, stmt_id, cell_x=0, cell_y=0, on_positive=None,
                 on_negative=None, continuity=None, min_level=None,
                 max_level=None, var_level=None, scale=None, auto=None,
                 var_auto=None, var_adjustment=None):
        super().__init__(stmt_id, cell_x, cell_y, on_complete=None)
        self.on_positive = on_positive
        self.on_negative = on_negative
        self.continuity = continuity
        self.min_level = min_level
        self.max_level = max_level
        self.var_level = var_level
        self.scale = scale
        self.auto = auto
        self.var_auto = var_auto
        self.var_adjustment = var_adjustment


class ScreenBrightnessSet(Block):
    """id 1114, UI name "Set screen brightness". Extends Action."""
    type_id = TYPE_SCREEN_BRIGHTNESS_SET

    def __init__(self, stmt_id, level=None, cell_x=0, cell_y=0, on_complete=None,
                 scale=None, auto=None, adjustment=None):
        super().__init__(stmt_id, cell_x, cell_y, on_complete)
        self.level = level
        self.scale = scale
        self.auto = auto
        self.adjustment = adjustment


class DeviceKeepAwake(Block):
    """id 1115, UI name "Keep device awake". Extends Action."""
    type_id = TYPE_DEVICE_KEEP_AWAKE

    def __init__(self, stmt_id, wake_state=None, cell_x=0, cell_y=0,
                 on_complete=None, wifi_state=None, wakeup=None):
        super().__init__(stmt_id, cell_x, cell_y, on_complete)
        self.wake_state = wake_state
        self.wifi_state = wifi_state
        self.wakeup = wakeup


class LogAppend(Block):
    """id 1093, UI name "Append to log". Extends Action."""
    type_id = TYPE_LOG_APPEND

    def __init__(self, stmt_id, message, cell_x=0, cell_y=0, on_complete=None,
                 when_logging=None):
        super().__init__(stmt_id, cell_x, cell_y, on_complete)
        self.message = message
        self.when_logging = when_logging


class AccessibilityButton(Block):
    """id 1334, UI name "Accessibility button". Extends Action."""
    type_id = TYPE_ACCESSIBILITY_BUTTON

    def __init__(self, stmt_id, display_id=None, cell_x=0, cell_y=0, on_complete=None):
        super().__init__(stmt_id, cell_x, cell_y, on_complete)
        self.display_id = display_id


class StringExpr:
    """K3.W -- string literal expression wrapper, type id 106."""
    type_id = TYPE_STRING_EXPR

    def __init__(self, value: str):
        self.value = value


class VariableExpr:
    """I3.l -- mutable-variable reference, type id 102. Plain UTF name, same
    wire shape as StringExpr but a distinct type used specifically for
    variable name fields (e.g. VariableAssign.variable, *.varXxx fields)."""
    type_id = TYPE_VARIABLE_EXPR

    def __init__(self, name: str):
        self.name = name


class DoubleExpr:
    """K3.J -- double literal expression wrapper, type id 104. Raw 8-byte
    big-endian double, no length prefix."""
    type_id = TYPE_DOUBLE_EXPR

    def __init__(self, value: float):
        self.value = float(value)


class BooleanExpr:
    """Q3.g$j -- boxed java.lang.Boolean, type id 1. Single 0/1 byte, no
    length prefix. This is the generic boxed-object wire type (not a
    dedicated boolean-literal *expression* wrapper like StringExpr/
    DoubleExpr are for their types), but Automate accepts a raw boxed
    Boolean directly wherever a boolean-valued expression field is
    expected (e.g. SetStateAction.state, Delay.wakeup)."""
    type_id = TYPE_BOOLEAN_EXPR

    def __init__(self, value: bool):
        self.value = bool(value)


# ---- Serialization ----

class FlowWriter:
    def __init__(self, w: ByteWriter):
        self.w = w
        self.seen = {}  # dedup key -> index in seen-list (0-indexed)
        self.next_index = 0

    @staticmethod
    def _dedup_key(obj):
        # Value literals (StringExpr/DoubleExpr/VariableExpr) intern by
        # value, since two call sites building the "same" literal (e.g. the
        # same package name passed to two different blocks) should collapse
        # to one back-referenced object, matching real Automate-exported
        # flows. Every other block is a distinct graph node, keyed by
        # identity.
        if isinstance(obj, StringExpr):
            return ("str", obj.value)
        if isinstance(obj, DoubleExpr):
            return ("dbl", obj.value)
        if isinstance(obj, VariableExpr):
            return ("var", obj.name)
        if isinstance(obj, BooleanExpr):
            return ("bool", obj.value)
        return ("id", id(obj))

    @staticmethod
    def _wrap_str(value):
        """Optional string-valued field: pass through None/StringExpr/
        VariableExpr as-is, or wrap a plain str as StringExpr -- lets
        callers write Delay("...", seconds=2) style plain values without
        constructing StringExpr by hand for every text field."""
        if value is None or isinstance(value, (StringExpr, VariableExpr)):
            return value
        return StringExpr(value)

    @staticmethod
    def _wrap_bool(value):
        """Optional boolean-*valued* expression field (e.g.
        SetStateAction.state): these are typed InterfaceC1601v0 like every
        other expression field, evaluated at runtime via truthiness
        (I3.h.J: nonzero number or non-empty string is true) -- NOT the raw
        boxed-Boolean wire type (id 1, BooleanExpr in this library), which
        does not implement InterfaceC1601v0 and was confirmed rejected by
        Automate ("Failed to read flow") when tried here. Encode as
        DoubleExpr(1.0/0.0), matching how a real numeric truthy/falsy
        expression is stored. Pass through None/StringExpr/DoubleExpr as-is
        for callers who want a different (still-valid) expression."""
        if value is None or isinstance(value, (StringExpr, DoubleExpr, VariableExpr)):
            return value
        return DoubleExpr(1.0 if value else 0.0)

    @staticmethod
    def _wrap_double(value):
        """Optional numeric field: pass through None/DoubleExpr as-is, or
        wrap a plain Python int/float as DoubleExpr."""
        if value is None or isinstance(value, DoubleExpr):
            return value
        return DoubleExpr(value)

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
        if isinstance(obj, VariableExpr):
            self.w.write_utf(obj.name)
            return
        if isinstance(obj, BooleanExpr):
            self.w.write_bool(obj.value)
            return

        # AbstractStatement fields (every block has these)
        self.w.write_svarint(obj.stmt_id)
        self.w.write_svarint(obj.cell_x)
        self.w.write_svarint(obj.cell_y)

        if isinstance(obj, ExpressionDecision):
            # Decision directly (NOT IntermittentDecision) -- no continuity
            # field, unlike every other Decision-family block below.
            self.write_object(obj.on_positive)
            self.write_object(obj.on_negative)
            self.write_object(obj.expression)
            return

        if isinstance(obj, (CarModeEnabled, BatteryLevel, WifiNetworkConnected,
                             BluetoothDeviceConnected, NotificationShow,
                             WifiEnabled, BluetoothEnabled,
                             ScreenBrightness)):
            # IntermittentDecision, NOT Action: onPositive/onNegative instead
            # of onComplete, plus continuity.
            self.write_object(obj.on_positive)
            self.write_object(obj.on_negative)
            self.write_object(obj.continuity)

            if isinstance(obj, (WifiEnabled, BluetoothEnabled)):
                pass  # no extra fields
            elif isinstance(obj, ScreenBrightness):
                self.write_object(obj.min_level)
                self.write_object(obj.max_level)
                self.write_object(obj.var_level)
                self.write_object(obj.scale)
                self.write_object(obj.auto)
                self.write_object(obj.var_auto)
                self.write_object(obj.var_adjustment)
            elif isinstance(obj, BatteryLevel):
                self.write_object(obj.min_level)
                self.write_object(obj.max_level)
                self.write_object(obj.var_level)
            elif isinstance(obj, WifiNetworkConnected):
                self.write_object(self._wrap_str(obj.ssid))
                self.write_object(self._wrap_str(obj.bssid))
                self.write_object(obj.var_connected_ssid)
                self.write_object(obj.var_connected_bssid)
                self.write_object(obj.var_connected_capabilities)
                self.write_object(obj.var_connected_link_speed)
                self.write_object(obj.var_connected_frequency)
                self.write_object(obj.var_connected_ip_address)
            elif isinstance(obj, BluetoothDeviceConnected):
                self.write_object(self._wrap_str(obj.device_address))
                self.write_object(self._wrap_str(obj.device_name))
                self.write_object(obj.device_class)
                self.write_object(obj.paired_only)
                self.write_object(obj.var_connected_device_address)
                self.write_object(obj.var_connected_device_name)
                self.write_object(obj.var_connected_device_class)
            elif isinstance(obj, NotificationShow):
                self.write_object(self._wrap_str(obj.title))
                self.write_object(self._wrap_str(obj.message))
                self.write_object(obj.short_critical_text)
                self.write_object(obj.picture_uri)
                self.write_object(obj.person_uri)
                self.write_object(obj.small_icon_uri)
                self.write_object(obj.large_icon_uri)
                self.write_object(obj.primary_layout_xml)
                self.write_object(obj.big_layout_xml)
                self.write_object(obj.heads_up_layout_xml)
                self.write_object(obj.color)
                self.write_object(obj.cancellable)
                self.write_object(obj.ongoing)
                self.write_object(obj.visibility)
                self.write_object(obj.category)
                self.write_object(obj.group_key)
                self.write_object(obj.channel_id)
                self.write_object(obj.progress)
                self.write_object(obj.when)
                self.write_object(obj.var_key)
                self.write_object(obj.var_interface_uri)
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
        elif isinstance(obj, ToastShow):
            self.write_object(obj.continuity)
            self.write_object(self._wrap_str(obj.message))
            self.write_object(obj.duration)
        elif isinstance(obj, SmsSend):
            self.write_object(obj.continuity)
            self.write_object(self._wrap_str(obj.phone_number))
            self.write_object(obj.subscription_id)     # version 114 >= 45
            self.write_object(self._wrap_str(obj.message))
            self.write_object(obj.multipart_limit)
            self.write_object(obj.hidden)
            self.write_object(obj.var_multipart_count)  # version 114 >= 97
        elif isinstance(obj, VariableAssign):
            self.write_object(self._wrap_str(obj.value))
            self.write_object(VariableExpr(obj.variable_name))
        elif isinstance(obj, HttpRequest):
            self.write_object(obj.network_interface)   # version 114 >= 74
            self.write_object(self._wrap_str(obj.url))
            self.write_object(self._wrap_str(obj.method))
            self.write_object(obj.account)
            self.write_object(obj.timeout)              # version 114 >= 82
            self.write_object(self._wrap_str(obj.alias))  # version 114 >= 109
            self.write_object(obj.trust)                 # version 114 >= 45
            self.write_object(obj.dont_redirect)          # version 114 >= 47
            self.write_object(self._wrap_str(obj.content_type))
            self.write_object(obj.body_part)
            self.write_object(obj.body_path)              # version 114 >= 82
            self.write_object(obj.headers)                # version 114 >= 35
            self.write_object(obj.save_response)
            self.write_object(obj.response_path)
            self.write_object(obj.var_response_code)
            self.write_object(obj.var_response_body)
            self.write_object(obj.var_response_headers)   # version 114 >= 35
        elif isinstance(obj, Label):
            self.write_object(obj.value)
        elif isinstance(obj, ClipboardSet):
            self.write_object(self._wrap_str(obj.text))
            self.write_object(obj.html_text)
            self.write_object(obj.uri)
            self.write_object(obj.mime_type)
            self.write_object(obj.label)
            self.write_object(obj.sensitive)
        elif isinstance(obj, ClipboardGet):
            self.write_object(obj.continuity)
            self.write_object(obj.var_content)
        elif isinstance(obj, (WifiSetState, BluetoothSetState)):
            self.write_object(self._wrap_bool(obj.state))
        elif isinstance(obj, ScreenBrightnessSet):
            self.write_object(self._wrap_double(obj.level))
            self.write_object(obj.scale)
            self.write_object(obj.auto)
            self.write_object(obj.adjustment)
        elif isinstance(obj, DeviceKeepAwake):
            self.write_object(self._wrap_str(obj.wake_state))
            self.write_object(obj.wifi_state)
            self.write_object(obj.wakeup)
        elif isinstance(obj, LogAppend):
            self.write_object(self._wrap_str(obj.message))
            self.write_object(obj.when_logging)
        elif isinstance(obj, AccessibilityButton):
            self.write_object(obj.display_id)
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
        if type_id == TYPE_VARIABLE_EXPR:
            obj = VariableExpr.__new__(VariableExpr)
            self.seen.append(obj)
            obj.name = self.r.read_utf()
            return obj
        if type_id == TYPE_BOOLEAN_EXPR:
            obj = BooleanExpr.__new__(BooleanExpr)
            self.seen.append(obj)
            obj.value = self.r.read_bool()
            return obj
        if type_id == TYPE_TOAST_SHOW:
            obj = ToastShow.__new__(ToastShow)
            self.seen.append(obj)
            self._read_stmt_header(obj)
            obj.on_complete = self.read_object()
            obj.continuity = self.read_object()
            obj.message = self.read_object()
            obj.duration = self.read_object()
            return obj
        if type_id == TYPE_SMS_SEND:
            obj = SmsSend.__new__(SmsSend)
            self.seen.append(obj)
            self._read_stmt_header(obj)
            obj.on_complete = self.read_object()
            obj.continuity = self.read_object()
            obj.phone_number = self.read_object()
            obj.subscription_id = self.read_object()
            obj.message = self.read_object()
            obj.multipart_limit = self.read_object()
            obj.hidden = self.read_object()
            obj.var_multipart_count = self.read_object()
            return obj
        if type_id == TYPE_VARIABLE_ASSIGN:
            obj = VariableAssign.__new__(VariableAssign)
            self.seen.append(obj)
            self._read_stmt_header(obj)
            obj.on_complete = self.read_object()
            obj.value = self.read_object()
            var = self.read_object()
            obj.variable_name = var.name if var is not None else None
            return obj
        if type_id == TYPE_BATTERY_LEVEL:
            obj = BatteryLevel.__new__(BatteryLevel)
            self.seen.append(obj)
            self._read_stmt_header(obj)
            obj.on_complete = None
            obj.on_positive = self.read_object()
            obj.on_negative = self.read_object()
            obj.continuity = self.read_object()
            obj.min_level = self.read_object()
            obj.max_level = self.read_object()
            obj.var_level = self.read_object()
            return obj
        if type_id == TYPE_WIFI_NETWORK_CONNECTED:
            obj = WifiNetworkConnected.__new__(WifiNetworkConnected)
            self.seen.append(obj)
            self._read_stmt_header(obj)
            obj.on_complete = None
            obj.on_positive = self.read_object()
            obj.on_negative = self.read_object()
            obj.continuity = self.read_object()
            obj.ssid = self.read_object()
            obj.bssid = self.read_object()
            obj.var_connected_ssid = self.read_object()
            obj.var_connected_bssid = self.read_object()
            obj.var_connected_capabilities = self.read_object()
            obj.var_connected_link_speed = self.read_object()
            obj.var_connected_frequency = self.read_object()
            obj.var_connected_ip_address = self.read_object()
            return obj
        if type_id == TYPE_BLUETOOTH_DEVICE_CONNECTED:
            obj = BluetoothDeviceConnected.__new__(BluetoothDeviceConnected)
            self.seen.append(obj)
            self._read_stmt_header(obj)
            obj.on_complete = None
            obj.on_positive = self.read_object()
            obj.on_negative = self.read_object()
            obj.continuity = self.read_object()
            obj.device_address = self.read_object()
            obj.device_name = self.read_object()
            obj.device_class = self.read_object()
            obj.paired_only = self.read_object()
            obj.var_connected_device_address = self.read_object()
            obj.var_connected_device_name = self.read_object()
            obj.var_connected_device_class = self.read_object()
            return obj
        if type_id == TYPE_NOTIFICATION_SHOW:
            obj = NotificationShow.__new__(NotificationShow)
            self.seen.append(obj)
            self._read_stmt_header(obj)
            obj.on_complete = None
            obj.on_positive = self.read_object()
            obj.on_negative = self.read_object()
            obj.continuity = self.read_object()
            obj.title = self.read_object()
            obj.message = self.read_object()
            obj.short_critical_text = self.read_object()
            obj.picture_uri = self.read_object()
            obj.person_uri = self.read_object()
            obj.small_icon_uri = self.read_object()
            obj.large_icon_uri = self.read_object()
            obj.primary_layout_xml = self.read_object()
            obj.big_layout_xml = self.read_object()
            obj.heads_up_layout_xml = self.read_object()
            obj.color = self.read_object()
            obj.cancellable = self.read_object()
            obj.ongoing = self.read_object()
            obj.visibility = self.read_object()
            obj.category = self.read_object()
            obj.group_key = self.read_object()
            obj.channel_id = self.read_object()
            obj.progress = self.read_object()
            obj.when = self.read_object()
            obj.var_key = self.read_object()
            obj.var_interface_uri = self.read_object()
            return obj
        if type_id == TYPE_HTTP_REQUEST:
            obj = HttpRequest.__new__(HttpRequest)
            self.seen.append(obj)
            self._read_stmt_header(obj)
            obj.on_complete = self.read_object()
            obj.network_interface = self.read_object()
            obj.url = self.read_object()
            obj.method = self.read_object()
            obj.account = self.read_object()
            obj.timeout = self.read_object()
            obj.alias = self.read_object()
            obj.trust = self.read_object()
            obj.dont_redirect = self.read_object()
            obj.content_type = self.read_object()
            obj.body_part = self.read_object()
            obj.body_path = self.read_object()
            obj.headers = self.read_object()
            obj.save_response = self.read_object()
            obj.response_path = self.read_object()
            obj.var_response_code = self.read_object()
            obj.var_response_body = self.read_object()
            obj.var_response_headers = self.read_object()
            return obj
        if type_id == TYPE_EXPRESSION_DECISION:
            obj = ExpressionDecision.__new__(ExpressionDecision)
            self.seen.append(obj)
            self._read_stmt_header(obj)
            obj.on_complete = None
            obj.on_positive = self.read_object()
            obj.on_negative = self.read_object()
            obj.continuity = None  # extends Decision directly, no continuity field
            obj.expression = self.read_object()
            return obj
        if type_id == TYPE_LABEL:
            obj = Label.__new__(Label)
            self.seen.append(obj)
            self._read_stmt_header(obj)
            obj.on_complete = self.read_object()
            obj.value = self.read_object()
            return obj
        if type_id == TYPE_CLIPBOARD_SET:
            obj = ClipboardSet.__new__(ClipboardSet)
            self.seen.append(obj)
            self._read_stmt_header(obj)
            obj.on_complete = self.read_object()
            obj.text = self.read_object()
            obj.html_text = self.read_object()
            obj.uri = self.read_object()
            obj.mime_type = self.read_object()
            obj.label = self.read_object()
            obj.sensitive = self.read_object()
            return obj
        if type_id == TYPE_CLIPBOARD_GET:
            obj = ClipboardGet.__new__(ClipboardGet)
            self.seen.append(obj)
            self._read_stmt_header(obj)
            obj.on_complete = self.read_object()
            obj.continuity = self.read_object()
            obj.var_content = self.read_object()
            return obj
        if type_id == TYPE_WIFI_ENABLED:
            obj = WifiEnabled.__new__(WifiEnabled)
            self.seen.append(obj)
            self._read_stmt_header(obj)
            obj.on_complete = None
            obj.on_positive = self.read_object()
            obj.on_negative = self.read_object()
            obj.continuity = self.read_object()
            return obj
        if type_id == TYPE_WIFI_SET_STATE:
            obj = WifiSetState.__new__(WifiSetState)
            self.seen.append(obj)
            self._read_stmt_header(obj)
            obj.on_complete = self.read_object()
            obj.state = self.read_object()
            return obj
        if type_id == TYPE_BLUETOOTH_ENABLED:
            obj = BluetoothEnabled.__new__(BluetoothEnabled)
            self.seen.append(obj)
            self._read_stmt_header(obj)
            obj.on_complete = None
            obj.on_positive = self.read_object()
            obj.on_negative = self.read_object()
            obj.continuity = self.read_object()
            return obj
        if type_id == TYPE_BLUETOOTH_SET_STATE:
            obj = BluetoothSetState.__new__(BluetoothSetState)
            self.seen.append(obj)
            self._read_stmt_header(obj)
            obj.on_complete = self.read_object()
            obj.state = self.read_object()
            return obj
        if type_id == TYPE_SCREEN_BRIGHTNESS:
            obj = ScreenBrightness.__new__(ScreenBrightness)
            self.seen.append(obj)
            self._read_stmt_header(obj)
            obj.on_complete = None
            obj.on_positive = self.read_object()
            obj.on_negative = self.read_object()
            obj.continuity = self.read_object()
            obj.min_level = self.read_object()
            obj.max_level = self.read_object()
            obj.var_level = self.read_object()
            obj.scale = self.read_object()
            obj.auto = self.read_object()
            obj.var_auto = self.read_object()
            obj.var_adjustment = self.read_object()
            return obj
        if type_id == TYPE_SCREEN_BRIGHTNESS_SET:
            obj = ScreenBrightnessSet.__new__(ScreenBrightnessSet)
            self.seen.append(obj)
            self._read_stmt_header(obj)
            obj.on_complete = self.read_object()
            obj.level = self.read_object()
            obj.scale = self.read_object()
            obj.auto = self.read_object()
            obj.adjustment = self.read_object()
            return obj
        if type_id == TYPE_DEVICE_KEEP_AWAKE:
            obj = DeviceKeepAwake.__new__(DeviceKeepAwake)
            self.seen.append(obj)
            self._read_stmt_header(obj)
            obj.on_complete = self.read_object()
            obj.wake_state = self.read_object()
            obj.wifi_state = self.read_object()
            obj.wakeup = self.read_object()
            return obj
        if type_id == TYPE_LOG_APPEND:
            obj = LogAppend.__new__(LogAppend)
            self.seen.append(obj)
            self._read_stmt_header(obj)
            obj.on_complete = self.read_object()
            obj.message = self.read_object()
            obj.when_logging = self.read_object()
            return obj
        if type_id == TYPE_ACCESSIBILITY_BUTTON:
            obj = AccessibilityButton.__new__(AccessibilityButton)
            self.seen.append(obj)
            self._read_stmt_header(obj)
            obj.on_complete = self.read_object()
            obj.display_id = self.read_object()
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
        elif isinstance(b, ToastShow):
            lines.append(f"ToastShow(id={b.stmt_id})")
        elif isinstance(b, SmsSend):
            lines.append(f"SmsSend(id={b.stmt_id})")
        elif isinstance(b, VariableAssign):
            lines.append(f"VariableAssign(id={b.stmt_id}, variable={b.variable_name!r})")
        elif isinstance(b, BatteryLevel):
            lines.append(f"BatteryLevel(id={b.stmt_id})")
        elif isinstance(b, WifiNetworkConnected):
            lines.append(f"WifiNetworkConnected(id={b.stmt_id})")
        elif isinstance(b, BluetoothDeviceConnected):
            lines.append(f"BluetoothDeviceConnected(id={b.stmt_id})")
        elif isinstance(b, NotificationShow):
            lines.append(f"NotificationShow(id={b.stmt_id})")
        elif isinstance(b, HttpRequest):
            lines.append(f"HttpRequest(id={b.stmt_id})")
        elif isinstance(b, ExpressionDecision):
            lines.append(f"ExpressionDecision(id={b.stmt_id})")
        elif isinstance(b, Label):
            lines.append(f"Label(id={b.stmt_id})")
        elif isinstance(b, ClipboardSet):
            lines.append(f"ClipboardSet(id={b.stmt_id})")
        elif isinstance(b, ClipboardGet):
            lines.append(f"ClipboardGet(id={b.stmt_id})")
        elif isinstance(b, WifiEnabled):
            lines.append(f"WifiEnabled(id={b.stmt_id})")
        elif isinstance(b, WifiSetState):
            lines.append(f"WifiSetState(id={b.stmt_id})")
        elif isinstance(b, BluetoothEnabled):
            lines.append(f"BluetoothEnabled(id={b.stmt_id})")
        elif isinstance(b, BluetoothSetState):
            lines.append(f"BluetoothSetState(id={b.stmt_id})")
        elif isinstance(b, ScreenBrightness):
            lines.append(f"ScreenBrightness(id={b.stmt_id})")
        elif isinstance(b, ScreenBrightnessSet):
            lines.append(f"ScreenBrightnessSet(id={b.stmt_id})")
        elif isinstance(b, DeviceKeepAwake):
            lines.append(f"DeviceKeepAwake(id={b.stmt_id})")
        elif isinstance(b, LogAppend):
            lines.append(f"LogAppend(id={b.stmt_id})")
        elif isinstance(b, AccessibilityButton):
            lines.append(f"AccessibilityButton(id={b.stmt_id})")
    return "\n".join(lines)



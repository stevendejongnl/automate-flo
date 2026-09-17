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

This module (automate_flo/format.py) holds only the wire-format engine:
the low-level byte reader/writer, MAGIC/VERSION, and FlowWriter/FlowReader
-- generic envelope/dispatch logic that applies to every block alike.
Dispatch is registry-based: FlowReader looks up the class for a type_id
in REGISTRY (built below from automate_flo.blocks.ALL_BLOCKS plus the
four expression wrapper types), then calls that class's own
write_fields/read_fields methods (polymorphism, not a big isinstance
chain). See automate_flo/base.py for the shared class hierarchy (Block /
Action / Decision / IntermittentAction / IntermittentDecision /
LevelDecision) and automate_flo/blocks/ for each concrete block -- that's
where to add a new block type; this file should rarely need touching.

To add a new block: create automate_flo/blocks/<snake_case_name>.py
following an existing block of the same category (Action/Decision/
IntermittentAction/IntermittentDecision/LevelDecision) as a template,
add its import + entry to ALL_BLOCKS in automate_flo/blocks/__init__.py,
and add its name to the import lists in automate_flo/__init__.py. Then
follow the methodology in the wiki's Reverse-Engineering-Notes.md page
(source read -> live UI cross-check -> code -> real-device import
verify -> fixture + tests -> docs sync).

Confirmed type ids (index; see each block's own file docstring in
automate_flo/blocks/ for full field-layout detail, UI name, and
reverse-engineering notes):
  1072  FlowBeginning        automate_flo/blocks/flow_beginning.py
  1221  AppKill              automate_flo/blocks/app_kill.py
  1001  ActivityStart        automate_flo/blocks/activity_start.py
  1046  Delay                automate_flo/blocks/delay.py
  1201  CarModeEnabled       automate_flo/blocks/car_mode_enabled.py
  1120  ToastShow            automate_flo/blocks/toast_show.py
  1103  NotificationShow     automate_flo/blocks/notification_show.py
  1122  SmsSend              automate_flo/blocks/sms_send.py
  1012  VariableAssign       automate_flo/blocks/variable_assign.py
  1146  WifiNetworkConnected automate_flo/blocks/wifi_network_connected.py
  1153  BluetoothDeviceConnected automate_flo/blocks/bluetooth_device_connected.py
  1021  BatteryLevel         automate_flo/blocks/battery_level.py
  1087  HttpRequest          automate_flo/blocks/http_request.py
  1058  ExpressionDecision   automate_flo/blocks/expression_decision.py
  1288  Label                automate_flo/blocks/label.py
  1033  ClipboardSet         automate_flo/blocks/clipboard_set.py
  1032  ClipboardGet         automate_flo/blocks/clipboard_get.py
  1147  WifiEnabled          automate_flo/blocks/wifi_enabled.py
  1149  WifiSetState         automate_flo/blocks/wifi_set_state.py
  1155  BluetoothEnabled     automate_flo/blocks/bluetooth_enabled.py
  1156  BluetoothSetState    automate_flo/blocks/bluetooth_set_state.py
  1113  ScreenBrightness     automate_flo/blocks/screen_brightness.py
  1114  ScreenBrightnessSet  automate_flo/blocks/screen_brightness_set.py
  1115  DeviceKeepAwake      automate_flo/blocks/device_keep_awake.py
  1093  LogAppend            automate_flo/blocks/log_append.py
  1334  AccessibilityButton  automate_flo/blocks/accessibility_button.py
  1236  AccountGenericAdd    automate_flo/blocks/account_generic_add.py
  1000  AccountPick          automate_flo/blocks/account_pick.py
  1019  AccountSyncEnabled   automate_flo/blocks/account_sync_enabled.py
  1230  AccountSyncRequest   automate_flo/blocks/account_sync_request.py
  1020  AccountSyncSetState  automate_flo/blocks/account_sync_set_state.py
  1002  ActivityStartResult  automate_flo/blocks/activity_start_result.py
  1346  ActivityStartVoice   automate_flo/blocks/activity_start_voice.py
  1342  AdbShellCommand      automate_flo/blocks/adb_shell_command.py
  1380  AdbProtocolSet       automate_flo/blocks/adb_protocol_set.py
  1003  AirplaneModeEnabled  automate_flo/blocks/airplane_mode_enabled.py
  1165  AirplaneModeSetState automate_flo/blocks/airplane_mode_set_state.py
  1210  Alarm                automate_flo/blocks/alarm.py
  1182  AlarmAdd             automate_flo/blocks/alarm_add.py
  1336  AlternativeLaunch    automate_flo/blocks/alternative_launch.py
  1004  AmbientLight         automate_flo/blocks/ambient_light.py
  1005  AmbientTemperature   automate_flo/blocks/ambient_temperature.py
  1244  AndroidVersion       automate_flo/blocks/android_version.py
  1235  AppClearCache        automate_flo/blocks/app_clear_cache.py
  1006  AppForeground        automate_flo/blocks/app_foreground.py
  1007  AppInstalled         automate_flo/blocks/app_installed.py
  1008  AppKillBackground    automate_flo/blocks/app_kill_background.py
  1305  AppList              automate_flo/blocks/app_list.py
  1242  AppNotificationsEnabled     automate_flo/blocks/app_notifications_enabled.py
  1306  AppNotificationsPriorityGet automate_flo/blocks/app_notifications_priority_get.py
  1307  AppNotificationsPrioritySet automate_flo/blocks/app_notifications_priority_set.py
  1243  AppNotificationsSetState    automate_flo/blocks/app_notifications_set_state.py
  1308  AppNotificationsVisibilityGet automate_flo/blocks/app_notifications_visibility_get.py
  1309  AppNotificationsVisibilitySet automate_flo/blocks/app_notifications_visibility_set.py
  1250  AppOpMode            automate_flo/blocks/app_op_mode.py
  1251  AppOpModeSet         automate_flo/blocks/app_op_mode_set.py
  1237  AppPick              automate_flo/blocks/app_pick.py
  1310  AppUsage             automate_flo/blocks/app_usage.py
  1421  AppWidgetConfigure   automate_flo/blocks/app_widget_configure.py
  1009  ArrayAdd             automate_flo/blocks/array_add.py
  1010  ArrayRemove          automate_flo/blocks/array_remove.py
  1011  ArraySet             automate_flo/blocks/array_set.py
  1013  AssistRequest        automate_flo/blocks/assist_request.py
  1014  AtmosphericPressure  automate_flo/blocks/atmospheric_pressure.py
  1253  AtomicAdd            automate_flo/blocks/atomic_add.py
  1254  AtomicClearAll       automate_flo/blocks/atomic_clear_all.py
  1255  AtomicCompareAndStore automate_flo/blocks/atomic_compare_and_store.py
  1256  AtomicLoad           automate_flo/blocks/atomic_load.py
  1257  AtomicStore          automate_flo/blocks/atomic_store.py
  1205  AttentionLight       automate_flo/blocks/attention_light.py
  1329  AudioDeviceConnected automate_flo/blocks/audio_device_connected.py
  1349  AudioDeviceRecording automate_flo/blocks/audio_device_recording.py
  1152  AudioPlayerControl   automate_flo/blocks/audio_player_control.py
  1015  AudioRecordStart     automate_flo/blocks/audio_record_start.py
  1016  AudioRecordStop      automate_flo/blocks/audio_record_stop.py
  1317  AudioStreamMuted     automate_flo/blocks/audio_stream_muted.py
  1318  AudioStreamSetMute   automate_flo/blocks/audio_stream_set_mute.py
  1017  AudioVolume          automate_flo/blocks/audio_volume.py
  1018  AudioVolumeSet       automate_flo/blocks/audio_volume_set.py
  1411  BarcodeScan          automate_flo/blocks/barcode_scan.py
  1369  BatteryCharging      automate_flo/blocks/battery_charging.py
  1370  BatteryProperties    automate_flo/blocks/battery_properties.py
  1383  BluetoothDeviceActiveSet automate_flo/blocks/bluetooth_device_active_set.py
  1371  BluetoothDeviceBondCreate automate_flo/blocks/bluetooth_device_bond_create.py
  1393  BluetoothDeviceBondRemove automate_flo/blocks/bluetooth_device_bond_remove.py
  1211  BluetoothDeviceConnect automate_flo/blocks/bluetooth_device_connect.py
  1270  BluetoothDeviceDisconnect automate_flo/blocks/bluetooth_device_disconnect.py
  1154  BluetoothDevicePick  automate_flo/blocks/bluetooth_device_pick.py
  1277  BluetoothDeviceScan  automate_flo/blocks/bluetooth_device_scan.py
  1372  BluetoothGattRead    automate_flo/blocks/bluetooth_gatt_read.py
  1022  BroadcastReceive     automate_flo/blocks/broadcast_receive.py
  1023  BroadcastSend        automate_flo/blocks/broadcast_send.py
  1024  CallAnswer           automate_flo/blocks/call_answer.py
  1025  CallEnd              automate_flo/blocks/call_end.py
  1026  CallIncoming         automate_flo/blocks/call_incoming.py
  1027  CallNumber           automate_flo/blocks/call_number.py
  1028  CallOutgoing         automate_flo/blocks/call_outgoing.py
  1029  CallState            automate_flo/blocks/call_state.py
  1031  CaptureImage         automate_flo/blocks/capture_image.py
  1030  CellSignalLevel      automate_flo/blocks/cell_signal_level.py
  1034  ComposeEmail         automate_flo/blocks/compose_email.py
  1035  ComposeMms           automate_flo/blocks/compose_mms.py
  1036  ComposeSms           automate_flo/blocks/compose_sms.py
  1037  ContactQuery         automate_flo/blocks/contact_query.py
  1038  ContactPick          automate_flo/blocks/contact_pick.py
  1039  ContentRead          automate_flo/blocks/content_read.py
  1040  ContentPick          automate_flo/blocks/content_pick.py
  1041  ContentShared        automate_flo/blocks/content_shared.py
  1042  ContentView          automate_flo/blocks/content_view.py
  1043  DatePick             automate_flo/blocks/date_pick.py
  1044  RingtoneGet          automate_flo/blocks/ringtone_get.py
  1045  RingtoneSet          automate_flo/blocks/ringtone_set.py
  1047  DeviceDocked         automate_flo/blocks/device_docked.py
  1048  DeviceLock           automate_flo/blocks/device_lock.py
  1049  DeviceOrientation    automate_flo/blocks/device_orientation.py
  1050  DeviceUnlocked       automate_flo/blocks/device_unlocked.py
  1051  DialNumber           automate_flo/blocks/dial_number.py
  1052  DialogChoice         automate_flo/blocks/dialog_choice.py
  1053  DialogConfirm        automate_flo/blocks/dialog_confirm.py
  1054  DialogInput          automate_flo/blocks/dialog_input.py
  1055  DictionaryPut        automate_flo/blocks/dictionary_put.py
  1056  DictionaryRemove     automate_flo/blocks/dictionary_remove.py
  1057  DurationPick         automate_flo/blocks/duration_pick.py
  106   StringExpr (W)       automate_flo/base.py -- string literal expression wrapper
  104   DoubleExpr (J)       automate_flo/base.py -- double literal expression wrapper,
        plain 8-byte BE double, no length prefix (e.g. Delay's "duration")
  102   VariableExpr (I3.l)  automate_flo/base.py -- mutable-variable reference, plain
        UTF name, same wire shape as StringExpr but a distinct type
  25    java.lang.String (raw String object, distinct from the "W" expr wrapper
        -- used in some other slots, not needed for our target flow, not
        implemented by this library)
  1     BooleanExpr (boxed java.lang.Boolean) automate_flo/base.py -- single
        0/1 byte, no length prefix

Goto (id 1287, the block that jumps to a Label) is NOT implemented: its
field layout is a uvarint count + N object-refs into already-written
Label nodes, plus a dynamic labelValue expression -- meaningfully more
involved than everything else here and skipped. Label is still useful
standalone as a connectable no-op anchor reachable via any other block's
onComplete.

Every block above has a fixture in tests/fixtures/ that was pushed to a
real Automate 1.53.2 install on an Android-17 emulator via adb and
confirmed accepted (Automate's own "Import ... flow?" dialog, not a
rejection); see tests/test_emulator_import.py. FlowBeginning->AppKill is
additionally byte-exact-verified against an Automate-exported sample
built entirely by hand in the app UI, independent of this library.
"""

import struct

from .base import BooleanExpr, DoubleExpr, StringExpr, VariableExpr
from .blocks import ALL_BLOCKS

MAGIC = 0x4C41466C
VERSION = 114

REGISTRY = {cls.type_id: cls for cls in
            ALL_BLOCKS + [StringExpr, VariableExpr, DoubleExpr, BooleanExpr]}


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


# ---- Serialization ----

class FlowWriter:
    def __init__(self, w: ByteWriter):
        self.w = w
        self.seen = {}  # dedup key -> index in seen-list (0-indexed)
        self.next_index = 0

    @staticmethod
    def wrap_str(value):
        """Optional string-valued field: pass through None/StringExpr/
        VariableExpr as-is, or wrap a plain str as StringExpr -- lets
        callers write Delay("...", seconds=2) style plain values without
        constructing StringExpr by hand for every text field."""
        if value is None or isinstance(value, (StringExpr, VariableExpr)):
            return value
        return StringExpr(value)

    @staticmethod
    def wrap_bool(value):
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
    def wrap_double(value):
        """Optional numeric field: pass through None/DoubleExpr as-is, or
        wrap a plain Python int/float as DoubleExpr."""
        if value is None or isinstance(value, DoubleExpr):
            return value
        return DoubleExpr(value)

    def write_object(self, obj):
        if obj is None:
            self.w.write_svarint(0)
            return
        key = obj.dedup_key()
        if key in self.seen:
            idx = self.seen[key]
            self.w.write_svarint(-(idx + 1))
            return
        self.seen[key] = self.next_index
        self.next_index += 1
        self.w.write_svarint(obj.type_id)
        obj.write_fields(self)


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
        cls = REGISTRY.get(type_id)
        if cls is None:
            raise NotImplementedError(f"Unknown/unhandled type id {type_id} at byte {self.r.pos}")
        obj = cls.__new__(cls)
        self.seen.append(obj)
        obj.read_fields(self)
        return obj


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
    return "\n".join(b.describe() for b in blocks)

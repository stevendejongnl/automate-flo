"""
Concrete .flo block classes, one per file. Each class inherits from a base
in automate_flo.base (Action/Decision/IntermittentAction/
IntermittentDecision/LevelDecision) and implements only its own extra
fields' write_fields/read_fields; the inherited chain handles everything
common to its category. See automate_flo/format.py's module docstring for
the wire-format overview and a type-id index, and each file below for that
block's own field-layout detail and reverse-engineering notes.

Imports are explicit and hand-maintained (not auto-discovered via
pkgutil) -- deliberately, so "what blocks exist" is readable at a glance
here rather than implied by directory contents.
"""


from .accessibility_button import AccessibilityButton
from .account_generic_add import AccountGenericAdd
from .account_pick import AccountPick
from .account_sync_enabled import AccountSyncEnabled
from .account_sync_request import AccountSyncRequest
from .account_sync_set_state import AccountSyncSetState
from .activity_start import ActivityStart
from .activity_start_result import ActivityStartResult
from .activity_start_voice import ActivityStartVoice
from .adb_protocol_set import AdbProtocolSet
from .adb_shell_command import AdbShellCommand
from .airplane_mode_enabled import AirplaneModeEnabled
from .airplane_mode_set_state import AirplaneModeSetState
from .alarm import Alarm
from .alarm_add import AlarmAdd
from .alternative_launch import AlternativeLaunch
from .ambient_light import AmbientLight
from .ambient_temperature import AmbientTemperature
from .android_version import AndroidVersion
from .app_clear_cache import AppClearCache
from .app_foreground import AppForeground
from .app_installed import AppInstalled
from .app_kill import AppKill
from .app_kill_background import AppKillBackground
from .app_list import AppList
from .app_notifications_enabled import AppNotificationsEnabled
from .app_notifications_priority_get import AppNotificationsPriorityGet
from .app_notifications_priority_set import AppNotificationsPrioritySet
from .app_notifications_set_state import AppNotificationsSetState
from .app_notifications_visibility_get import AppNotificationsVisibilityGet
from .app_notifications_visibility_set import AppNotificationsVisibilitySet
from .app_op_mode import AppOpMode
from .app_op_mode_set import AppOpModeSet
from .app_pick import AppPick
from .app_usage import AppUsage
from .app_widget_configure import AppWidgetConfigure
from .array_add import ArrayAdd
from .array_remove import ArrayRemove
from .array_set import ArraySet
from .assist_request import AssistRequest
from .atmospheric_pressure import AtmosphericPressure
from .atomic_add import AtomicAdd
from .atomic_clear_all import AtomicClearAll
from .atomic_compare_and_store import AtomicCompareAndStore
from .atomic_load import AtomicLoad
from .atomic_store import AtomicStore
from .attention_light import AttentionLight
from .audio_device_connected import AudioDeviceConnected
from .audio_device_recording import AudioDeviceRecording
from .audio_player_control import AudioPlayerControl
from .audio_record_start import AudioRecordStart
from .audio_record_stop import AudioRecordStop
from .audio_stream_muted import AudioStreamMuted
from .audio_stream_set_mute import AudioStreamSetMute
from .audio_volume import AudioVolume
from .audio_volume_set import AudioVolumeSet
from .barcode_scan import BarcodeScan
from .battery_charging import BatteryCharging
from .battery_level import BatteryLevel
from .battery_properties import BatteryProperties
from .bluetooth_device_active_set import BluetoothDeviceActiveSet
from .bluetooth_device_bond_create import BluetoothDeviceBondCreate
from .bluetooth_device_bond_remove import BluetoothDeviceBondRemove
from .bluetooth_device_connect import BluetoothDeviceConnect
from .bluetooth_device_connected import BluetoothDeviceConnected
from .bluetooth_device_disconnect import BluetoothDeviceDisconnect
from .bluetooth_device_pick import BluetoothDevicePick
from .bluetooth_device_scan import BluetoothDeviceScan
from .bluetooth_enabled import BluetoothEnabled
from .bluetooth_gatt_read import BluetoothGattRead
from .bluetooth_set_state import BluetoothSetState
from .broadcast_receive import BroadcastReceive
from .broadcast_send import BroadcastSend
from .call_answer import CallAnswer
from .call_end import CallEnd
from .call_incoming import CallIncoming
from .call_number import CallNumber
from .call_outgoing import CallOutgoing
from .call_state import CallState
from .capture_image import CaptureImage
from .car_mode_enabled import CarModeEnabled
from .cell_signal_level import CellSignalLevel
from .clipboard_get import ClipboardGet
from .clipboard_set import ClipboardSet
from .compose_email import ComposeEmail
from .compose_mms import ComposeMms
from .compose_sms import ComposeSms
from .contact_pick import ContactPick
from .contact_query import ContactQuery
from .content_pick import ContentPick
from .content_read import ContentRead
from .content_shared import ContentShared
from .content_view import ContentView
from .date_pick import DatePick
from .delay import Delay
from .device_docked import DeviceDocked
from .device_keep_awake import DeviceKeepAwake
from .device_lock import DeviceLock
from .device_orientation import DeviceOrientation
from .device_unlocked import DeviceUnlocked
from .dial_number import DialNumber
from .dialog_choice import DialogChoice
from .dialog_confirm import DialogConfirm
from .dialog_input import DialogInput
from .dictionary_put import DictionaryPut
from .dictionary_remove import DictionaryRemove
from .duration_pick import DurationPick
from .expression_decision import ExpressionDecision
from .flow_beginning import FlowBeginning
from .http_request import HttpRequest
from .label import Label
from .log_append import LogAppend
from .notification_show import NotificationShow
from .ringtone_get import RingtoneGet
from .ringtone_set import RingtoneSet
from .screen_brightness import ScreenBrightness
from .screen_brightness_set import ScreenBrightnessSet
from .sms_send import SmsSend
from .toast_show import ToastShow
from .variable_assign import VariableAssign
from .wifi_enabled import WifiEnabled
from .wifi_network_connected import WifiNetworkConnected
from .wifi_set_state import WifiSetState

ALL_BLOCKS = [
    AccessibilityButton,
    AccountGenericAdd,
    AccountPick,
    AccountSyncEnabled,
    AccountSyncRequest,
    AccountSyncSetState,
    ActivityStart,
    ActivityStartResult,
    ActivityStartVoice,
    AdbProtocolSet,
    AdbShellCommand,
    AirplaneModeEnabled,
    AirplaneModeSetState,
    Alarm,
    AlarmAdd,
    AlternativeLaunch,
    AmbientLight,
    AmbientTemperature,
    AndroidVersion,
    AppClearCache,
    AppForeground,
    AppInstalled,
    AppKill,
    AppKillBackground,
    AppList,
    AppNotificationsEnabled,
    AppNotificationsPriorityGet,
    AppNotificationsPrioritySet,
    AppNotificationsSetState,
    AppNotificationsVisibilityGet,
    AppNotificationsVisibilitySet,
    AppOpMode,
    AppOpModeSet,
    AppPick,
    AppUsage,
    AppWidgetConfigure,
    ArrayAdd,
    ArrayRemove,
    ArraySet,
    AssistRequest,
    AtmosphericPressure,
    AtomicAdd,
    AtomicClearAll,
    AtomicCompareAndStore,
    AtomicLoad,
    AtomicStore,
    AttentionLight,
    AudioDeviceConnected,
    AudioDeviceRecording,
    AudioPlayerControl,
    AudioRecordStart,
    AudioRecordStop,
    AudioStreamMuted,
    AudioStreamSetMute,
    AudioVolume,
    AudioVolumeSet,
    BarcodeScan,
    BatteryCharging,
    BatteryLevel,
    BatteryProperties,
    BluetoothDeviceActiveSet,
    BluetoothDeviceBondCreate,
    BluetoothDeviceBondRemove,
    BluetoothDeviceConnect,
    BluetoothDeviceConnected,
    BluetoothDeviceDisconnect,
    BluetoothDevicePick,
    BluetoothDeviceScan,
    BluetoothEnabled,
    BluetoothGattRead,
    BluetoothSetState,
    BroadcastReceive,
    BroadcastSend,
    CallAnswer,
    CallEnd,
    CallIncoming,
    CallNumber,
    CallOutgoing,
    CallState,
    CaptureImage,
    CarModeEnabled,
    CellSignalLevel,
    ClipboardGet,
    ClipboardSet,
    ComposeEmail,
    ComposeMms,
    ComposeSms,
    ContactPick,
    ContactQuery,
    ContentPick,
    ContentRead,
    ContentShared,
    ContentView,
    DatePick,
    Delay,
    DeviceDocked,
    DeviceKeepAwake,
    DeviceLock,
    DeviceOrientation,
    DeviceUnlocked,
    DialNumber,
    DialogChoice,
    DialogConfirm,
    DialogInput,
    DictionaryPut,
    DictionaryRemove,
    DurationPick,
    ExpressionDecision,
    FlowBeginning,
    HttpRequest,
    Label,
    LogAppend,
    NotificationShow,
    RingtoneGet,
    RingtoneSet,
    ScreenBrightness,
    ScreenBrightnessSet,
    SmsSend,
    ToastShow,
    VariableAssign,
    WifiEnabled,
    WifiNetworkConnected,
    WifiSetState,
]

__all__ = [cls.__name__ for cls in ALL_BLOCKS] + ["ALL_BLOCKS"]

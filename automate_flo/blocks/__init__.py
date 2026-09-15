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
from .app_kill import AppKill
from .battery_level import BatteryLevel
from .bluetooth_device_connected import BluetoothDeviceConnected
from .bluetooth_enabled import BluetoothEnabled
from .bluetooth_set_state import BluetoothSetState
from .car_mode_enabled import CarModeEnabled
from .clipboard_get import ClipboardGet
from .clipboard_set import ClipboardSet
from .delay import Delay
from .device_keep_awake import DeviceKeepAwake
from .expression_decision import ExpressionDecision
from .flow_beginning import FlowBeginning
from .http_request import HttpRequest
from .label import Label
from .log_append import LogAppend
from .notification_show import NotificationShow
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
    AppKill,
    BatteryLevel,
    BluetoothDeviceConnected,
    BluetoothEnabled,
    BluetoothSetState,
    CarModeEnabled,
    ClipboardGet,
    ClipboardSet,
    Delay,
    DeviceKeepAwake,
    ExpressionDecision,
    FlowBeginning,
    HttpRequest,
    Label,
    LogAppend,
    NotificationShow,
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

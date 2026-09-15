import pathlib

from automate_flo import (
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
    DoubleExpr,
    ExpressionDecision,
    FlowBeginning,
    HttpRequest,
    Label,
    LogAppend,
    NotificationShow,
    ScreenBrightness,
    ScreenBrightnessSet,
    SmsSend,
    StringExpr,
    ToastShow,
    VariableAssign,
    VariableExpr,
    WifiEnabled,
    WifiNetworkConnected,
    WifiSetState,
    parse_flow,
    write_flow,
)

FIXTURES = pathlib.Path(__file__).parent / "fixtures"

# All fixtures use placeholder data (example.com, com.example.*, fictional
# NANP reserved numbers 555-0100..0199) -- none of it is real.
PKG = "com.example.targetapp"


def test_roundtrip_flow_beginning_app_kill_byte_exact():
    original = (FIXTURES / "flow-beginning-app-kill.flo").read_bytes()

    parsed = parse_flow(original)
    fb = parsed["blocks"][0]
    assert isinstance(fb, FlowBeginning)
    ak = fb.on_complete
    assert isinstance(ak, AppKill)
    assert ak.package_name == PKG
    assert ak.on_complete is None

    fb2 = FlowBeginning(stmt_id=1, cell_x=0, cell_y=0, title="")
    ak2 = AppKill(stmt_id=2, package_name=PKG, cell_x=0, cell_y=6)
    fb2.on_complete = ak2

    rebuilt = write_flow([fb2, ak2], next_id=2)
    assert rebuilt == original


def test_android_auto_app_toggle_flow_self_consistent():
    begin = FlowBeginning(stmt_id=1, cell_x=0, cell_y=0, title="")
    start = ActivityStart(stmt_id=2, package_name=PKG, cell_x=0, cell_y=6)
    delay = Delay(stmt_id=3, seconds=2.0, cell_x=0, cell_y=12)
    car = CarModeEnabled(stmt_id=4, cell_x=0, cell_y=18)
    kill = AppKill(stmt_id=5, package_name=PKG, cell_x=4, cell_y=24)

    begin.on_complete = start
    start.on_complete = delay
    delay.on_complete = car
    car.on_positive = delay
    car.on_negative = kill

    data = write_flow([begin, start, delay, car, kill], next_id=5)

    # Confirmed device-verified: this exact flow was imported and run
    # successfully in the real Automate app on Android 17.
    expected = (FIXTURES / "android-auto-app-toggle.flo").read_bytes()
    assert data == expected

    reparsed = parse_flow(data)
    r_begin = reparsed["blocks"][0]
    r_start = r_begin.on_complete
    assert isinstance(r_start, ActivityStart) and r_start.package_name == PKG
    r_delay = r_start.on_complete
    assert isinstance(r_delay, Delay) and r_delay.seconds == 2.0
    r_car = r_delay.on_complete
    assert isinstance(r_car, CarModeEnabled)
    assert r_car.on_positive is r_delay
    r_kill = r_car.on_negative
    assert isinstance(r_kill, AppKill) and r_kill.package_name == PKG


# Each test below round-trips against a fixture that was independently
# real-device-verified (see tests/test_emulator_import.py and README.md ->
# Status): Automate itself accepted the exact bytes these writers produce.

def test_toast_show_byte_exact():
    begin = FlowBeginning(stmt_id=1, cell_x=0, cell_y=0, title="")
    toast = ToastShow(stmt_id=2, message="hello from automate-flo", cell_x=0, cell_y=6)
    begin.on_complete = toast

    data = write_flow([begin, toast], next_id=2)
    assert data == (FIXTURES / "toast-show.flo").read_bytes()


def test_sms_send_byte_exact():
    begin = FlowBeginning(stmt_id=1, cell_x=0, cell_y=0, title="")
    # +1-555-0100..0199 is reserved by NANP for fictional use.
    sms = SmsSend(stmt_id=2, phone_number="+15555550123", message="test", cell_x=0, cell_y=6)
    begin.on_complete = sms

    data = write_flow([begin, sms], next_id=2)
    assert data == (FIXTURES / "sms-send.flo").read_bytes()


def test_variable_assign_byte_exact():
    begin = FlowBeginning(stmt_id=1, cell_x=0, cell_y=0, title="")
    va = VariableAssign(stmt_id=2, variable_name="myVar", value="hello", cell_x=0, cell_y=6)
    begin.on_complete = va

    data = write_flow([begin, va], next_id=2)
    assert data == (FIXTURES / "variable-assign.flo").read_bytes()


def test_battery_level_byte_exact():
    begin = FlowBeginning(stmt_id=1, cell_x=0, cell_y=0, title="")
    bl = BatteryLevel(stmt_id=2, cell_x=0, cell_y=6)
    kill = AppKill(stmt_id=3, package_name=PKG, cell_x=0, cell_y=12)
    begin.on_complete = bl
    bl.on_positive = kill
    bl.on_negative = None

    data = write_flow([begin, bl, kill], next_id=3)
    assert data == (FIXTURES / "battery-level.flo").read_bytes()


def test_wifi_network_connected_byte_exact():
    begin = FlowBeginning(stmt_id=1, cell_x=0, cell_y=0, title="")
    wc = WifiNetworkConnected(stmt_id=2, cell_x=0, cell_y=6)
    begin.on_complete = wc

    data = write_flow([begin, wc], next_id=2)
    assert data == (FIXTURES / "wifi-connected.flo").read_bytes()


def test_bluetooth_device_connected_byte_exact():
    begin = FlowBeginning(stmt_id=1, cell_x=0, cell_y=0, title="")
    bt = BluetoothDeviceConnected(stmt_id=2, cell_x=0, cell_y=6)
    begin.on_complete = bt

    data = write_flow([begin, bt], next_id=2)
    assert data == (FIXTURES / "bt-connected.flo").read_bytes()


def test_notification_show_byte_exact():
    begin = FlowBeginning(stmt_id=1, cell_x=0, cell_y=0, title="")
    ns = NotificationShow(stmt_id=2, title="Hi", message="World", cell_x=0, cell_y=6)
    begin.on_complete = ns

    data = write_flow([begin, ns], next_id=2)
    assert data == (FIXTURES / "notification-show.flo").read_bytes()


def test_http_request_byte_exact():
    begin = FlowBeginning(stmt_id=1, cell_x=0, cell_y=0, title="")
    hr = HttpRequest(stmt_id=2, url="https://example.com", cell_x=0, cell_y=6)
    begin.on_complete = hr

    data = write_flow([begin, hr], next_id=2)
    assert data == (FIXTURES / "http-request.flo").read_bytes()


def test_expression_decision_byte_exact():
    begin = FlowBeginning(stmt_id=1, cell_x=0, cell_y=0, title="")
    ed = ExpressionDecision(stmt_id=2, expression=StringExpr("true"), cell_x=0, cell_y=6)
    begin.on_complete = ed

    data = write_flow([begin, ed], next_id=2)
    assert data == (FIXTURES / "expression-decision.flo").read_bytes()


def test_label_byte_exact():
    begin = FlowBeginning(stmt_id=1, cell_x=0, cell_y=0, title="")
    lbl = Label(stmt_id=2, value=StringExpr("myLabel"), cell_x=0, cell_y=6)
    begin.on_complete = lbl

    data = write_flow([begin, lbl], next_id=2)
    assert data == (FIXTURES / "label.flo").read_bytes()


def test_clipboard_set_byte_exact():
    begin = FlowBeginning(stmt_id=1, cell_x=0, cell_y=0, title="")
    cs = ClipboardSet(stmt_id=2, text="hello clipboard", cell_x=0, cell_y=6)
    begin.on_complete = cs

    data = write_flow([begin, cs], next_id=2)
    assert data == (FIXTURES / "clipboard-set.flo").read_bytes()


def test_clipboard_get_byte_exact():
    begin = FlowBeginning(stmt_id=1, cell_x=0, cell_y=0, title="")
    cg = ClipboardGet(stmt_id=2, var_content=VariableExpr("clip"), cell_x=0, cell_y=6)
    begin.on_complete = cg

    data = write_flow([begin, cg], next_id=2)
    assert data == (FIXTURES / "clipboard-get.flo").read_bytes()


def test_wifi_enabled_byte_exact():
    begin = FlowBeginning(stmt_id=1, cell_x=0, cell_y=0, title="")
    we = WifiEnabled(stmt_id=2, cell_x=0, cell_y=6)
    begin.on_complete = we

    data = write_flow([begin, we], next_id=2)
    assert data == (FIXTURES / "wifi-enabled.flo").read_bytes()


def test_wifi_set_state_byte_exact():
    begin = FlowBeginning(stmt_id=1, cell_x=0, cell_y=0, title="")
    ws = WifiSetState(stmt_id=2, state=True, cell_x=0, cell_y=6)
    begin.on_complete = ws

    data = write_flow([begin, ws], next_id=2)
    assert data == (FIXTURES / "wifi-set-state.flo").read_bytes()


def test_bluetooth_enabled_byte_exact():
    begin = FlowBeginning(stmt_id=1, cell_x=0, cell_y=0, title="")
    be = BluetoothEnabled(stmt_id=2, cell_x=0, cell_y=6)
    begin.on_complete = be

    data = write_flow([begin, be], next_id=2)
    assert data == (FIXTURES / "bluetooth-enabled.flo").read_bytes()


def test_bluetooth_set_state_byte_exact():
    begin = FlowBeginning(stmt_id=1, cell_x=0, cell_y=0, title="")
    bs = BluetoothSetState(stmt_id=2, state=True, cell_x=0, cell_y=6)
    begin.on_complete = bs

    data = write_flow([begin, bs], next_id=2)
    assert data == (FIXTURES / "bluetooth-set-state.flo").read_bytes()


def test_screen_brightness_byte_exact():
    begin = FlowBeginning(stmt_id=1, cell_x=0, cell_y=0, title="")
    sb = ScreenBrightness(stmt_id=2, cell_x=0, cell_y=6)
    begin.on_complete = sb

    data = write_flow([begin, sb], next_id=2)
    assert data == (FIXTURES / "screen-brightness.flo").read_bytes()


def test_screen_brightness_set_byte_exact():
    begin = FlowBeginning(stmt_id=1, cell_x=0, cell_y=0, title="")
    sbs = ScreenBrightnessSet(stmt_id=2, level=50.0, cell_x=0, cell_y=6)
    begin.on_complete = sbs

    data = write_flow([begin, sbs], next_id=2)
    assert data == (FIXTURES / "screen-brightness-set.flo").read_bytes()


def test_device_keep_awake_byte_exact():
    begin = FlowBeginning(stmt_id=1, cell_x=0, cell_y=0, title="")
    dka = DeviceKeepAwake(stmt_id=2, cell_x=0, cell_y=6)
    begin.on_complete = dka

    data = write_flow([begin, dka], next_id=2)
    assert data == (FIXTURES / "device-keep-awake.flo").read_bytes()


def test_log_append_byte_exact():
    begin = FlowBeginning(stmt_id=1, cell_x=0, cell_y=0, title="")
    la = LogAppend(stmt_id=2, message="hello from automate-flo", cell_x=0, cell_y=6)
    begin.on_complete = la

    data = write_flow([begin, la], next_id=2)
    assert data == (FIXTURES / "log-append.flo").read_bytes()


def test_accessibility_button_byte_exact():
    begin = FlowBeginning(stmt_id=1, cell_x=0, cell_y=0, title="")
    ab = AccessibilityButton(stmt_id=2, cell_x=0, cell_y=6)
    begin.on_complete = ab

    data = write_flow([begin, ab], next_id=2)
    assert data == (FIXTURES / "accessibility-button.flo").read_bytes()


def test_account_generic_add_byte_exact():
    begin = FlowBeginning(stmt_id=1, cell_x=0, cell_y=0, title="")
    aga = AccountGenericAdd(stmt_id=2, account_name="myaccount", username="bob",
                             password="hunter2", cell_x=0, cell_y=6)
    begin.on_complete = aga

    data = write_flow([begin, aga], next_id=2)
    assert data == (FIXTURES / "account-generic-add.flo").read_bytes()


def test_account_pick_byte_exact():
    begin = FlowBeginning(stmt_id=1, cell_x=0, cell_y=0, title="")
    ap = AccountPick(stmt_id=2, cell_x=0, cell_y=6)
    begin.on_complete = ap

    data = write_flow([begin, ap], next_id=2)
    assert data == (FIXTURES / "account-pick.flo").read_bytes()


def test_account_sync_enabled_byte_exact():
    begin = FlowBeginning(stmt_id=1, cell_x=0, cell_y=0, title="")
    ase = AccountSyncEnabled(stmt_id=2, cell_x=0, cell_y=6)
    begin.on_complete = ase

    data = write_flow([begin, ase], next_id=2)
    assert data == (FIXTURES / "account-sync-enabled.flo").read_bytes()


def test_account_sync_request_byte_exact():
    begin = FlowBeginning(stmt_id=1, cell_x=0, cell_y=0, title="")
    asr = AccountSyncRequest(stmt_id=2, cell_x=0, cell_y=6)
    begin.on_complete = asr

    data = write_flow([begin, asr], next_id=2)
    assert data == (FIXTURES / "account-sync-request.flo").read_bytes()


def test_account_sync_set_state_byte_exact():
    begin = FlowBeginning(stmt_id=1, cell_x=0, cell_y=0, title="")
    asss = AccountSyncSetState(stmt_id=2, state=True, cell_x=0, cell_y=6)
    begin.on_complete = asss

    data = write_flow([begin, asss], next_id=2)
    assert data == (FIXTURES / "account-sync-set-state.flo").read_bytes()


def test_activity_start_result_byte_exact():
    begin = FlowBeginning(stmt_id=1, cell_x=0, cell_y=0, title="")
    asr = ActivityStartResult(stmt_id=2, package_name="com.example.app", cell_x=0, cell_y=6)
    begin.on_complete = asr

    data = write_flow([begin, asr], next_id=2)
    assert data == (FIXTURES / "activity-start-result.flo").read_bytes()


def test_activity_start_voice_byte_exact():
    begin = FlowBeginning(stmt_id=1, cell_x=0, cell_y=0, title="")
    asv = ActivityStartVoice(stmt_id=2, package_name="com.example.app", cell_x=0, cell_y=6)
    begin.on_complete = asv

    data = write_flow([begin, asv], next_id=2)
    assert data == (FIXTURES / "activity-start-voice.flo").read_bytes()


def test_adb_shell_command_byte_exact():
    begin = FlowBeginning(stmt_id=1, cell_x=0, cell_y=0, title="")
    asc = AdbShellCommand(stmt_id=2, command="echo hi", cell_x=0, cell_y=6)
    begin.on_complete = asc

    data = write_flow([begin, asc], next_id=2)
    assert data == (FIXTURES / "adb-shell-command.flo").read_bytes()


def test_adb_protocol_set_byte_exact():
    begin = FlowBeginning(stmt_id=1, cell_x=0, cell_y=0, title="")
    aps = AdbProtocolSet(stmt_id=2, cell_x=0, cell_y=6)
    begin.on_complete = aps

    data = write_flow([begin, aps], next_id=2)
    assert data == (FIXTURES / "adb-protocol-set.flo").read_bytes()


def test_airplane_mode_enabled_byte_exact():
    begin = FlowBeginning(stmt_id=1, cell_x=0, cell_y=0, title="")
    ame = AirplaneModeEnabled(stmt_id=2, cell_x=0, cell_y=6)
    begin.on_complete = ame

    data = write_flow([begin, ame], next_id=2)
    assert data == (FIXTURES / "airplane-mode-enabled.flo").read_bytes()


def test_airplane_mode_set_state_byte_exact():
    begin = FlowBeginning(stmt_id=1, cell_x=0, cell_y=0, title="")
    amss = AirplaneModeSetState(stmt_id=2, state=True, cell_x=0, cell_y=6)
    begin.on_complete = amss

    data = write_flow([begin, amss], next_id=2)
    assert data == (FIXTURES / "airplane-mode-set-state.flo").read_bytes()


def test_alarm_byte_exact():
    begin = FlowBeginning(stmt_id=1, cell_x=0, cell_y=0, title="")
    a = Alarm(stmt_id=2, cell_x=0, cell_y=6,
              var_alarm_timestamp=VariableExpr("alarmTime"))
    begin.on_complete = a

    data = write_flow([begin, a], next_id=2)
    assert data == (FIXTURES / "alarm.flo").read_bytes()


def test_alarm_add_byte_exact():
    begin = FlowBeginning(stmt_id=1, cell_x=0, cell_y=0, title="")
    aa = AlarmAdd(stmt_id=2, cell_x=0, cell_y=6, time_of_day=28800000.0,
                  weekdays=62.0, label="Wake up",
                  sound_uri="content://media/alarm", vibrate=True)
    begin.on_complete = aa

    data = write_flow([begin, aa], next_id=2)
    assert data == (FIXTURES / "alarm-add.flo").read_bytes()


def test_alternative_launch_byte_exact():
    begin = FlowBeginning(stmt_id=1, cell_x=0, cell_y=0, title="")
    al = AlternativeLaunch(stmt_id=2, cell_x=0, cell_y=6, title="My App")
    begin.on_complete = al

    data = write_flow([begin, al], next_id=2)
    assert data == (FIXTURES / "alternative-launch.flo").read_bytes()


def test_ambient_light_byte_exact():
    begin = FlowBeginning(stmt_id=1, cell_x=0, cell_y=0, title="")
    al = AmbientLight(stmt_id=2, cell_x=0, cell_y=6)
    begin.on_complete = al

    data = write_flow([begin, al], next_id=2)
    assert data == (FIXTURES / "ambient-light.flo").read_bytes()


def test_ambient_temperature_byte_exact():
    begin = FlowBeginning(stmt_id=1, cell_x=0, cell_y=0, title="")
    at = AmbientTemperature(stmt_id=2, cell_x=0, cell_y=6)
    begin.on_complete = at

    data = write_flow([begin, at], next_id=2)
    assert data == (FIXTURES / "ambient-temperature.flo").read_bytes()


def test_android_version_byte_exact():
    begin = FlowBeginning(stmt_id=1, cell_x=0, cell_y=0, title="")
    av = AndroidVersion(stmt_id=2, cell_x=0, cell_y=6, min_level=DoubleExpr(21.0),
                         max_level=DoubleExpr(33.0), var_level=VariableExpr("sdk"))
    begin.on_complete = av

    data = write_flow([begin, av], next_id=2)
    assert data == (FIXTURES / "android-version.flo").read_bytes()


def test_app_clear_cache_byte_exact():
    begin = FlowBeginning(stmt_id=1, cell_x=0, cell_y=0, title="")
    acc = AppClearCache(stmt_id=2, package_name=PKG, cell_x=0, cell_y=6)
    begin.on_complete = acc

    data = write_flow([begin, acc], next_id=2)
    assert data == (FIXTURES / "app-clear-cache.flo").read_bytes()

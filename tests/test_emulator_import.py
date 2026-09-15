"""Import every fixture .flo into a real Automate install and confirm the
app itself accepts it, instead of only trusting our own parser.

Requires a running device/emulator with Automate installed, since the APK
isn't ours to redistribute (LlamaLab's proprietary app). See README.md ->
"Testing against the real app" for how to set one up. Skipped entirely if
that's not available -- this file makes no assumption about how or whether
you've prepared one, it just checks and bails if not.

Set AUTOMATE_FLO_DEVICE_SERIAL to the adb serial to test against, e.g.:

    AUTOMATE_FLO_DEVICE_SERIAL=emulator-5554 uv run pytest tests/test_emulator_import.py
"""

import os
import pathlib

import pytest

from tests.emulator import (
    automate_installed,
    device_online,
    ensure_storage_permission,
    import_flow,
)

FIXTURES = pathlib.Path(__file__).parent / "fixtures"
SERIAL = os.environ.get("AUTOMATE_FLO_DEVICE_SERIAL")

pytestmark = pytest.mark.skipif(
    not SERIAL,
    reason="set AUTOMATE_FLO_DEVICE_SERIAL to an adb device serial to run "
           "these tests against a real Automate install",
)


@pytest.fixture(scope="module", autouse=True)
def _require_device_and_app():
    if not device_online(SERIAL):
        pytest.skip(f"device {SERIAL!r} not online (check `adb devices`)")
    if not automate_installed(SERIAL):
        pytest.skip(
            "Automate is not installed on this device. Download the APK "
            "yourself (LlamaLab does not permit redistribution) and: "
            f"adb -s {SERIAL} install -r Automate_<version>.apk"
        )
    ensure_storage_permission(SERIAL)


@pytest.mark.parametrize("fixture_name", [
    "flow-beginning-app-kill.flo",
    "android-auto-app-toggle.flo",
    "toast-show.flo",
    "sms-send.flo",
    "variable-assign.flo",
    "battery-level.flo",
    "wifi-connected.flo",
    "bt-connected.flo",
    "notification-show.flo",
    "http-request.flo",
    "expression-decision.flo",
    "label.flo",
    "clipboard-set.flo",
    "clipboard-get.flo",
    "wifi-enabled.flo",
    "wifi-set-state.flo",
    "bluetooth-enabled.flo",
    "bluetooth-set-state.flo",
    "screen-brightness.flo",
    "screen-brightness-set.flo",
    "device-keep-awake.flo",
    "log-append.flo",
    "accessibility-button.flo",
    "account-generic-add.flo",
    "account-pick.flo",
    "account-sync-enabled.flo",
    "account-sync-request.flo",
    "account-sync-set-state.flo",
    "activity-start-result.flo",
    "activity-start-voice.flo",
    "adb-shell-command.flo",
    "adb-protocol-set.flo",
    "airplane-mode-enabled.flo",
    "airplane-mode-set-state.flo",
    "alarm.flo",
    "alarm-add.flo",
    "alternative-launch.flo",
    "ambient-light.flo",
    "ambient-temperature.flo",
    "android-version.flo",
    "app-clear-cache.flo",
    "app-foreground.flo",
    "app-installed.flo",
    "app-kill-background.flo",
    "app-list.flo",
    "app-notifications-enabled.flo",
    "app-notifications-priority-get.flo",
    "app-notifications-priority-set.flo",
    "app-notifications-set-state.flo",
    "app-notifications-visibility-get.flo",
    "app-notifications-visibility-set.flo",
    "app-op-mode.flo",
    "app-op-mode-set.flo",
    "app-pick.flo",
    "app-usage.flo",
    "app-widget-configure.flo",
])
def test_fixture_imports_cleanly(fixture_name):
    path = FIXTURES / fixture_name
    dialog_text = import_flow(SERIAL, path)

    assert "Failed to read flow" not in dialog_text, (
        f"Automate rejected {fixture_name}:\n{dialog_text}"
    )
    assert "flow?" in dialog_text.lower(), (
        f"Expected an 'Import \"...\" flow?' confirmation dialog, got:\n{dialog_text}"
    )

"""Cross-cutting multi-block flow tests that don't belong to any single
block -- per-block tests live next to their source in automate_flo/blocks/
(see conftest.py for the shared device-verification fixtures)."""

import pathlib

from automate_flo import (
    ActivityStart,
    AppKill,
    CarModeEnabled,
    Delay,
    FlowBeginning,
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


def test_flow_beginning_app_kill_imports_cleanly(import_flow_fn):
    dialog_text = import_flow_fn(FIXTURES / "flow-beginning-app-kill.flo")

    assert "Failed to read flow" not in dialog_text, (
        f"Automate rejected flow-beginning-app-kill.flo:\n{dialog_text}"
    )
    assert "flow?" in dialog_text.lower(), (
        f"Expected an 'Import \"...\" flow?' confirmation dialog, got:\n{dialog_text}"
    )


def test_android_auto_app_toggle_imports_cleanly(import_flow_fn):
    dialog_text = import_flow_fn(FIXTURES / "android-auto-app-toggle.flo")

    assert "Failed to read flow" not in dialog_text, (
        f"Automate rejected android-auto-app-toggle.flo:\n{dialog_text}"
    )
    assert "flow?" in dialog_text.lower(), (
        f"Expected an 'Import \"...\" flow?' confirmation dialog, got:\n{dialog_text}"
    )

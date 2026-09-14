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


def test_roundtrip_flow_beginning_app_kill_byte_exact():
    original = (FIXTURES / "flow-beginning-app-kill.flo").read_bytes()

    parsed = parse_flow(original)
    fb = parsed["blocks"][0]
    assert isinstance(fb, FlowBeginning)
    ak = fb.on_complete
    assert isinstance(ak, AppKill)
    assert ak.package_name == "nl.flitsmeister"
    assert ak.on_complete is None

    fb2 = FlowBeginning(stmt_id=1, cell_x=0, cell_y=0, title="")
    ak2 = AppKill(stmt_id=2, package_name="nl.flitsmeister", cell_x=0, cell_y=6)
    fb2.on_complete = ak2

    rebuilt = write_flow([fb2, ak2], next_id=2)
    assert rebuilt == original


def test_android_auto_flitsmeister_flow_self_consistent():
    begin = FlowBeginning(stmt_id=1, cell_x=0, cell_y=0, title="")
    start = ActivityStart(stmt_id=2, package_name="nl.flitsmeister", cell_x=0, cell_y=6)
    delay = Delay(stmt_id=3, seconds=2.0, cell_x=0, cell_y=12)
    car = CarModeEnabled(stmt_id=4, cell_x=0, cell_y=18)
    kill = AppKill(stmt_id=5, package_name="nl.flitsmeister", cell_x=4, cell_y=24)

    begin.on_complete = start
    start.on_complete = delay
    delay.on_complete = car
    car.on_positive = delay
    car.on_negative = kill

    data = write_flow([begin, start, delay, car, kill], next_id=5)

    # Confirmed device-verified: this exact flow was imported and run
    # successfully in the real Automate app on Android 17.
    expected = (FIXTURES / "android-auto-flitsmeister.flo").read_bytes()
    assert data == expected

    reparsed = parse_flow(data)
    r_begin = reparsed["blocks"][0]
    r_start = r_begin.on_complete
    assert isinstance(r_start, ActivityStart) and r_start.package_name == "nl.flitsmeister"
    r_delay = r_start.on_complete
    assert isinstance(r_delay, Delay) and r_delay.seconds == 2.0
    r_car = r_delay.on_complete
    assert isinstance(r_car, CarModeEnabled)
    assert r_car.on_positive is r_delay
    r_kill = r_car.on_negative
    assert isinstance(r_kill, AppKill) and r_kill.package_name == "nl.flitsmeister"

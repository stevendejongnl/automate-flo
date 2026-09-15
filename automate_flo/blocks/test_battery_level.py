import pathlib

from automate_flo import AppKill, BatteryLevel, FlowBeginning, write_flow

PKG = "com.example.targetapp"


def test_battery_level_byte_exact():
    begin = FlowBeginning(stmt_id=1, cell_x=0, cell_y=0, title="")
    bl = BatteryLevel(stmt_id=2, cell_x=0, cell_y=6)
    kill = AppKill(stmt_id=3, package_name=PKG, cell_x=0, cell_y=12)
    begin.on_complete = bl
    bl.on_positive = kill
    bl.on_negative = None

    data = write_flow([begin, bl, kill], next_id=3)
    assert data == (pathlib.Path(__file__).parent / "battery_level.flo").read_bytes()


def test_battery_level_imports_cleanly(import_flow_fn):
    dialog_text = import_flow_fn(pathlib.Path(__file__).parent / "battery_level.flo")

    assert "Failed to read flow" not in dialog_text, (
        f"Automate rejected battery_level.flo:\n{dialog_text}"
    )
    assert "flow?" in dialog_text.lower(), (
        f"Expected an 'Import \"...\" flow?' confirmation dialog, got:\n{dialog_text}"
    )

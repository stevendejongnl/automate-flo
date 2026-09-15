import pathlib

from automate_flo import BatteryProperties, FlowBeginning, VariableExpr, write_flow


def test_battery_properties_byte_exact():
    begin = FlowBeginning(stmt_id=1, cell_x=0, cell_y=0, title="")
    b = BatteryProperties(stmt_id=2, var_capacity=VariableExpr("capacity"))
    b.cell_x, b.cell_y = 0, 6
    begin.on_complete = b

    data = write_flow([begin, b], next_id=2)
    assert data == (pathlib.Path(__file__).parent / "battery_properties.flo").read_bytes()


def test_battery_properties_imports_cleanly(import_flow_fn):
    dialog_text = import_flow_fn(pathlib.Path(__file__).parent / "battery_properties.flo")

    assert "Failed to read flow" not in dialog_text, (
        f"Automate rejected battery_properties.flo:\n{dialog_text}"
    )
    assert "flow?" in dialog_text.lower(), (
        f"Expected an 'Import \"...\" flow?' confirmation dialog, got:\n{dialog_text}"
    )

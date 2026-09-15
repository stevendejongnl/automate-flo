import pathlib

from automate_flo import BluetoothGattRead, FlowBeginning, VariableExpr, write_flow


def test_bluetooth_gatt_read_byte_exact():
    begin = FlowBeginning(stmt_id=1, cell_x=0, cell_y=0, title="")
    b = BluetoothGattRead(stmt_id=2, device_address="AA:BB:CC:DD:EE:FF", var_result=VariableExpr("gattResult"))
    b.cell_x, b.cell_y = 0, 6
    begin.on_complete = b

    data = write_flow([begin, b], next_id=2)
    assert data == (pathlib.Path(__file__).parent / "bluetooth_gatt_read.flo").read_bytes()


def test_bluetooth_gatt_read_imports_cleanly(import_flow_fn):
    dialog_text = import_flow_fn(pathlib.Path(__file__).parent / "bluetooth_gatt_read.flo")

    assert "Failed to read flow" not in dialog_text, (
        f"Automate rejected bluetooth_gatt_read.flo:\n{dialog_text}"
    )
    assert "flow?" in dialog_text.lower(), (
        f"Expected an 'Import \"...\" flow?' confirmation dialog, got:\n{dialog_text}"
    )

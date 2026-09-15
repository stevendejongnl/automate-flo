import pathlib

from automate_flo import BluetoothDeviceBondCreate, FlowBeginning, write_flow


def test_bluetooth_device_bond_create_byte_exact():
    begin = FlowBeginning(stmt_id=1, cell_x=0, cell_y=0, title="")
    b = BluetoothDeviceBondCreate(stmt_id=2, device_address="AA:BB:CC:DD:EE:FF")
    b.cell_x, b.cell_y = 0, 6
    begin.on_complete = b

    data = write_flow([begin, b], next_id=2)
    assert data == (pathlib.Path(__file__).parent / "bluetooth_device_bond_create.flo").read_bytes()


def test_bluetooth_device_bond_create_imports_cleanly(import_flow_fn):
    dialog_text = import_flow_fn(pathlib.Path(__file__).parent / "bluetooth_device_bond_create.flo")

    assert "Failed to read flow" not in dialog_text, (
        f"Automate rejected bluetooth_device_bond_create.flo:\n{dialog_text}"
    )
    assert "flow?" in dialog_text.lower(), (
        f"Expected an 'Import \"...\" flow?' confirmation dialog, got:\n{dialog_text}"
    )

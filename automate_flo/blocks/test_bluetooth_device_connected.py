import pathlib

from automate_flo import BluetoothDeviceConnected, FlowBeginning, write_flow


def test_bluetooth_device_connected_byte_exact():
    begin = FlowBeginning(stmt_id=1, cell_x=0, cell_y=0, title="")
    bt = BluetoothDeviceConnected(stmt_id=2, cell_x=0, cell_y=6)
    begin.on_complete = bt

    data = write_flow([begin, bt], next_id=2)
    assert data == (pathlib.Path(__file__).parent / "bluetooth_device_connected.flo").read_bytes()


def test_bluetooth_device_connected_imports_cleanly(import_flow_fn):
    dialog_text = import_flow_fn(pathlib.Path(__file__).parent / "bluetooth_device_connected.flo")

    assert "Failed to read flow" not in dialog_text, (
        f"Automate rejected bluetooth_device_connected.flo:\n{dialog_text}"
    )
    assert "flow?" in dialog_text.lower(), (
        f"Expected an 'Import \"...\" flow?' confirmation dialog, got:\n{dialog_text}"
    )

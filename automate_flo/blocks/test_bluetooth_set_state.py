import pathlib

from automate_flo import BluetoothSetState, FlowBeginning, write_flow


def test_bluetooth_set_state_byte_exact():
    begin = FlowBeginning(stmt_id=1, cell_x=0, cell_y=0, title="")
    bs = BluetoothSetState(stmt_id=2, state=True, cell_x=0, cell_y=6)
    begin.on_complete = bs

    data = write_flow([begin, bs], next_id=2)
    assert data == (pathlib.Path(__file__).parent / "bluetooth_set_state.flo").read_bytes()


def test_bluetooth_set_state_imports_cleanly(import_flow_fn):
    dialog_text = import_flow_fn(pathlib.Path(__file__).parent / "bluetooth_set_state.flo")

    assert "Failed to read flow" not in dialog_text, (
        f"Automate rejected bluetooth_set_state.flo:\n{dialog_text}"
    )
    assert "flow?" in dialog_text.lower(), (
        f"Expected an 'Import \"...\" flow?' confirmation dialog, got:\n{dialog_text}"
    )

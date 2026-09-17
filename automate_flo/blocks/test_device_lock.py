import pathlib

from automate_flo import DeviceLock, FlowBeginning, write_flow


def test_device_lock_byte_exact():
    begin = FlowBeginning(stmt_id=1, cell_x=0, cell_y=0, title="")
    b = DeviceLock(stmt_id=2, cell_x=0, cell_y=6)
    begin.on_complete = b

    data = write_flow([begin, b], next_id=2)
    assert data == (pathlib.Path(__file__).parent / "device_lock.flo").read_bytes()


def test_device_lock_imports_cleanly(import_flow_fn):
    dialog_text = import_flow_fn(pathlib.Path(__file__).parent / "device_lock.flo")

    assert "Failed to read flow" not in dialog_text, (
        f"Automate rejected device_lock.flo:\n{dialog_text}"
    )
    assert "flow?" in dialog_text.lower(), (
        f"Expected an 'Import \"...\" flow?' confirmation dialog, got:\n{dialog_text}"
    )

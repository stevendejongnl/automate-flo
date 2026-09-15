import pathlib

from automate_flo import DeviceKeepAwake, FlowBeginning, write_flow


def test_device_keep_awake_byte_exact():
    begin = FlowBeginning(stmt_id=1, cell_x=0, cell_y=0, title="")
    dka = DeviceKeepAwake(stmt_id=2, cell_x=0, cell_y=6)
    begin.on_complete = dka

    data = write_flow([begin, dka], next_id=2)
    assert data == (pathlib.Path(__file__).parent / "device_keep_awake.flo").read_bytes()


def test_device_keep_awake_imports_cleanly(import_flow_fn):
    dialog_text = import_flow_fn(pathlib.Path(__file__).parent / "device_keep_awake.flo")

    assert "Failed to read flow" not in dialog_text, (
        f"Automate rejected device_keep_awake.flo:\n{dialog_text}"
    )
    assert "flow?" in dialog_text.lower(), (
        f"Expected an 'Import \"...\" flow?' confirmation dialog, got:\n{dialog_text}"
    )

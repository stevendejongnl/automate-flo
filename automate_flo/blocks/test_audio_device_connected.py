import pathlib

from automate_flo import AudioDeviceConnected, FlowBeginning, VariableExpr, write_flow


def test_audio_device_connected_byte_exact():
    begin = FlowBeginning(stmt_id=1, cell_x=0, cell_y=0, title="")
    b = AudioDeviceConnected(stmt_id=2, var_connected_device_type=VariableExpr("devType"))
    b.cell_x, b.cell_y = 0, 6
    begin.on_complete = b

    data = write_flow([begin, b], next_id=2)
    assert data == (pathlib.Path(__file__).parent / "audio_device_connected.flo").read_bytes()


def test_audio_device_connected_imports_cleanly(import_flow_fn):
    dialog_text = import_flow_fn(pathlib.Path(__file__).parent / "audio_device_connected.flo")

    assert "Failed to read flow" not in dialog_text, (
        f"Automate rejected audio_device_connected.flo:\n{dialog_text}"
    )
    assert "flow?" in dialog_text.lower(), (
        f"Expected an 'Import \"...\" flow?' confirmation dialog, got:\n{dialog_text}"
    )

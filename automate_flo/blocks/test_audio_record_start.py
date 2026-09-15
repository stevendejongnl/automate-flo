import pathlib

from automate_flo import AudioRecordStart, FlowBeginning, VariableExpr, write_flow


def test_audio_record_start_byte_exact():
    begin = FlowBeginning(stmt_id=1, cell_x=0, cell_y=0, title="")
    b = AudioRecordStart(stmt_id=2, var_audio_file=VariableExpr("audioFile"))
    b.cell_x, b.cell_y = 0, 6
    begin.on_complete = b

    data = write_flow([begin, b], next_id=2)
    assert data == (pathlib.Path(__file__).parent / "audio_record_start.flo").read_bytes()


def test_audio_record_start_imports_cleanly(import_flow_fn):
    dialog_text = import_flow_fn(pathlib.Path(__file__).parent / "audio_record_start.flo")

    assert "Failed to read flow" not in dialog_text, (
        f"Automate rejected audio_record_start.flo:\n{dialog_text}"
    )
    assert "flow?" in dialog_text.lower(), (
        f"Expected an 'Import \"...\" flow?' confirmation dialog, got:\n{dialog_text}"
    )

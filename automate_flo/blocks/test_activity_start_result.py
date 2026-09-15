import pathlib

from automate_flo import ActivityStartResult, FlowBeginning, write_flow


def test_activity_start_result_byte_exact():
    begin = FlowBeginning(stmt_id=1, cell_x=0, cell_y=0, title="")
    asr = ActivityStartResult(stmt_id=2, package_name="com.example.app", cell_x=0, cell_y=6)
    begin.on_complete = asr

    data = write_flow([begin, asr], next_id=2)
    assert data == (pathlib.Path(__file__).parent / "activity_start_result.flo").read_bytes()


def test_activity_start_result_imports_cleanly(import_flow_fn):
    dialog_text = import_flow_fn(pathlib.Path(__file__).parent / "activity_start_result.flo")

    assert "Failed to read flow" not in dialog_text, (
        f"Automate rejected activity_start_result.flo:\n{dialog_text}"
    )
    assert "flow?" in dialog_text.lower(), (
        f"Expected an 'Import \"...\" flow?' confirmation dialog, got:\n{dialog_text}"
    )

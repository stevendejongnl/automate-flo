import pathlib

from automate_flo import FlowBeginning, LogAppend, write_flow


def test_log_append_byte_exact():
    begin = FlowBeginning(stmt_id=1, cell_x=0, cell_y=0, title="")
    la = LogAppend(stmt_id=2, message="hello from automate-flo", cell_x=0, cell_y=6)
    begin.on_complete = la

    data = write_flow([begin, la], next_id=2)
    assert data == (pathlib.Path(__file__).parent / "log_append.flo").read_bytes()


def test_log_append_imports_cleanly(import_flow_fn):
    dialog_text = import_flow_fn(pathlib.Path(__file__).parent / "log_append.flo")

    assert "Failed to read flow" not in dialog_text, (
        f"Automate rejected log_append.flo:\n{dialog_text}"
    )
    assert "flow?" in dialog_text.lower(), (
        f"Expected an 'Import \"...\" flow?' confirmation dialog, got:\n{dialog_text}"
    )

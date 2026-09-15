import pathlib

from automate_flo import FlowBeginning, ToastShow, write_flow


def test_toast_show_byte_exact():
    begin = FlowBeginning(stmt_id=1, cell_x=0, cell_y=0, title="")
    toast = ToastShow(stmt_id=2, message="hello from automate-flo", cell_x=0, cell_y=6)
    begin.on_complete = toast

    data = write_flow([begin, toast], next_id=2)
    assert data == (pathlib.Path(__file__).parent / "toast_show.flo").read_bytes()


def test_toast_show_imports_cleanly(import_flow_fn):
    dialog_text = import_flow_fn(pathlib.Path(__file__).parent / "toast_show.flo")

    assert "Failed to read flow" not in dialog_text, (
        f"Automate rejected toast_show.flo:\n{dialog_text}"
    )
    assert "flow?" in dialog_text.lower(), (
        f"Expected an 'Import \"...\" flow?' confirmation dialog, got:\n{dialog_text}"
    )

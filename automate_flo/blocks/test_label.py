import pathlib

from automate_flo import FlowBeginning, Label, StringExpr, write_flow


def test_label_byte_exact():
    begin = FlowBeginning(stmt_id=1, cell_x=0, cell_y=0, title="")
    lbl = Label(stmt_id=2, value=StringExpr("myLabel"), cell_x=0, cell_y=6)
    begin.on_complete = lbl

    data = write_flow([begin, lbl], next_id=2)
    assert data == (pathlib.Path(__file__).parent / "label.flo").read_bytes()


def test_label_imports_cleanly(import_flow_fn):
    dialog_text = import_flow_fn(pathlib.Path(__file__).parent / "label.flo")

    assert "Failed to read flow" not in dialog_text, (
        f"Automate rejected label.flo:\n{dialog_text}"
    )
    assert "flow?" in dialog_text.lower(), (
        f"Expected an 'Import \"...\" flow?' confirmation dialog, got:\n{dialog_text}"
    )

import pathlib

from automate_flo import ClipboardGet, FlowBeginning, VariableExpr, write_flow


def test_clipboard_get_byte_exact():
    begin = FlowBeginning(stmt_id=1, cell_x=0, cell_y=0, title="")
    cg = ClipboardGet(stmt_id=2, var_content=VariableExpr("clip"), cell_x=0, cell_y=6)
    begin.on_complete = cg

    data = write_flow([begin, cg], next_id=2)
    assert data == (pathlib.Path(__file__).parent / "clipboard_get.flo").read_bytes()


def test_clipboard_get_imports_cleanly(import_flow_fn):
    dialog_text = import_flow_fn(pathlib.Path(__file__).parent / "clipboard_get.flo")

    assert "Failed to read flow" not in dialog_text, (
        f"Automate rejected clipboard_get.flo:\n{dialog_text}"
    )
    assert "flow?" in dialog_text.lower(), (
        f"Expected an 'Import \"...\" flow?' confirmation dialog, got:\n{dialog_text}"
    )

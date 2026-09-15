import pathlib

from automate_flo import ArrayRemove, FlowBeginning, VariableExpr, write_flow


def test_array_remove_byte_exact():
    begin = FlowBeginning(stmt_id=1, cell_x=0, cell_y=0, title="")
    ar = ArrayRemove(stmt_id=2, cell_x=0, cell_y=6, var_array=VariableExpr("arr"), index=0,
                      var_old_value=VariableExpr("old"))
    begin.on_complete = ar

    data = write_flow([begin, ar], next_id=2)
    assert data == (pathlib.Path(__file__).parent / "array_remove.flo").read_bytes()


def test_array_remove_imports_cleanly(import_flow_fn):
    dialog_text = import_flow_fn(pathlib.Path(__file__).parent / "array_remove.flo")

    assert "Failed to read flow" not in dialog_text, (
        f"Automate rejected array_remove.flo:\n{dialog_text}"
    )
    assert "flow?" in dialog_text.lower(), (
        f"Expected an 'Import \"...\" flow?' confirmation dialog, got:\n{dialog_text}"
    )

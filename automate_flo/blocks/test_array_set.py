import pathlib

from automate_flo import ArraySet, FlowBeginning, VariableExpr, write_flow


def test_array_set_byte_exact():
    begin = FlowBeginning(stmt_id=1, cell_x=0, cell_y=0, title="")
    as_ = ArraySet(stmt_id=2, cell_x=0, cell_y=6, var_array=VariableExpr("arr"), index=0, value="hello")
    begin.on_complete = as_

    data = write_flow([begin, as_], next_id=2)
    assert data == (pathlib.Path(__file__).parent / "array_set.flo").read_bytes()


def test_array_set_imports_cleanly(import_flow_fn):
    dialog_text = import_flow_fn(pathlib.Path(__file__).parent / "array_set.flo")

    assert "Failed to read flow" not in dialog_text, (
        f"Automate rejected array_set.flo:\n{dialog_text}"
    )
    assert "flow?" in dialog_text.lower(), (
        f"Expected an 'Import \"...\" flow?' confirmation dialog, got:\n{dialog_text}"
    )

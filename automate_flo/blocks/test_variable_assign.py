import pathlib

from automate_flo import FlowBeginning, VariableAssign, write_flow


def test_variable_assign_byte_exact():
    begin = FlowBeginning(stmt_id=1, cell_x=0, cell_y=0, title="")
    va = VariableAssign(stmt_id=2, variable_name="myVar", value="hello", cell_x=0, cell_y=6)
    begin.on_complete = va

    data = write_flow([begin, va], next_id=2)
    assert data == (pathlib.Path(__file__).parent / "variable_assign.flo").read_bytes()


def test_variable_assign_imports_cleanly(import_flow_fn):
    dialog_text = import_flow_fn(pathlib.Path(__file__).parent / "variable_assign.flo")

    assert "Failed to read flow" not in dialog_text, (
        f"Automate rejected variable_assign.flo:\n{dialog_text}"
    )
    assert "flow?" in dialog_text.lower(), (
        f"Expected an 'Import \"...\" flow?' confirmation dialog, got:\n{dialog_text}"
    )

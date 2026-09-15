import pathlib

from automate_flo import AtomicAdd, FlowBeginning, VariableExpr, write_flow


def test_atomic_add_byte_exact():
    begin = FlowBeginning(stmt_id=1, cell_x=0, cell_y=0, title="")
    aa = AtomicAdd(stmt_id=2, cell_x=0, cell_y=6, var_atomic=VariableExpr("counter"), delta=1)
    begin.on_complete = aa

    data = write_flow([begin, aa], next_id=2)
    assert data == (pathlib.Path(__file__).parent / "atomic_add.flo").read_bytes()


def test_atomic_add_imports_cleanly(import_flow_fn):
    dialog_text = import_flow_fn(pathlib.Path(__file__).parent / "atomic_add.flo")

    assert "Failed to read flow" not in dialog_text, (
        f"Automate rejected atomic_add.flo:\n{dialog_text}"
    )
    assert "flow?" in dialog_text.lower(), (
        f"Expected an 'Import \"...\" flow?' confirmation dialog, got:\n{dialog_text}"
    )

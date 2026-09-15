import pathlib

from automate_flo import ExpressionDecision, FlowBeginning, StringExpr, write_flow


def test_expression_decision_byte_exact():
    begin = FlowBeginning(stmt_id=1, cell_x=0, cell_y=0, title="")
    ed = ExpressionDecision(stmt_id=2, expression=StringExpr("true"), cell_x=0, cell_y=6)
    begin.on_complete = ed

    data = write_flow([begin, ed], next_id=2)
    assert data == (pathlib.Path(__file__).parent / "expression_decision.flo").read_bytes()


def test_expression_decision_imports_cleanly(import_flow_fn):
    dialog_text = import_flow_fn(pathlib.Path(__file__).parent / "expression_decision.flo")

    assert "Failed to read flow" not in dialog_text, (
        f"Automate rejected expression_decision.flo:\n{dialog_text}"
    )
    assert "flow?" in dialog_text.lower(), (
        f"Expected an 'Import \"...\" flow?' confirmation dialog, got:\n{dialog_text}"
    )

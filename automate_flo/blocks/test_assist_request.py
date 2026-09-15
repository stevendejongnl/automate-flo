import pathlib

from automate_flo import AssistRequest, FlowBeginning, VariableExpr, write_flow


def test_assist_request_byte_exact():
    begin = FlowBeginning(stmt_id=1, cell_x=0, cell_y=0, title="")
    ar = AssistRequest(stmt_id=2, cell_x=0, cell_y=6, title="Assist",
                        var_package_name=VariableExpr("pkg"), var_activity_class_name=VariableExpr("cls"),
                        var_intent_action=VariableExpr("act"), var_intent_categories=VariableExpr("cat"),
                        var_intent_uri=VariableExpr("uri"), var_intent_mime_type=VariableExpr("mime"),
                        var_intent_extras=VariableExpr("extras"), var_web_uri=VariableExpr("web"))
    begin.on_complete = ar

    data = write_flow([begin, ar], next_id=2)
    assert data == (pathlib.Path(__file__).parent / "assist_request.flo").read_bytes()


def test_assist_request_imports_cleanly(import_flow_fn):
    dialog_text = import_flow_fn(pathlib.Path(__file__).parent / "assist_request.flo")

    assert "Failed to read flow" not in dialog_text, (
        f"Automate rejected assist_request.flo:\n{dialog_text}"
    )
    assert "flow?" in dialog_text.lower(), (
        f"Expected an 'Import \"...\" flow?' confirmation dialog, got:\n{dialog_text}"
    )

import pathlib

from automate_flo import AppWidgetConfigure, FlowBeginning, VariableExpr, write_flow


def test_app_widget_configure_byte_exact():
    begin = FlowBeginning(stmt_id=1, cell_x=0, cell_y=0, title="")
    awc = AppWidgetConfigure(stmt_id=2, cell_x=0, cell_y=6, title="Configure",
                              var_interface_uri=VariableExpr("uri"), var_host_category=VariableExpr("cat"))
    begin.on_complete = awc

    data = write_flow([begin, awc], next_id=2)
    assert data == (pathlib.Path(__file__).parent / "app_widget_configure.flo").read_bytes()


def test_app_widget_configure_imports_cleanly(import_flow_fn):
    dialog_text = import_flow_fn(pathlib.Path(__file__).parent / "app_widget_configure.flo")

    assert "Failed to read flow" not in dialog_text, (
        f"Automate rejected app_widget_configure.flo:\n{dialog_text}"
    )
    assert "flow?" in dialog_text.lower(), (
        f"Expected an 'Import \"...\" flow?' confirmation dialog, got:\n{dialog_text}"
    )

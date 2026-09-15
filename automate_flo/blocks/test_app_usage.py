import pathlib

from automate_flo import AppUsage, FlowBeginning, VariableExpr, write_flow

PKG = "com.example.targetapp"


def test_app_usage_byte_exact():
    begin = FlowBeginning(stmt_id=1, cell_x=0, cell_y=0, title="")
    au = AppUsage(stmt_id=2, cell_x=0, cell_y=6, package_name=PKG,
                  var_usage_duration=VariableExpr("dur"), var_last_used_timestamp=VariableExpr("last"),
                  var_stats_start_timestamp=VariableExpr("start"), var_stats_end_timestamp=VariableExpr("end"))
    begin.on_complete = au

    data = write_flow([begin, au], next_id=2)
    assert data == (pathlib.Path(__file__).parent / "app_usage.flo").read_bytes()


def test_app_usage_imports_cleanly(import_flow_fn):
    dialog_text = import_flow_fn(pathlib.Path(__file__).parent / "app_usage.flo")

    assert "Failed to read flow" not in dialog_text, (
        f"Automate rejected app_usage.flo:\n{dialog_text}"
    )
    assert "flow?" in dialog_text.lower(), (
        f"Expected an 'Import \"...\" flow?' confirmation dialog, got:\n{dialog_text}"
    )

import pathlib

from automate_flo import AppInstalled, FlowBeginning, VariableExpr, write_flow

PKG = "com.example.targetapp"


def test_app_installed_byte_exact():
    begin = FlowBeginning(stmt_id=1, cell_x=0, cell_y=0, title="")
    ai = AppInstalled(stmt_id=2, cell_x=0, cell_y=6, package_name=PKG,
                       var_package_name=VariableExpr("pkg"), var_display_name=VariableExpr("name"),
                       var_version_code=VariableExpr("vcode"), var_version_name=VariableExpr("vname"),
                       var_cache_size=VariableExpr("cache"), var_data_size=VariableExpr("data"),
                       var_code_size=VariableExpr("code"), var_source_dirs=VariableExpr("dirs"))
    begin.on_complete = ai

    data = write_flow([begin, ai], next_id=2)
    assert data == (pathlib.Path(__file__).parent / "app_installed.flo").read_bytes()


def test_app_installed_imports_cleanly(import_flow_fn):
    dialog_text = import_flow_fn(pathlib.Path(__file__).parent / "app_installed.flo")

    assert "Failed to read flow" not in dialog_text, (
        f"Automate rejected app_installed.flo:\n{dialog_text}"
    )
    assert "flow?" in dialog_text.lower(), (
        f"Expected an 'Import \"...\" flow?' confirmation dialog, got:\n{dialog_text}"
    )

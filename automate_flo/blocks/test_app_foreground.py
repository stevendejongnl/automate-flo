import pathlib

from automate_flo import AppForeground, FlowBeginning, VariableExpr, write_flow

PKG = "com.example.targetapp"


def test_app_foreground_byte_exact():
    begin = FlowBeginning(stmt_id=1, cell_x=0, cell_y=0, title="")
    af = AppForeground(stmt_id=2, cell_x=0, cell_y=6, package_name=PKG,
                        class_name=PKG + ".MainActivity",
                        var_foreground_package_name=VariableExpr("fgPkg"),
                        var_foreground_class_name=VariableExpr("fgCls"))
    begin.on_complete = af

    data = write_flow([begin, af], next_id=2)
    assert data == (pathlib.Path(__file__).parent / "app_foreground.flo").read_bytes()


def test_app_foreground_imports_cleanly(import_flow_fn):
    dialog_text = import_flow_fn(pathlib.Path(__file__).parent / "app_foreground.flo")

    assert "Failed to read flow" not in dialog_text, (
        f"Automate rejected app_foreground.flo:\n{dialog_text}"
    )
    assert "flow?" in dialog_text.lower(), (
        f"Expected an 'Import \"...\" flow?' confirmation dialog, got:\n{dialog_text}"
    )

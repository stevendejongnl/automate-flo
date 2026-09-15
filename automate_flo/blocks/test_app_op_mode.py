import pathlib

from automate_flo import AppOpMode, FlowBeginning, VariableExpr, write_flow

PKG = "com.example.targetapp"


def test_app_op_mode_byte_exact():
    begin = FlowBeginning(stmt_id=1, cell_x=0, cell_y=0, title="")
    aom = AppOpMode(stmt_id=2, cell_x=0, cell_y=6, package_name=PKG, opstr="android:fine_location",
                     mode=1, var_current_mode=VariableExpr("cur"))
    begin.on_complete = aom

    data = write_flow([begin, aom], next_id=2)
    assert data == (pathlib.Path(__file__).parent / "app_op_mode.flo").read_bytes()


def test_app_op_mode_imports_cleanly(import_flow_fn):
    dialog_text = import_flow_fn(pathlib.Path(__file__).parent / "app_op_mode.flo")

    assert "Failed to read flow" not in dialog_text, (
        f"Automate rejected app_op_mode.flo:\n{dialog_text}"
    )
    assert "flow?" in dialog_text.lower(), (
        f"Expected an 'Import \"...\" flow?' confirmation dialog, got:\n{dialog_text}"
    )

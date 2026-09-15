import pathlib

from automate_flo import AppNotificationsVisibilityGet, FlowBeginning, VariableExpr, write_flow

PKG = "com.example.targetapp"


def test_app_notifications_visibility_get_byte_exact():
    begin = FlowBeginning(stmt_id=1, cell_x=0, cell_y=0, title="")
    avg = AppNotificationsVisibilityGet(stmt_id=2, cell_x=0, cell_y=6, package_name=PKG,
                                         var_visibility=VariableExpr("vis"))
    begin.on_complete = avg

    data = write_flow([begin, avg], next_id=2)
    assert data == (pathlib.Path(__file__).parent / "app_notifications_visibility_get.flo").read_bytes()


def test_app_notifications_visibility_get_imports_cleanly(import_flow_fn):
    dialog_text = import_flow_fn(pathlib.Path(__file__).parent / "app_notifications_visibility_get.flo")

    assert "Failed to read flow" not in dialog_text, (
        f"Automate rejected app_notifications_visibility_get.flo:\n{dialog_text}"
    )
    assert "flow?" in dialog_text.lower(), (
        f"Expected an 'Import \"...\" flow?' confirmation dialog, got:\n{dialog_text}"
    )

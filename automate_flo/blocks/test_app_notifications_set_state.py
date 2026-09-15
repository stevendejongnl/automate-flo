import pathlib

from automate_flo import AppNotificationsSetState, FlowBeginning, write_flow

PKG = "com.example.targetapp"


def test_app_notifications_set_state_byte_exact():
    begin = FlowBeginning(stmt_id=1, cell_x=0, cell_y=0, title="")
    ass_ = AppNotificationsSetState(stmt_id=2, cell_x=0, cell_y=6, package_name=PKG, state=True)
    begin.on_complete = ass_

    data = write_flow([begin, ass_], next_id=2)
    assert data == (pathlib.Path(__file__).parent / "app_notifications_set_state.flo").read_bytes()


def test_app_notifications_set_state_imports_cleanly(import_flow_fn):
    dialog_text = import_flow_fn(pathlib.Path(__file__).parent / "app_notifications_set_state.flo")

    assert "Failed to read flow" not in dialog_text, (
        f"Automate rejected app_notifications_set_state.flo:\n{dialog_text}"
    )
    assert "flow?" in dialog_text.lower(), (
        f"Expected an 'Import \"...\" flow?' confirmation dialog, got:\n{dialog_text}"
    )

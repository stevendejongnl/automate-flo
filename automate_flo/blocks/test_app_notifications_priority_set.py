import pathlib

from automate_flo import AppNotificationsPrioritySet, FlowBeginning, write_flow

PKG = "com.example.targetapp"


def test_app_notifications_priority_set_byte_exact():
    begin = FlowBeginning(stmt_id=1, cell_x=0, cell_y=0, title="")
    aps = AppNotificationsPrioritySet(stmt_id=2, cell_x=0, cell_y=6, package_name=PKG, priority=2)
    begin.on_complete = aps

    data = write_flow([begin, aps], next_id=2)
    assert data == (pathlib.Path(__file__).parent / "app_notifications_priority_set.flo").read_bytes()


def test_app_notifications_priority_set_imports_cleanly(import_flow_fn):
    dialog_text = import_flow_fn(pathlib.Path(__file__).parent / "app_notifications_priority_set.flo")

    assert "Failed to read flow" not in dialog_text, (
        f"Automate rejected app_notifications_priority_set.flo:\n{dialog_text}"
    )
    assert "flow?" in dialog_text.lower(), (
        f"Expected an 'Import \"...\" flow?' confirmation dialog, got:\n{dialog_text}"
    )

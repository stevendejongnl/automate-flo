import pathlib

from automate_flo import FlowBeginning, NotificationShow, write_flow


def test_notification_show_byte_exact():
    begin = FlowBeginning(stmt_id=1, cell_x=0, cell_y=0, title="")
    ns = NotificationShow(stmt_id=2, title="Hi", message="World", cell_x=0, cell_y=6)
    begin.on_complete = ns

    data = write_flow([begin, ns], next_id=2)
    assert data == (pathlib.Path(__file__).parent / "notification_show.flo").read_bytes()


def test_notification_show_imports_cleanly(import_flow_fn):
    dialog_text = import_flow_fn(pathlib.Path(__file__).parent / "notification_show.flo")

    assert "Failed to read flow" not in dialog_text, (
        f"Automate rejected notification_show.flo:\n{dialog_text}"
    )
    assert "flow?" in dialog_text.lower(), (
        f"Expected an 'Import \"...\" flow?' confirmation dialog, got:\n{dialog_text}"
    )

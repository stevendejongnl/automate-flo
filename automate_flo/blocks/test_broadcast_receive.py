import pathlib

from automate_flo import BroadcastReceive, FlowBeginning, write_flow


def test_broadcast_receive_byte_exact():
    begin = FlowBeginning(stmt_id=1, cell_x=0, cell_y=0, title="")
    b = BroadcastReceive(stmt_id=2, action="android.intent.action.BOOT_COMPLETED", cell_x=0, cell_y=6)
    begin.on_complete = b

    data = write_flow([begin, b], next_id=2)
    assert data == (pathlib.Path(__file__).parent / "broadcast_receive.flo").read_bytes()


def test_broadcast_receive_imports_cleanly(import_flow_fn):
    dialog_text = import_flow_fn(pathlib.Path(__file__).parent / "broadcast_receive.flo")

    assert "Failed to read flow" not in dialog_text, (
        f"Automate rejected broadcast_receive.flo:\n{dialog_text}"
    )
    assert "flow?" in dialog_text.lower(), (
        f"Expected an 'Import \"...\" flow?' confirmation dialog, got:\n{dialog_text}"
    )

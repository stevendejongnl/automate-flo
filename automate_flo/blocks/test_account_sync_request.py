import pathlib

from automate_flo import AccountSyncRequest, FlowBeginning, write_flow


def test_account_sync_request_byte_exact():
    begin = FlowBeginning(stmt_id=1, cell_x=0, cell_y=0, title="")
    asr = AccountSyncRequest(stmt_id=2, cell_x=0, cell_y=6)
    begin.on_complete = asr

    data = write_flow([begin, asr], next_id=2)
    assert data == (pathlib.Path(__file__).parent / "account_sync_request.flo").read_bytes()


def test_account_sync_request_imports_cleanly(import_flow_fn):
    dialog_text = import_flow_fn(pathlib.Path(__file__).parent / "account_sync_request.flo")

    assert "Failed to read flow" not in dialog_text, (
        f"Automate rejected account_sync_request.flo:\n{dialog_text}"
    )
    assert "flow?" in dialog_text.lower(), (
        f"Expected an 'Import \"...\" flow?' confirmation dialog, got:\n{dialog_text}"
    )

import pathlib

from automate_flo import FlowBeginning, SmsSend, write_flow


def test_sms_send_byte_exact():
    begin = FlowBeginning(stmt_id=1, cell_x=0, cell_y=0, title="")
    # +1-555-0100..0199 is reserved by NANP for fictional use.
    sms = SmsSend(stmt_id=2, phone_number="+15555550123", message="test", cell_x=0, cell_y=6)
    begin.on_complete = sms

    data = write_flow([begin, sms], next_id=2)
    assert data == (pathlib.Path(__file__).parent / "sms_send.flo").read_bytes()


def test_sms_send_imports_cleanly(import_flow_fn):
    dialog_text = import_flow_fn(pathlib.Path(__file__).parent / "sms_send.flo")

    assert "Failed to read flow" not in dialog_text, (
        f"Automate rejected sms_send.flo:\n{dialog_text}"
    )
    assert "flow?" in dialog_text.lower(), (
        f"Expected an 'Import \"...\" flow?' confirmation dialog, got:\n{dialog_text}"
    )

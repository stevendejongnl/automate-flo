import pathlib

from automate_flo import DialNumber, FlowBeginning, write_flow


def test_dial_number_byte_exact():
    begin = FlowBeginning(stmt_id=1, cell_x=0, cell_y=0, title="")
    b = DialNumber(stmt_id=2, phone_number="+15551234567", cell_x=0, cell_y=6)
    begin.on_complete = b

    data = write_flow([begin, b], next_id=2)
    assert data == (pathlib.Path(__file__).parent / "dial_number.flo").read_bytes()


def test_dial_number_imports_cleanly(import_flow_fn):
    dialog_text = import_flow_fn(pathlib.Path(__file__).parent / "dial_number.flo")

    assert "Failed to read flow" not in dialog_text, (
        f"Automate rejected dial_number.flo:\n{dialog_text}"
    )
    assert "flow?" in dialog_text.lower(), (
        f"Expected an 'Import \"...\" flow?' confirmation dialog, got:\n{dialog_text}"
    )

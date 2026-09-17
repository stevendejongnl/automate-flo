import pathlib

from automate_flo import RingtoneGet, FlowBeginning, write_flow


def test_ringtone_get_byte_exact():
    begin = FlowBeginning(stmt_id=1, cell_x=0, cell_y=0, title="")
    b = RingtoneGet(stmt_id=2, cell_x=0, cell_y=6)
    begin.on_complete = b

    data = write_flow([begin, b], next_id=2)
    assert data == (pathlib.Path(__file__).parent / "ringtone_get.flo").read_bytes()


def test_ringtone_get_imports_cleanly(import_flow_fn):
    dialog_text = import_flow_fn(pathlib.Path(__file__).parent / "ringtone_get.flo")

    assert "Failed to read flow" not in dialog_text, (
        f"Automate rejected ringtone_get.flo:\n{dialog_text}"
    )
    assert "flow?" in dialog_text.lower(), (
        f"Expected an 'Import \"...\" flow?' confirmation dialog, got:\n{dialog_text}"
    )

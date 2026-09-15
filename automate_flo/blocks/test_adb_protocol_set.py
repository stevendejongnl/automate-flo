import pathlib

from automate_flo import AdbProtocolSet, FlowBeginning, write_flow


def test_adb_protocol_set_byte_exact():
    begin = FlowBeginning(stmt_id=1, cell_x=0, cell_y=0, title="")
    aps = AdbProtocolSet(stmt_id=2, cell_x=0, cell_y=6)
    begin.on_complete = aps

    data = write_flow([begin, aps], next_id=2)
    assert data == (pathlib.Path(__file__).parent / "adb_protocol_set.flo").read_bytes()


def test_adb_protocol_set_imports_cleanly(import_flow_fn):
    dialog_text = import_flow_fn(pathlib.Path(__file__).parent / "adb_protocol_set.flo")

    assert "Failed to read flow" not in dialog_text, (
        f"Automate rejected adb_protocol_set.flo:\n{dialog_text}"
    )
    assert "flow?" in dialog_text.lower(), (
        f"Expected an 'Import \"...\" flow?' confirmation dialog, got:\n{dialog_text}"
    )

import pathlib

from automate_flo import ContactPick, FlowBeginning, write_flow


def test_contact_pick_byte_exact():
    begin = FlowBeginning(stmt_id=1, cell_x=0, cell_y=0, title="")
    b = ContactPick(stmt_id=2, cell_x=0, cell_y=6)
    begin.on_complete = b

    data = write_flow([begin, b], next_id=2)
    assert data == (pathlib.Path(__file__).parent / "contact_pick.flo").read_bytes()


def test_contact_pick_imports_cleanly(import_flow_fn):
    dialog_text = import_flow_fn(pathlib.Path(__file__).parent / "contact_pick.flo")

    assert "Failed to read flow" not in dialog_text, (
        f"Automate rejected contact_pick.flo:\n{dialog_text}"
    )
    assert "flow?" in dialog_text.lower(), (
        f"Expected an 'Import \"...\" flow?' confirmation dialog, got:\n{dialog_text}"
    )

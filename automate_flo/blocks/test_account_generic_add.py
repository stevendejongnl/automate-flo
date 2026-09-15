import pathlib

from automate_flo import AccountGenericAdd, FlowBeginning, write_flow


def test_account_generic_add_byte_exact():
    begin = FlowBeginning(stmt_id=1, cell_x=0, cell_y=0, title="")
    aga = AccountGenericAdd(stmt_id=2, account_name="myaccount", username="bob",
                             password="hunter2", cell_x=0, cell_y=6)
    begin.on_complete = aga

    data = write_flow([begin, aga], next_id=2)
    assert data == (pathlib.Path(__file__).parent / "account_generic_add.flo").read_bytes()


def test_account_generic_add_imports_cleanly(import_flow_fn):
    dialog_text = import_flow_fn(pathlib.Path(__file__).parent / "account_generic_add.flo")

    assert "Failed to read flow" not in dialog_text, (
        f"Automate rejected account_generic_add.flo:\n{dialog_text}"
    )
    assert "flow?" in dialog_text.lower(), (
        f"Expected an 'Import \"...\" flow?' confirmation dialog, got:\n{dialog_text}"
    )

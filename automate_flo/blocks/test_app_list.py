import pathlib

from automate_flo import AppList, FlowBeginning, VariableExpr, write_flow


def test_app_list_byte_exact():
    begin = FlowBeginning(stmt_id=1, cell_x=0, cell_y=0, title="")
    al = AppList(stmt_id=2, cell_x=0, cell_y=6, flags_include=1, flags_exclude=2,
                 states=3, categories=-1, var_package_names=VariableExpr("pkgs"),
                 var_display_names=VariableExpr("names"))
    begin.on_complete = al

    data = write_flow([begin, al], next_id=2)
    assert data == (pathlib.Path(__file__).parent / "app_list.flo").read_bytes()


def test_app_list_imports_cleanly(import_flow_fn):
    dialog_text = import_flow_fn(pathlib.Path(__file__).parent / "app_list.flo")

    assert "Failed to read flow" not in dialog_text, (
        f"Automate rejected app_list.flo:\n{dialog_text}"
    )
    assert "flow?" in dialog_text.lower(), (
        f"Expected an 'Import \"...\" flow?' confirmation dialog, got:\n{dialog_text}"
    )

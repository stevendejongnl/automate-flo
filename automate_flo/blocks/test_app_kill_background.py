import pathlib

from automate_flo import AppKillBackground, FlowBeginning, write_flow

PKG = "com.example.targetapp"


def test_app_kill_background_byte_exact():
    begin = FlowBeginning(stmt_id=1, cell_x=0, cell_y=0, title="")
    akb = AppKillBackground(stmt_id=2, cell_x=0, cell_y=6, package_name=PKG)
    begin.on_complete = akb

    data = write_flow([begin, akb], next_id=2)
    assert data == (pathlib.Path(__file__).parent / "app_kill_background.flo").read_bytes()


def test_app_kill_background_imports_cleanly(import_flow_fn):
    dialog_text = import_flow_fn(pathlib.Path(__file__).parent / "app_kill_background.flo")

    assert "Failed to read flow" not in dialog_text, (
        f"Automate rejected app_kill_background.flo:\n{dialog_text}"
    )
    assert "flow?" in dialog_text.lower(), (
        f"Expected an 'Import \"...\" flow?' confirmation dialog, got:\n{dialog_text}"
    )

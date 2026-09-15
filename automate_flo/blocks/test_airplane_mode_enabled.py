import pathlib

from automate_flo import AirplaneModeEnabled, FlowBeginning, write_flow


def test_airplane_mode_enabled_byte_exact():
    begin = FlowBeginning(stmt_id=1, cell_x=0, cell_y=0, title="")
    ame = AirplaneModeEnabled(stmt_id=2, cell_x=0, cell_y=6)
    begin.on_complete = ame

    data = write_flow([begin, ame], next_id=2)
    assert data == (pathlib.Path(__file__).parent / "airplane_mode_enabled.flo").read_bytes()


def test_airplane_mode_enabled_imports_cleanly(import_flow_fn):
    dialog_text = import_flow_fn(pathlib.Path(__file__).parent / "airplane_mode_enabled.flo")

    assert "Failed to read flow" not in dialog_text, (
        f"Automate rejected airplane_mode_enabled.flo:\n{dialog_text}"
    )
    assert "flow?" in dialog_text.lower(), (
        f"Expected an 'Import \"...\" flow?' confirmation dialog, got:\n{dialog_text}"
    )

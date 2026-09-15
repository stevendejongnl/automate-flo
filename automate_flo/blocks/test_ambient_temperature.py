import pathlib

from automate_flo import AmbientTemperature, FlowBeginning, write_flow


def test_ambient_temperature_byte_exact():
    begin = FlowBeginning(stmt_id=1, cell_x=0, cell_y=0, title="")
    at = AmbientTemperature(stmt_id=2, cell_x=0, cell_y=6)
    begin.on_complete = at

    data = write_flow([begin, at], next_id=2)
    assert data == (pathlib.Path(__file__).parent / "ambient_temperature.flo").read_bytes()


def test_ambient_temperature_imports_cleanly(import_flow_fn):
    dialog_text = import_flow_fn(pathlib.Path(__file__).parent / "ambient_temperature.flo")

    assert "Failed to read flow" not in dialog_text, (
        f"Automate rejected ambient_temperature.flo:\n{dialog_text}"
    )
    assert "flow?" in dialog_text.lower(), (
        f"Expected an 'Import \"...\" flow?' confirmation dialog, got:\n{dialog_text}"
    )

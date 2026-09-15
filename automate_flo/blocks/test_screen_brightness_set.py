import pathlib

from automate_flo import FlowBeginning, ScreenBrightnessSet, write_flow


def test_screen_brightness_set_byte_exact():
    begin = FlowBeginning(stmt_id=1, cell_x=0, cell_y=0, title="")
    sbs = ScreenBrightnessSet(stmt_id=2, level=50.0, cell_x=0, cell_y=6)
    begin.on_complete = sbs

    data = write_flow([begin, sbs], next_id=2)
    assert data == (pathlib.Path(__file__).parent / "screen_brightness_set.flo").read_bytes()


def test_screen_brightness_set_imports_cleanly(import_flow_fn):
    dialog_text = import_flow_fn(pathlib.Path(__file__).parent / "screen_brightness_set.flo")

    assert "Failed to read flow" not in dialog_text, (
        f"Automate rejected screen_brightness_set.flo:\n{dialog_text}"
    )
    assert "flow?" in dialog_text.lower(), (
        f"Expected an 'Import \"...\" flow?' confirmation dialog, got:\n{dialog_text}"
    )

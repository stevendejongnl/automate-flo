import pathlib

from automate_flo import FlowBeginning, ScreenBrightness, write_flow


def test_screen_brightness_byte_exact():
    begin = FlowBeginning(stmt_id=1, cell_x=0, cell_y=0, title="")
    sb = ScreenBrightness(stmt_id=2, cell_x=0, cell_y=6)
    begin.on_complete = sb

    data = write_flow([begin, sb], next_id=2)
    assert data == (pathlib.Path(__file__).parent / "screen_brightness.flo").read_bytes()


def test_screen_brightness_imports_cleanly(import_flow_fn):
    dialog_text = import_flow_fn(pathlib.Path(__file__).parent / "screen_brightness.flo")

    assert "Failed to read flow" not in dialog_text, (
        f"Automate rejected screen_brightness.flo:\n{dialog_text}"
    )
    assert "flow?" in dialog_text.lower(), (
        f"Expected an 'Import \"...\" flow?' confirmation dialog, got:\n{dialog_text}"
    )

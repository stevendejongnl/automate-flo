import pathlib

from automate_flo import AccessibilityButton, FlowBeginning, write_flow


def test_accessibility_button_byte_exact():
    begin = FlowBeginning(stmt_id=1, cell_x=0, cell_y=0, title="")
    ab = AccessibilityButton(stmt_id=2, cell_x=0, cell_y=6)
    begin.on_complete = ab

    data = write_flow([begin, ab], next_id=2)
    assert data == (pathlib.Path(__file__).parent / "accessibility_button.flo").read_bytes()


def test_accessibility_button_imports_cleanly(import_flow_fn):
    dialog_text = import_flow_fn(pathlib.Path(__file__).parent / "accessibility_button.flo")

    assert "Failed to read flow" not in dialog_text, (
        f"Automate rejected accessibility_button.flo:\n{dialog_text}"
    )
    assert "flow?" in dialog_text.lower(), (
        f"Expected an 'Import \"...\" flow?' confirmation dialog, got:\n{dialog_text}"
    )

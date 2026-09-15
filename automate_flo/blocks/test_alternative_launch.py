import pathlib

from automate_flo import AlternativeLaunch, FlowBeginning, write_flow


def test_alternative_launch_byte_exact():
    begin = FlowBeginning(stmt_id=1, cell_x=0, cell_y=0, title="")
    al = AlternativeLaunch(stmt_id=2, cell_x=0, cell_y=6, title="My App")
    begin.on_complete = al

    data = write_flow([begin, al], next_id=2)
    assert data == (pathlib.Path(__file__).parent / "alternative_launch.flo").read_bytes()


def test_alternative_launch_imports_cleanly(import_flow_fn):
    dialog_text = import_flow_fn(pathlib.Path(__file__).parent / "alternative_launch.flo")

    assert "Failed to read flow" not in dialog_text, (
        f"Automate rejected alternative_launch.flo:\n{dialog_text}"
    )
    assert "flow?" in dialog_text.lower(), (
        f"Expected an 'Import \"...\" flow?' confirmation dialog, got:\n{dialog_text}"
    )

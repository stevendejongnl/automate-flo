import pathlib

from automate_flo import AdbShellCommand, FlowBeginning, write_flow


def test_adb_shell_command_byte_exact():
    begin = FlowBeginning(stmt_id=1, cell_x=0, cell_y=0, title="")
    asc = AdbShellCommand(stmt_id=2, command="echo hi", cell_x=0, cell_y=6)
    begin.on_complete = asc

    data = write_flow([begin, asc], next_id=2)
    assert data == (pathlib.Path(__file__).parent / "adb_shell_command.flo").read_bytes()


def test_adb_shell_command_imports_cleanly(import_flow_fn):
    dialog_text = import_flow_fn(pathlib.Path(__file__).parent / "adb_shell_command.flo")

    assert "Failed to read flow" not in dialog_text, (
        f"Automate rejected adb_shell_command.flo:\n{dialog_text}"
    )
    assert "flow?" in dialog_text.lower(), (
        f"Expected an 'Import \"...\" flow?' confirmation dialog, got:\n{dialog_text}"
    )

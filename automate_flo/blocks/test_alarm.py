import pathlib

from automate_flo import Alarm, FlowBeginning, VariableExpr, write_flow


def test_alarm_byte_exact():
    begin = FlowBeginning(stmt_id=1, cell_x=0, cell_y=0, title="")
    a = Alarm(stmt_id=2, cell_x=0, cell_y=6,
              var_alarm_timestamp=VariableExpr("alarmTime"))
    begin.on_complete = a

    data = write_flow([begin, a], next_id=2)
    assert data == (pathlib.Path(__file__).parent / "alarm.flo").read_bytes()


def test_alarm_imports_cleanly(import_flow_fn):
    dialog_text = import_flow_fn(pathlib.Path(__file__).parent / "alarm.flo")

    assert "Failed to read flow" not in dialog_text, (
        f"Automate rejected alarm.flo:\n{dialog_text}"
    )
    assert "flow?" in dialog_text.lower(), (
        f"Expected an 'Import \"...\" flow?' confirmation dialog, got:\n{dialog_text}"
    )

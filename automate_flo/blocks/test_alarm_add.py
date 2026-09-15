import pathlib

from automate_flo import AlarmAdd, FlowBeginning, write_flow


def test_alarm_add_byte_exact():
    begin = FlowBeginning(stmt_id=1, cell_x=0, cell_y=0, title="")
    aa = AlarmAdd(stmt_id=2, cell_x=0, cell_y=6, time_of_day=28800000.0,
                  weekdays=62.0, label="Wake up",
                  sound_uri="content://media/alarm", vibrate=True)
    begin.on_complete = aa

    data = write_flow([begin, aa], next_id=2)
    assert data == (pathlib.Path(__file__).parent / "alarm_add.flo").read_bytes()


def test_alarm_add_imports_cleanly(import_flow_fn):
    dialog_text = import_flow_fn(pathlib.Path(__file__).parent / "alarm_add.flo")

    assert "Failed to read flow" not in dialog_text, (
        f"Automate rejected alarm_add.flo:\n{dialog_text}"
    )
    assert "flow?" in dialog_text.lower(), (
        f"Expected an 'Import \"...\" flow?' confirmation dialog, got:\n{dialog_text}"
    )

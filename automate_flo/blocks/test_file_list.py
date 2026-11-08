from automate_flo import (
    FlowBeginning, FileList, EnumDoubleExpr, VariableExpr, write_flow,
    parse_flow,
)


def test_file_list_round_trip():
    begin = FlowBeginning(stmt_id=1, cell_x=0, cell_y=0, title="")
    fl = FileList(stmt_id=2, path="/sdcard/AndroidApps/*.apks",
                  content_type=EnumDoubleExpr(2.0),
                  var_filenames=VariableExpr("dirs"), cell_x=0, cell_y=6)
    begin.on_complete = fl

    data = write_flow([begin, fl], next_id=2)
    parsed = parse_flow(data)["blocks"][0].on_complete
    assert isinstance(parsed, FileList)
    assert parsed.path.value == "/sdcard/AndroidApps/*.apks"
    # ContentType picker value rides the raw-double wrapper (type 101).
    assert type(parsed.content_type).__name__ == "EnumDoubleExpr"
    assert parsed.content_type.value == 2.0
    assert parsed.var_filenames.name == "dirs"

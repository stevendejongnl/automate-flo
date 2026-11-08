from automate_flo import (
    FlowBeginning, ForEach, FileDelete, VariableExpr, write_flow,
    parse_flow,
)


def test_for_each_round_trip():
    begin = FlowBeginning(stmt_id=1, cell_x=0, cell_y=0, title="")
    fd = FileDelete(stmt_id=3, path=VariableExpr("Old"), cell_x=0, cell_y=12)
    fe = ForEach(stmt_id=2, on_ok=fd, on_do=fd, container=VariableExpr("dirs"),
                 var_entry_value=VariableExpr("Old"), cell_x=0, cell_y=6)
    begin.on_complete = fe

    data = write_flow([begin, fe, fd], next_id=3)
    parsed = parse_flow(data)["blocks"][0].on_complete
    assert isinstance(parsed, ForEach)
    # OK and DO both target FileDelete through back-references.
    assert parsed.on_complete is parsed.on_do
    assert parsed.container.name == "dirs"
    assert parsed.var_entry_value.name == "Old"
    assert parsed.until is None

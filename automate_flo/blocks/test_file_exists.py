from automate_flo import (
    FlowBeginning, FileExists, IntExpr, StringExpr, VariableExpr,
    write_flow, parse_flow,
)


def test_file_exists_round_trip():
    begin = FlowBeginning(stmt_id=1, cell_x=0, cell_y=0, title="")
    fe = FileExists(stmt_id=2, path=VariableExpr("Dir"),
                    var_type=VariableExpr("type"), cell_x=0, cell_y=6)
    begin.on_complete = fe

    data = write_flow([begin, fe], next_id=2)
    parsed = parse_flow(data)["blocks"][0].on_complete
    assert isinstance(parsed, FileExists)
    assert parsed.path.name == "Dir"
    assert parsed.var_type.name == "type"
    assert parsed.var_size is None
    assert parsed.var_last_modified is None

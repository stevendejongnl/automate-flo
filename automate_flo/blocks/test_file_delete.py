from automate_flo import (
    FlowBeginning, FileDelete, VariableExpr, write_flow, parse_flow,
)


def test_file_delete_round_trip():
    begin = FlowBeginning(stmt_id=1, cell_x=0, cell_y=0, title="")
    fd = FileDelete(stmt_id=2, path=VariableExpr("Old"), recursive=True,
                    cell_x=0, cell_y=6)
    begin.on_complete = fd

    data = write_flow([begin, fd], next_id=2)
    parsed = parse_flow(data)["blocks"][0].on_complete
    assert isinstance(parsed, FileDelete)
    assert parsed.path.name == "Old"
    assert parsed.recursive.value == 1.0

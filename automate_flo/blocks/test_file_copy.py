from automate_flo import (
    FlowBeginning, FileCopy, StringExpr, write_flow, parse_flow,
)


def test_file_copy_round_trip():
    # Also a regression test for a writer bug found while round-tripping
    # real flows: temporary wrapper objects must be kept alive while
    # their identity-based dedup keys are in use, or a recycled id made
    # recursive/update resolve to an unrelated earlier object.
    begin = FlowBeginning(stmt_id=1, cell_x=0, cell_y=0, title="")
    fc = FileCopy(stmt_id=2, source_path="/a/*.apk", destination_path="/b/",
                  recursive=False, update=True, cell_x=0, cell_y=6)
    begin.on_complete = fc

    data = write_flow([begin, fc], next_id=2)
    parsed = parse_flow(data)["blocks"][0].on_complete
    assert isinstance(parsed, FileCopy)
    assert parsed.source_path.value == "/a/*.apk"
    assert parsed.destination_path.value == "/b/"
    assert type(parsed.recursive).__name__ == "DoubleExpr"
    assert parsed.recursive.value == 0.0
    assert parsed.update.value == 1.0

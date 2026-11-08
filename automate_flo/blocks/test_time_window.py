from automate_flo import (
    FlowBeginning, TimeWindow, DoubleExpr, IntExpr, write_flow, parse_flow,
)


def test_time_window_round_trip():
    begin = FlowBeginning(stmt_id=1, cell_x=0, cell_y=0, title="")
    tw = TimeWindow(stmt_id=2, continuity=IntExpr(1),
                    time_of_day=DoubleExpr(0.0),
                    duration_seconds=DoubleExpr(9000.0),
                    cell_x=0, cell_y=6)
    begin.on_complete = tw

    data = write_flow([begin, tw], next_id=2)
    parsed = parse_flow(data)["blocks"][0].on_complete
    assert isinstance(parsed, TimeWindow)
    assert parsed.continuity.value == 1
    assert parsed.time_of_day.value == 0.0
    assert parsed.duration_seconds.value == 9000.0
    assert parsed.field4 is None

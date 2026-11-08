from automate_flo import FlowBeginning, Fork, AppKill, write_flow, parse_flow


def test_fork_round_trip():
    begin = FlowBeginning(stmt_id=1, cell_x=0, cell_y=0, title="")
    kill = AppKill(stmt_id=3, package_name="com.example.x", cell_x=0, cell_y=12)
    fork = Fork(stmt_id=2, on_ok=kill, on_new=kill, cell_x=0, cell_y=6)
    begin.on_complete = fork

    data = write_flow([begin, fork, kill], next_id=3)
    parsed = parse_flow(data)["blocks"][0]
    r_fork = parsed.on_complete
    assert isinstance(r_fork, Fork)
    # OK and NEW both connect to kill; both are back-references to the
    # one shared object, so they must be the very same instance.
    assert r_fork.on_complete is r_fork.on_new
    assert r_fork.on_complete.stmt_id == 3

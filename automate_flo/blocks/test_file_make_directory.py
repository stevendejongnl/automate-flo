from automate_flo import (
    FlowBeginning, FileMakeDirectory, StringExpr, write_flow, parse_flow,
)


def test_file_make_directory_round_trip():
    begin = FlowBeginning(stmt_id=1, cell_x=0, cell_y=0, title="")
    mk = FileMakeDirectory(stmt_id=2, path="/sdcard/AndroidApps/",
                           cell_x=0, cell_y=6)
    begin.on_complete = mk

    data = write_flow([begin, mk], next_id=2)
    parsed = parse_flow(data)["blocks"][0].on_complete
    assert isinstance(parsed, FileMakeDirectory)
    assert parsed.path.value == "/sdcard/AndroidApps/"

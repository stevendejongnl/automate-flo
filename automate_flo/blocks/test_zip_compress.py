from automate_flo import (
    FlowBeginning, ZipCompress, EnumDoubleExpr, VariableExpr, write_flow,
    parse_flow,
)


def test_zip_compress_round_trip():
    begin = FlowBeginning(stmt_id=1, cell_x=0, cell_y=0, title="")
    zc = ZipCompress(stmt_id=2, destination_zip_file=VariableExpr("Dir"),
                     source_path=VariableExpr("ApkFile"),
                     destination_folder_in_zip=None, recursive=False,
                     update=True, compression_method=EnumDoubleExpr(0.0),
                     cell_x=0, cell_y=6)
    begin.on_complete = zc

    data = write_flow([begin, zc], next_id=2)
    parsed = parse_flow(data)["blocks"][0].on_complete
    assert isinstance(parsed, ZipCompress)
    assert parsed.destination_zip_file.name == "Dir"
    assert parsed.source_path.name == "ApkFile"
    assert parsed.destination_folder_in_zip is None
    assert parsed.recursive.value == 0.0
    assert parsed.update.value == 1.0
    assert parsed.compression_method.value == 0.0

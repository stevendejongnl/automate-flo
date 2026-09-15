import pathlib

from automate_flo import AndroidVersion, DoubleExpr, FlowBeginning, VariableExpr, write_flow


def test_android_version_byte_exact():
    begin = FlowBeginning(stmt_id=1, cell_x=0, cell_y=0, title="")
    av = AndroidVersion(stmt_id=2, cell_x=0, cell_y=6, min_level=DoubleExpr(21.0),
                         max_level=DoubleExpr(33.0), var_level=VariableExpr("sdk"))
    begin.on_complete = av

    data = write_flow([begin, av], next_id=2)
    assert data == (pathlib.Path(__file__).parent / "android_version.flo").read_bytes()


def test_android_version_imports_cleanly(import_flow_fn):
    dialog_text = import_flow_fn(pathlib.Path(__file__).parent / "android_version.flo")

    assert "Failed to read flow" not in dialog_text, (
        f"Automate rejected android_version.flo:\n{dialog_text}"
    )
    assert "flow?" in dialog_text.lower(), (
        f"Expected an 'Import \"...\" flow?' confirmation dialog, got:\n{dialog_text}"
    )

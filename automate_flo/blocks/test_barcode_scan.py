import pathlib

from automate_flo import BarcodeScan, FlowBeginning, VariableExpr, write_flow


def test_barcode_scan_byte_exact():
    begin = FlowBeginning(stmt_id=1, cell_x=0, cell_y=0, title="")
    b = BarcodeScan(stmt_id=2, var_raw_values=VariableExpr("rawValues"))
    b.cell_x, b.cell_y = 0, 6
    begin.on_complete = b

    data = write_flow([begin, b], next_id=2)
    assert data == (pathlib.Path(__file__).parent / "barcode_scan.flo").read_bytes()


def test_barcode_scan_imports_cleanly(import_flow_fn):
    dialog_text = import_flow_fn(pathlib.Path(__file__).parent / "barcode_scan.flo")

    assert "Failed to read flow" not in dialog_text, (
        f"Automate rejected barcode_scan.flo:\n{dialog_text}"
    )
    assert "flow?" in dialog_text.lower(), (
        f"Expected an 'Import \"...\" flow?' confirmation dialog, got:\n{dialog_text}"
    )

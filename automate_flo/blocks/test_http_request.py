import pathlib

from automate_flo import FlowBeginning, HttpRequest, write_flow


def test_http_request_byte_exact():
    begin = FlowBeginning(stmt_id=1, cell_x=0, cell_y=0, title="")
    hr = HttpRequest(stmt_id=2, url="https://example.com", cell_x=0, cell_y=6)
    begin.on_complete = hr

    data = write_flow([begin, hr], next_id=2)
    assert data == (pathlib.Path(__file__).parent / "http_request.flo").read_bytes()


def test_http_request_imports_cleanly(import_flow_fn):
    dialog_text = import_flow_fn(pathlib.Path(__file__).parent / "http_request.flo")

    assert "Failed to read flow" not in dialog_text, (
        f"Automate rejected http_request.flo:\n{dialog_text}"
    )
    assert "flow?" in dialog_text.lower(), (
        f"Expected an 'Import \"...\" flow?' confirmation dialog, got:\n{dialog_text}"
    )

import pathlib

from automate_flo import FlowBeginning, WifiNetworkConnected, write_flow


def test_wifi_network_connected_byte_exact():
    begin = FlowBeginning(stmt_id=1, cell_x=0, cell_y=0, title="")
    wc = WifiNetworkConnected(stmt_id=2, cell_x=0, cell_y=6)
    begin.on_complete = wc

    data = write_flow([begin, wc], next_id=2)
    assert data == (pathlib.Path(__file__).parent / "wifi_network_connected.flo").read_bytes()


def test_wifi_network_connected_imports_cleanly(import_flow_fn):
    dialog_text = import_flow_fn(pathlib.Path(__file__).parent / "wifi_network_connected.flo")

    assert "Failed to read flow" not in dialog_text, (
        f"Automate rejected wifi_network_connected.flo:\n{dialog_text}"
    )
    assert "flow?" in dialog_text.lower(), (
        f"Expected an 'Import \"...\" flow?' confirmation dialog, got:\n{dialog_text}"
    )

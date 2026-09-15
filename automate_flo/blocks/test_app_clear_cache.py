import pathlib

from automate_flo import AppClearCache, FlowBeginning, write_flow

PKG = "com.example.targetapp"


def test_app_clear_cache_byte_exact():
    begin = FlowBeginning(stmt_id=1, cell_x=0, cell_y=0, title="")
    acc = AppClearCache(stmt_id=2, package_name=PKG, cell_x=0, cell_y=6)
    begin.on_complete = acc

    data = write_flow([begin, acc], next_id=2)
    assert data == (pathlib.Path(__file__).parent / "app_clear_cache.flo").read_bytes()


def test_app_clear_cache_imports_cleanly(import_flow_fn):
    dialog_text = import_flow_fn(pathlib.Path(__file__).parent / "app_clear_cache.flo")

    assert "Failed to read flow" not in dialog_text, (
        f"Automate rejected app_clear_cache.flo:\n{dialog_text}"
    )
    assert "flow?" in dialog_text.lower(), (
        f"Expected an 'Import \"...\" flow?' confirmation dialog, got:\n{dialog_text}"
    )

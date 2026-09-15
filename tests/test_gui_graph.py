import pytest
from automate_flo.format import parse_flow, write_flow
from automate_flo_gui.graph import graph_to_blocks, blocks_to_graph

def test_graph_to_blocks_and_blocks_to_graph():
    with open("tests/fixtures/android-auto-app-toggle.flo", "rb") as f:
        data = f.read()
    
    parsed = parse_flow(data)
    g = blocks_to_graph(parsed)
    roots, next_id = graph_to_blocks(g)
    new_data = write_flow(roots, next_id)
    new_parsed = parse_flow(new_data)
    new_g = blocks_to_graph(new_parsed)
    
    assert g == new_g

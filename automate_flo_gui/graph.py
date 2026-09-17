from automate_flo.blocks import ALL_BLOCKS

TYPE_MAP = {cls.__name__: cls for cls in ALL_BLOCKS}

def graph_to_blocks(graph):
    type_map = TYPE_MAP
    nodes = graph["nodes"]
    edges = graph["edges"]

    blocks = []
    id_to_block = {}

    for node in nodes:
        cls = type_map.get(node["type"])
        if cls is None:
            raise ValueError(f"Unknown block type: {node['type']!r}")
        stmt_id = len(blocks) + 1
        block = cls(stmt_id=stmt_id, cell_x=node["x"], cell_y=node["y"], **node["fields"])
        blocks.append(block)
        id_to_block[node["id"]] = block

    for edge in edges:
        from_block = id_to_block[edge["from"]]
        to_block = id_to_block[edge["to"]]
        if edge["kind"] == "complete":
            from_block.on_complete = to_block
        elif edge["kind"] == "positive":
            from_block.on_positive = to_block
        elif edge["kind"] == "negative":
            from_block.on_negative = to_block

    referenced_ids = {edge["to"] for edge in edges}
    roots = [block for node, block in zip(nodes, blocks) if node["id"] not in referenced_ids]

    if nodes:
        if len(roots) != 1:
            raise ValueError(f"flow must have exactly one entry point with no incoming connections, found {len(roots)}")
        if roots[0].__class__.__name__ != "FlowBeginning":
            raise ValueError(f"flow must start with a FlowBeginning block, not {roots[0].__class__.__name__}")

    return roots, len(nodes)

def blocks_to_graph(parsed):
    blocks = parsed["blocks"]
    next_id = parsed["next_id"]

    nodes = []
    edges = []

    def get_or_create_node_id(block):
        if id(block) in id_to_node:
            return id_to_node[id(block)]
        node_id = f"n{len(nodes) + 1}"
        node = {
            "id": node_id,
            "type": block.__class__.__name__,
            "x": block.cell_x,
            "y": block.cell_y,
            "fields": {name: value if isinstance(value, (str, int, float, bool, type(None))) else str(value) for name, value in vars(block).items() if name not in {"stmt_id", "cell_x", "cell_y", "on_complete", "on_positive", "on_negative"}}
        }
        nodes.append(node)
        id_to_node[id(block)] = node_id
        return node_id

    id_to_node = {}

    def add_edge(from_id, to_id, kind):
        edges.append({"from": from_id, "to": to_id, "kind": kind})

    visited = set()

    def dfs(block):
        if id(block) in visited:
            return
        visited.add(id(block))
        node_id = get_or_create_node_id(block)
        kind_by_attr = {"on_complete": "complete", "on_positive": "positive", "on_negative": "negative"}
        for attr, kind in kind_by_attr.items():
            child = getattr(block, attr, None)
            if child:
                add_edge(node_id, get_or_create_node_id(child), kind)
                dfs(child)

    for block in blocks:
        dfs(block)

    return {
        "next_id": next_id,
        "nodes": nodes,
        "edges": edges
    }

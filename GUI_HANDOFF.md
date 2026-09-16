# Handoff: building the automate-flo drag-and-drop GUI

This worktree (branch `gui`, at `~/workspace/automate-flo-gui`) is for building
a web GUI on top of the existing `automate_flo` codec library, so flows can be
built visually (drag-and-drop nodes + connections, like the real Automate
app's block editor) instead of hand-writing Python.

**Driven by a local LLM (Qwen2.5-Coder via Ollama) through Aider, not Claude
Code**, same methodology as this repo's block-coverage work (see the main
`HANDOFF.md`). Work happens in the numbered batches below, one Aider session
per batch. Run the full test suite before and after each batch:

```bash
cd ~/workspace/automate-flo-gui
uv run pytest
```

Never touch `automate_flo/` (the core codec library) in this work — it is
zero-dependency and done; the GUI is purely a new layer on top that imports
from it.

## Progress (updated 2026-09-16)

**Batches 1-3 are done and committed** (commits `1cddae5`, `7beb8c6`,
`13c5796` on this branch). Batch 4 (connections + import/export UX) and
Batch 5 (polish) are not started. Resume with Batch 4 below.

What works right now, verified live end-to-end with Playwright against the
real FastAPI backend (not just unit tests): open the app, click a block type
in the left palette to add it to the canvas, drag it around (position snaps
to the grid, matching `.flo`'s `cell_x`/`cell_y` units via
`frontend/src/helpers/grid.js`'s 16px/cell), click it to select it, edit its
fields in the right-hand inspector, see the change land in the shared
`FlowStore`. Backend `/api/blocks`, `/api/flow/import`, `/api/flow/export`
all work and were round-tripped against a real device-verified fixture
(`tests/fixtures/android-auto-app-toggle.flo`, including its
Delay↔CarModeEnabled loop).

Not yet wired: dragging a connection between node ports (no `flow-port.js`/
`edge-line.js`/`port-geometry.js` yet, so edges can only be set by directly
calling `FlowStore.addEdge()`, not from the UI), and the toolbar
(New/Open/Save) doesn't exist yet — `main.js` composes palette+canvas+
inspector but has no way to trigger `/api/flow/import` or `/api/flow/export`
from the browser yet.

### Lessons from Batches 1-3, worth reading before starting Batch 4

- **Local model**: use `ollama_chat/qwen2.5-coder:7b` only. The 14b model
  was tried first and was too slow on this GPU (8GB VRAM, only half fits ->
  ~2 tok/s -> blows past Aider's default 600s timeout on any real response)
  and was removed (`ollama rm qwen2.5-coder:14b`). See the personal memory
  entry `local_llm_model_size` for why.
- **Pass long/code-heavy messages via `--message-file <path>`, never inline
  `--message "..."`** — backticks in an inline message get interpreted by
  the shell (command substitution), corrupting or dropping the whole
  invocation silently.
- **Edit format is flaky regardless of `--edit-format whole` vs `diff`**:
  the model sometimes emits plain prose/code-blocks with a filename header
  instead of the format's real markers, and Aider then applies nothing
  (files stay empty, "No test suite found" in Vitest). When this happens,
  just retry the identical request once or twice — it's non-deterministic,
  not a real disagreement with the prompt. If it keeps failing 2+ times,
  the model's response in the log is often still complete and correct
  content (just wrongly formatted) — extract it from the aider output and
  write the files directly rather than continuing to retry indefinitely.
- **Recurring bug: stray root-level files.** The model repeatedly writes a
  new *nested*-path file (e.g. `frontend/src/components/flow-node.js`) to
  the *repo root* (`flow-node.js`) instead, even when the correct path was
  given explicitly and even when it reports "Applied edit to
  frontend/src/components/flow-node.js". After every batch of new files,
  check the repo root for stray same-named files (`ls *.js` at repo root)
  and `mv` them into place before running tests.
- **Recurring test-authoring bugs to sanity-check for, every file:**
  - Missing `import { describe, it, expect, ... } from "vitest"` (near
    every generated test file had this) — causes "No test suite found" or
    `ReferenceError`.
  - jest-dom matchers used as if installed (`toHaveClass`,
    `toHaveTextContent`, `toBeInTheDocument`) — this project doesn't have
    `@testing-library/jest-dom`. Replace with plain assertions
    (`.classList.contains(...)`, `.textContent`, `!== null`).
  - `el.querySelector(...)` used where Lit renders into shadow DOM — needs
    `el.shadowRoot.querySelector(...)`.
  - A "fires an event" test reading `.detail` off `dispatchEvent()`'s
    *return value* (a boolean) instead of registering a listener first.
  - A mock (`vi.mock`/`mockResolvedValue`) configured *after* an element
    that fetches on `connectedCallback` was already appended to the
    document — the one-shot fetch already fired against the unconfigured
    mock by then. Configure the mock, then append the element.
  - `PointerEvent` isn't implemented in this project's jsdom version — use
    `MouseEvent` with a manually-assigned `.pointerId` property in tests
    (components here only ever read `clientX`/`clientY`/`pointerId` as
    plain properties, so this is equivalent).
- **Test environment must be `jsdom`, not `happy-dom`**: happy-dom silently
  failed to re-render a Lit template with a nested conditional array (data
  and render() logic were both confirmed correct via debug logging —
  swapping to jsdom fixed it immediately, no code change needed). This is
  already set in `frontend/vite.config.js`; don't change it back.
- **Workflow that worked well**: write the aider prompt to a scratch file,
  run one aider call per new file-pair (component + its test, or helper +
  its test), then `uv run pytest` / `npx vitest run` immediately after each.
  Fix small (~1-5 line) mechanical bugs directly rather than round-tripping
  through aider again; send real logic bugs back to aider as a precise,
  itemized bug report (see the git log for Batches 1 and 3 for examples of
  that style) and only escalate to writing something substantial yourself
  if aider fails repeatedly on the same file.
- Before ending a work session, do a live Playwright smoke test (not just
  unit tests) against both servers running together — several real bugs
  (e.g. the app-shell CSS grid areas never being assigned, so the palette
  rendered full-width instead of in its sidebar) only showed up that way,
  not in unit tests. Pattern: `npx playwright install chromium` (no system
  deps available on this Arch box, so skip `--with-deps`), launch chromium,
  `page.goto("http://localhost:<vite-port>/")` (use `localhost`, not
  `127.0.0.1` — vite only binds the IPv6 loopback here), use
  `page.evaluate()` to poke at component internals directly (e.g.
  `document.querySelector("app-shell").querySelector("flow-canvas").store`),
  screenshot at the end. claude-in-chrome could NOT reach localhost servers
  in this environment — use Playwright instead. Remember to revert
  `frontend/vite.config.js`'s proxy port back to `8000` and kill the
  smoke-test `uvicorn`/`vite` processes afterward.

## Stack decision (already made, do not re-litigate)

- **Backend**: FastAPI + uvicorn, run via `uv run uvicorn automate_flo_gui.server:app`.
  Chosen because it's a clean JSON API, ASGI (containerizes cleanly for a
  future k8s deploy), and pairs naturally with `uv`.
- **Frontend**: Lit (web components), built with Vite, living in `frontend/`.
  No server-side templating — the frontend is a static SPA the backend serves.
  Tested with Vitest.
- Add a `gui` optional dependency group to `pyproject.toml` (`fastapi`,
  `uvicorn[standard]`) — do NOT add these to the core `dependencies = []`.

## Frontend code shape — keep components small, tests co-located

- Every Lit component does ONE thing. If a component's template or logic is
  doing more than one job (e.g. "renders a node AND computes port pixel
  positions AND formats field values"), split the non-rendering logic out
  into a plain-JS helper module and the reusable sub-pieces into their own
  small components. Prefer several small files over one large one.
- Reusable, non-component logic (pixel/grid math, fetch wrappers for the
  `/api/*` endpoints, id generation, field-kind -> input-type mapping, JSON
  coercion, etc.) goes in `frontend/src/helpers/`, one concern per file, each
  imported by whichever components need it — never copy-pasted between
  components.
- **Every** component and helper file gets its test file next to it, same
  directory, same basename: `flow-node.js` + `flow-node.test.js`,
  `grid.js` + `grid.test.js`. No separate `frontend/tests/` or `__tests__/`
  directory — tests live beside the code they test.
- `frontend/src/components/` holds only Lit components (`*.js` + co-located
  `*.test.js`); `frontend/src/helpers/` holds only plain functions/classes
  (`*.js` + co-located `*.test.js`).

## Data contracts — follow exactly, do not improvise

### Block schema (`GET /api/blocks`)

One entry per class in `automate_flo.blocks.ALL_BLOCKS`, built by introspecting
`inspect.signature(cls.__init__)` — there is no separate schema to maintain by
hand, this must stay auto-generated so it doesn't drift as more blocks are
added.

```json
{
  "type_name": "Delay",
  "type_id": 1046,
  "category": "action",
  "doc_summary": "first line of the class docstring, or \"\"",
  "fields": [
    {"name": "seconds", "required": true, "default": null, "kind": "string"},
    {"name": "wakeup", "required": false, "default": null, "kind": "unknown"}
  ]
}
```

- `category`: `"decision"` if `issubclass(cls, automate_flo.base.Decision)`,
  else `"action"`.
- `fields`: from `inspect.signature(cls.__init__).parameters`, **in
  declared order**, excluding these structural names: `self`, `stmt_id`,
  `cell_x`, `cell_y`, `on_complete`, `on_positive`, `on_negative`. Everything
  else (including `continuity`) is a field.
  - `required` = `True` iff the parameter has no default (`param.default is
    inspect.Parameter.empty`).
  - `default`: the parameter's default, coerced to a JSON-safe value (`str`,
    `int`, `float`, `bool`, or `None`); if the raw default isn't one of those
    types, `str()` it.
  - `kind`: check `isinstance(default, bool)` **before** `isinstance(default,
    (int, float))` (bool is an int subclass in Python). Map: bool ->
    `"boolean"`, int/float -> `"number"`, str -> `"string"`, else (including
    required fields with no default to infer from) -> `"string"`.

### Graph JSON (shared shape, used both directions)

```json
{
  "next_id": 5,
  "nodes": [
    {"id": "n1", "type": "FlowBeginning", "x": 0, "y": 0,
     "fields": {"title": "", "hidden": false, "parallel": false}},
    {"id": "n2", "type": "Delay", "x": 6, "y": 0, "fields": {"seconds": 2.0}}
  ],
  "edges": [
    {"from": "n1", "to": "n2", "kind": "complete"}
  ]
}
```

- `x`/`y` are `cell_x`/`cell_y` directly (grid units, not pixels — any pixel
  scaling is a frontend rendering concern only, never sent to the backend).
- `id` is an arbitrary frontend-assigned string, used only to wire edges
  within this JSON payload. It is NOT the block's `stmt_id`.
- `kind` is one of `"complete"` (Action.on_complete), `"positive"`
  (Decision.on_positive), `"negative"` (Decision.on_negative).

### `automate_flo_gui/graph.py`

**Read `automate_flo/format.py`'s `write_flow`/`parse_flow` docstrings and
signatures first** (`write_flow(blocks, next_id)`, `parse_flow(data) ->
{"version", "next_id", "blocks"}`). Critically: in both directions, `blocks`
is only the **top-level roots** — the rest of the graph is reached by walking
`on_complete`/`on_positive`/`on_negative` (which is also how cycles/back-refs
in the file format work — the real app's flows can loop, e.g. a Delay whose
chain leads back to an earlier block). Do not treat `parsed["blocks"]` as
"all blocks in the flow" — it usually contains just one `FlowBeginning`.

`graph_to_blocks(graph: dict) -> tuple[list[Block], int]`:
1. `type_map = {cls.__name__: cls for cls in automate_flo.blocks.ALL_BLOCKS}`.
2. For each node in `graph["nodes"]`, in array order: look up the class by
   `node["type"]` (raise `ValueError(f"Unknown block type: {node['type']!r}")`
   if missing). Assign `stmt_id = index + 1` (1-based, node array order).
   Instantiate `cls(stmt_id=stmt_id, cell_x=node["x"], cell_y=node["y"],
   **node["fields"])`. Let a `TypeError` from a missing required field
   propagate — the caller (`server.py`) turns it into a 400.
3. `id_to_block = {node["id"]: block for node, block in zip(graph["nodes"], blocks)}`.
4. Second pass over `graph["edges"]`: set `id_to_block[edge["from"]].on_complete
   / .on_positive / .on_negative = id_to_block[edge["to"]]` based on
   `edge["kind"]`.
5. **Top-level roots** = every node with in-degree 0, i.e. blocks whose id
   never appears as an `edge["to"]` — in node array order. This matches real
   Automate flows (a `FlowBeginning` root, but also handles orphaned/
   not-yet-wired chains the user built but hasn't connected to anything,
   which must still round-trip and export).
6. Return `(roots, len(graph["nodes"]))` — `next_id = len(nodes)`, mirroring
   the exact convention in the main README's usage example (5 blocks ->
   `next_id=5`).

`blocks_to_graph(parsed: dict) -> dict` (`parsed` is `parse_flow()`'s return
value):
1. DFS/BFS from `parsed["blocks"]` (the roots), following `getattr(block,
   "on_complete", None)`, `getattr(block, "on_positive", None)`,
   `getattr(block, "on_negative", None)` as child pointers. Track visited
   nodes by `id(block)` (object identity) in a dict mapping to an assigned
   string id (`f"n{n}"`, 1-based in discovery order) — required to terminate
   correctly on cycles (mark a node visited **before** recursing into its
   children).
2. For each discovered block, build `fields` = every entry of `vars(block)`
   except `{"stmt_id", "cell_x", "cell_y", "on_complete", "on_positive",
   "on_negative"}`, each value coerced JSON-safe (`v if isinstance(v, (str,
   int, float, bool, type(None))) else str(v)` — leave a `# TODO` noting
   richer handling of non-primitive fields like expression/account objects is
   a follow-up, not v1 scope).
3. Build `edges` from each discovered block's `on_complete`/`on_positive`/
   `on_negative`, when not `None`, using the id mapping from step 1.
4. Return `{"next_id": len(nodes), "nodes": nodes, "edges": edges}`.

## Batches

Work through these in order. Each is one Aider session/commit. Run `uv run
pytest` before moving to the next.

### Batch 1 — backend foundation (no frontend yet)
- `pyproject.toml`: add `[project.optional-dependencies] gui = ["fastapi",
  "uvicorn[standard]"]`.
- `automate_flo_gui/__init__.py`, `automate_flo_gui/introspect.py`
  (`build_block_schemas() -> list[dict]`, exactly per the Block schema
  contract above), `automate_flo_gui/graph.py` (per the contract above),
  `automate_flo_gui/server.py` (FastAPI app: `GET /api/blocks`, `POST
  /api/flow/export` — body is Graph JSON, returns `.flo` bytes with
  `Content-Type: application/octet-stream`; `POST /api/flow/import` — body is
  raw `.flo` bytes, returns Graph JSON. Wrap `graph_to_blocks`/`write_flow`
  and `parse_flow`/`blocks_to_graph` errors as HTTP 400 with the exception
  message).
- `tests/test_gui_introspect.py`: schema exists for every `ALL_BLOCKS` entry,
  category correct for a known Action (`Delay`) and a known Decision
  (`ExpressionDecision`), required/default/kind correct for a couple of known
  fields.
- `tests/test_gui_graph.py`: round-trip using the real fixture
  `tests/fixtures/android-auto-app-toggle.flo` — `parse_flow` ->
  `blocks_to_graph` -> `graph_to_blocks` -> `write_flow` -> `parse_flow` again
  -> assert the block types/fields/edge structure match the original
  (byte-exact is NOT required here, that's already covered by the core
  library's own tests — just structural equivalence).

### Batch 2 — frontend scaffold (Lit + Vite), no canvas logic yet
- `frontend/package.json` (add `vitest` as a dev dependency alongside `lit`
  and `vite`), `frontend/vite.config.js` (dev server proxies `/api` to
  `http://127.0.0.1:8000`), `frontend/index.html`, `frontend/src/main.js`.
- `frontend/src/helpers/api-client.js`: thin wrapper functions
  `fetchBlockSchemas()`, `importFlow(bytes)`, `exportFlow(graph)` around the
  three `/api/*` endpoints — the only place `fetch()` is called from.
  `api-client.test.js` beside it, mocking `fetch`.
- `frontend/src/components/app-shell.js`: top-level layout only (toolbar
  slot + palette sidebar slot + canvas slot + inspector slot as empty
  placeholders for now) — no state or business logic in this component.
- `frontend/src/components/palette-item.js`: one block type entry (name +
  `doc_summary`), fires an event on click. Small, reusable, no fetching.
- `frontend/src/components/block-palette.js`: uses `api-client.js` to fetch
  schemas, groups by `category`, has a search input, renders one
  `palette-item` per block type. Delegates rendering of each entry to
  `palette-item`, doesn't duplicate its markup.

### Batch 3 — canvas + nodes
- `frontend/src/helpers/flow-store.js`: small plain-JS reactive store class
  (not a component) holding `{nodes: [], edges: [], selectedNodeId: null}`
  matching the Graph JSON node/edge shape, with methods to add/move/remove
  nodes, add/remove edges, select a node, and emit a change event components
  can listen to. This is the single source of truth `app-shell.js` wires
  into its children — no component owns flow state itself.
- `frontend/src/helpers/grid.js`: the cell-to-pixel scaling constant (e.g.
  16px/cell) and `cellToPixel`/`pixelToCell` functions — the only place this
  conversion happens.
- `frontend/src/components/flow-node.js`: a small card showing `type` + `id`,
  clicking selects it in the store. Pointer-drag logic for repositioning
  can live in this component (it's the one thing it owns) but must call
  into `grid.js` for the math, not reimplement it.
- `frontend/src/components/flow-canvas.js`: renders one `flow-node` per
  store node using `grid.js` for positions. Owns nothing but layout/wiring —
  no drag math, no store logic of its own.
- `frontend/src/components/inspector-field.js`: one form row for one field
  (label + the right input type for `"string"`/`"number"`/`"boolean"`/
  `"unknown"`), fires a change event with the new value. Reusable across
  every field of every block type.
- `frontend/src/components/node-inspector.js`: looks up the selected node's
  schema (via `api-client.js`), renders one `inspector-field` per schema
  field, forwards its change events into `flow-store.js`. No per-kind input
  markup of its own — that's `inspector-field`'s job.
- Clicking a `palette-item` adds a new node of that type to the store at a
  default position.

### Batch 4 — connections + import/export
- `frontend/src/helpers/port-geometry.js`: given a node's position/type,
  compute pixel anchor points for its output port(s) (one for
  Action-category `complete`, two for Decision-category `positive`/
  `negative`) and for a target node's input side — pure functions, no DOM.
- `frontend/src/components/flow-port.js`: one small draggable handle element,
  used by `flow-node.js` (one instance per output the node has). Dragging
  from it to another node's body fires an event; `flow-canvas.js` turns that
  into a `flow-store.js` edge update (replacing any existing edge from that
  same `(from, kind)` first — an output points to only one target, matching
  the data model).
- `frontend/src/components/edge-line.js`: renders one edge as an SVG line/
  bezier between two pixel points (from `port-geometry.js`). `flow-canvas.js`
  renders one `edge-line` per store edge inside an SVG overlay — it doesn't
  compute geometry itself.
- `frontend/src/components/app-toolbar.js`: **New** (clear store), **Open**
  (file input, calls `api-client.js`'s `importFlow`, replaces store
  contents), **Save** (builds Graph JSON from the store, calls
  `exportFlow`, triggers a browser download of the returned bytes as
  `flow.flo`) — three small buttons, no import/export logic of its own
  beyond calling `api-client.js` and the store.
- Delete selected node (keyboard `Delete`/`Backspace` while a node is
  selected, handled in `flow-canvas.js` or `app-shell.js`) — removes the
  node and any edges touching it via `flow-store.js`.

### Batch 5 — polish
- Highlight required-but-empty fields in the inspector in red; block Save
  (with an inline message, not a JS `alert`) if any exist.
- Add a "GUI" section to the main `README.md`: dev commands (`cd frontend &&
  npm install && npm run dev`, and `uv run uvicorn
  automate_flo_gui.server:app --reload` in another terminal), and how to
  build+serve the production bundle from FastAPI alone (`npm run build` in
  `frontend/`, then FastAPI mounts `frontend/dist` as static files at `/`).

Do not start on Docker/k8s manifests — that's an explicit later phase once
the GUI itself works, not part of this batch list.

## Running Aider against the local model

```bash
cd ~/workspace/automate-flo-gui
export OLLAMA_API_BASE=http://127.0.0.1:11434
~/.local/bin/aider --model ollama_chat/qwen2.5-coder:14b --yes-always --no-auto-commits --no-stream --no-check-update
```

(`--no-auto-commits`: review each batch's diff before committing by hand —
this is a much bigger change than the small watch-GUI fixes this pattern was
used for before, worth a manual look before it lands.)

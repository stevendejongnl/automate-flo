from pathlib import Path

from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import Response
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from automate_flo_gui import introspect, graph
from automate_flo import format

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/api/blocks")
async def get_blocks():
    return introspect.build_block_schemas()

@app.post("/api/flow/export")
async def export_flow(request: Request):
    try:
        data = await request.json()
        blocks, next_id = graph.graph_to_blocks(data)
        bytes_data = format.write_flow(blocks, next_id)
        return Response(content=bytes_data, media_type="application/octet-stream")
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/api/flow/import")
async def import_flow(request: Request):
    try:
        bytes_data = await request.body()
        parsed = format.parse_flow(bytes_data)
        return graph.blocks_to_graph(parsed)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

# Serve the built frontend (frontend/dist, after `npm run build`) as static
# files, so a single `uvicorn automate_flo_gui.server:app` can serve the
# whole GUI without a separate frontend dev server. Mounted last so it
# never shadows the /api/* routes above. Skipped entirely in local dev
# before the frontend has been built (e.g. under `uv run pytest`).
_DIST_DIR = Path(__file__).resolve().parent.parent / "frontend" / "dist"
if _DIST_DIR.is_dir():
    app.mount("/", StaticFiles(directory=_DIST_DIR, html=True), name="frontend")

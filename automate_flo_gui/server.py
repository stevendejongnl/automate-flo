from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import Response
from fastapi.middleware.cors import CORSMiddleware
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

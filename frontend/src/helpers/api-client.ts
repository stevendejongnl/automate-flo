import type { BlockSchema, Graph } from "../types.js";

export async function fetchBlockSchemas(): Promise<BlockSchema[]> {
    const response = await fetch("/api/blocks");
    if (!response.ok) {
        throw new Error(`fetchBlockSchemas failed: ${response.status}`);
    }
    return await response.json();
}

export async function importFlow(bytes: ArrayBuffer): Promise<Graph> {
    const response = await fetch("/api/flow/import", {
        method: "POST",
        headers: {
            "Content-Type": "application/octet-stream"
        },
        body: bytes
    });
    if (!response.ok) {
        throw new Error(`importFlow failed: ${response.status}`);
    }
    return await response.json();
}

export async function exportFlow(graph: Graph): Promise<ArrayBuffer> {
    const response = await fetch("/api/flow/export", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify(graph)
    });
    if (!response.ok) {
        throw new Error(`exportFlow failed: ${response.status}`);
    }
    return await response.arrayBuffer();
}

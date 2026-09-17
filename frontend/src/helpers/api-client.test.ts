import { describe, it, expect, vi, beforeEach, afterEach } from "vitest";
import { fetchBlockSchemas, importFlow, exportFlow } from "./api-client";

describe("api-client", () => {
    beforeEach(() => {
        vi.stubGlobal("fetch", vi.fn());
    });

    afterEach(() => {
        vi.unstubAllGlobals();
    });

    it("fetchBlockSchemas returns parsed JSON on successful response", async () => {
        const mockResponse = {
            ok: true,
            json: vi.fn().mockResolvedValue([{ type: "Block" }])
        };
        vi.stubGlobal("fetch", vi.fn().mockResolvedValue(mockResponse));

        const result = await fetchBlockSchemas();
        expect(result).toEqual([{ type: "Block" }]);
        expect(fetch).toHaveBeenCalledWith("/api/blocks");
    });

    it("fetchBlockSchemas throws when response.ok is false", async () => {
        const mockResponse = {
            ok: false,
            status: 404
        };
        vi.stubGlobal("fetch", vi.fn().mockResolvedValue(mockResponse));

        await expect(fetchBlockSchemas()).rejects.toThrow("fetchBlockSchemas failed: HTTP 404");
        expect(fetch).toHaveBeenCalledWith("/api/blocks");
    });

    it("fetchBlockSchemas surfaces backend detail message when available", async () => {
        const mockResponse = {
            ok: false,
            status: 400,
            json: vi.fn().mockResolvedValue({ detail: "Unknown/unhandled type id 16 at byte 57" })
        };
        vi.stubGlobal("fetch", vi.fn().mockResolvedValue(mockResponse));

        await expect(fetchBlockSchemas()).rejects.toThrow("fetchBlockSchemas failed: Unknown/unhandled type id 16 at byte 57");
        expect(fetch).toHaveBeenCalledWith("/api/blocks");
    });

    it("importFlow surfaces backend detail message when available", async () => {
        const mockResponse = {
            ok: false,
            status: 400,
            json: vi.fn().mockResolvedValue({ detail: "Unknown/unhandled type id 16 at byte 57" })
        };
        vi.stubGlobal("fetch", vi.fn().mockResolvedValue(mockResponse));

        await expect(importFlow(new ArrayBuffer(0))).rejects.toThrow("importFlow failed: Unknown/unhandled type id 16 at byte 57");
        expect(fetch).toHaveBeenCalledWith("/api/flow/import", {
            method: "POST",
            headers: {
                "Content-Type": "application/octet-stream"
            },
            body: new ArrayBuffer(0)
        });
    });

    it("importFlow calls fetch with correct parameters and returns parsed JSON", async () => {
        const mockResponse = {
            ok: true,
            json: vi.fn().mockResolvedValue({ next_id: 1, nodes: [], edges: [] })
        };
        vi.stubGlobal("fetch", vi.fn().mockResolvedValue(mockResponse));

        const bytes = new ArrayBuffer(0);
        const result = await importFlow(bytes);
        expect(result).toEqual({ next_id: 1, nodes: [], edges: [] });
        expect(fetch).toHaveBeenCalledWith("/api/flow/import", {
            method: "POST",
            headers: {
                "Content-Type": "application/octet-stream"
            },
            body: bytes
        });
    });

    it("exportFlow calls fetch with correct parameters and returns ArrayBuffer", async () => {
        const mockResponse = {
            ok: true,
            arrayBuffer: vi.fn().mockResolvedValue(new ArrayBuffer(0))
        };
        vi.stubGlobal("fetch", vi.fn().mockResolvedValue(mockResponse));

        const graph = { next_id: 1, nodes: [], edges: [] };
        const result = await exportFlow(graph);
        expect(result instanceof ArrayBuffer).toBe(true);
        expect(fetch).toHaveBeenCalledWith("/api/flow/export", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify(graph)
        });
    });
});

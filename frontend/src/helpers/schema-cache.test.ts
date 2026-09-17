import { describe, it, expect, vi, afterEach } from "vitest";
import { fetchBlockSchemas } from "./api-client.js";
import { getBlockSchemas, resetSchemaCache } from "./schema-cache.js";

vi.mock("./api-client.js", () => ({ fetchBlockSchemas: vi.fn() }));

describe("schema-cache", () => {
  const mockFetchBlockSchemas = vi.mocked(fetchBlockSchemas);

  afterEach(() => {
    resetSchemaCache();
    mockFetchBlockSchemas.mockReset();
  });

  it("fetches schemas on first call", async () => {
    mockFetchBlockSchemas.mockResolvedValue([
      { type_name: "Delay", type_id: 1046, category: "action", is_entry_point: false, doc_summary: "Waits", fields: [] }
    ]);
    const schemas = await getBlockSchemas();
    expect(schemas).toHaveLength(1);
    expect(mockFetchBlockSchemas).toHaveBeenCalledTimes(1);
  });

  it("does not re-fetch on subsequent calls", async () => {
    mockFetchBlockSchemas.mockResolvedValue([
      { type_name: "Delay", type_id: 1046, category: "action", is_entry_point: false, doc_summary: "Waits", fields: [] }
    ]);
    await getBlockSchemas();
    await getBlockSchemas();
    await getBlockSchemas();
    expect(mockFetchBlockSchemas).toHaveBeenCalledTimes(1);
  });

  it("fetches again after resetSchemaCache", async () => {
    mockFetchBlockSchemas.mockResolvedValue([]);
    await getBlockSchemas();
    resetSchemaCache();
    await getBlockSchemas();
    expect(mockFetchBlockSchemas).toHaveBeenCalledTimes(2);
  });
});

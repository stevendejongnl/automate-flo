import { vi, describe, it, expect, afterEach } from "vitest";
import { fetchBlockSchemas } from "../helpers/api-client.js";
import "./block-palette.js";
import type { BlockPalette } from "./block-palette.js";
import type { PaletteItem } from "./palette-item.js";
import { createEl } from "../helpers/test-utils.js";

vi.mock("../helpers/api-client.js", () => ({ fetchBlockSchemas: vi.fn() }));

describe("BlockPalette", () => {
  it("fetches schemas and renders palette-items", async () => {
    const mockFetchBlockSchemas = vi.mocked(fetchBlockSchemas);
    mockFetchBlockSchemas.mockResolvedValue([
      { type_name: "Delay", type_id: 1046, category: "action", is_entry_point: false, doc_summary: "Waits", fields: [] },
      { type_name: "ExpressionDecision", type_id: 1058, category: "decision", is_entry_point: false, doc_summary: "Branches", fields: [] }
    ]);

    const el = createEl<BlockPalette>("block-palette");
    document.body.appendChild(el);
    await new Promise(r => setTimeout(r, 0));
    await el.updateComplete;

    expect(el.shadowRoot!.querySelectorAll("palette-item")).toHaveLength(2);
    expect((el.shadowRoot!.querySelector("palette-item[typename='Delay']") as PaletteItem).typeName).toBe("Delay");
    expect((el.shadowRoot!.querySelector("palette-item[typename='ExpressionDecision']") as PaletteItem).typeName).toBe("ExpressionDecision");
  });

  it("filters palette-items by search query", async () => {
    const mockFetchBlockSchemas = vi.mocked(fetchBlockSchemas);
    mockFetchBlockSchemas.mockResolvedValue([
      { type_name: "Delay", type_id: 1046, category: "action", is_entry_point: false, doc_summary: "Waits", fields: [] },
      { type_name: "ExpressionDecision", type_id: 1058, category: "decision", is_entry_point: false, doc_summary: "Branches", fields: [] }
    ]);

    const el = createEl<BlockPalette>("block-palette");
    document.body.appendChild(el);
    await new Promise(r => setTimeout(r, 0));
    await el.updateComplete;

    el.shadowRoot!.querySelector<HTMLInputElement>("input")!.value = "Delay";
    el.shadowRoot!.querySelector<HTMLInputElement>("input")!.dispatchEvent(new Event("input"));
    await el.updateComplete;

    expect(el.shadowRoot!.querySelectorAll("palette-item")).toHaveLength(1);
    expect((el.shadowRoot!.querySelector("palette-item[typename='Delay']") as PaletteItem).typeName).toBe("Delay");
  });

  it("displays error message on fetch failure", async () => {
    const mockFetchBlockSchemas = vi.mocked(fetchBlockSchemas);
    mockFetchBlockSchemas.mockRejectedValueOnce(new Error("Fetch failed"));

    const el = createEl<BlockPalette>("block-palette");
    document.body.appendChild(el);
    await new Promise(r => setTimeout(r, 0));
    await el.updateComplete;

    expect(el.shadowRoot!.querySelector(".error")!.textContent).toContain("Fetch failed");
  });

  it("renders entry-point blocks in a separate start section", async () => {
    const mockFetchBlockSchemas = vi.mocked(fetchBlockSchemas);
    mockFetchBlockSchemas.mockResolvedValue([
      { type_name: "FlowBeginning", type_id: 1072, category: "action", is_entry_point: true, doc_summary: "Entry point", fields: [] },
      { type_name: "Delay", type_id: 1046, category: "action", is_entry_point: false, doc_summary: "Waits", fields: [] }
    ]);

    const el = createEl<BlockPalette>("block-palette");
    document.body.appendChild(el);
    await new Promise(r => setTimeout(r, 0));
    await el.updateComplete;

    const headings = [...el.shadowRoot!.querySelectorAll("h3")].map(h => h.textContent);
    expect(headings).toContain("start");
    expect(el.shadowRoot!.querySelectorAll("palette-item")).toHaveLength(2);
  });
});

afterEach(() => {
  const el = document.body.querySelector("block-palette");
  if (el) {
    document.body.removeChild(el);
  }
  vi.resetAllMocks();
});

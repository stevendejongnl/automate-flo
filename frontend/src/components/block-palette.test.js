import { vi, describe, it, expect, afterEach } from "vitest";
import { fetchBlockSchemas } from "../helpers/api-client.js";
import "./block-palette.js";

vi.mock("../helpers/api-client.js", () => ({ fetchBlockSchemas: vi.fn() }));

describe("BlockPalette", () => {
  it("fetches schemas and renders palette-items", async () => {
    fetchBlockSchemas.mockResolvedValue([
      { type_name: "Delay", type_id: 1046, category: "action", doc_summary: "Waits", fields: [] },
      { type_name: "ExpressionDecision", type_id: 1058, category: "decision", doc_summary: "Branches", fields: [] }
    ]);

    const el = document.createElement("block-palette");
    document.body.appendChild(el);
    await new Promise(r => setTimeout(r, 0));
    await el.updateComplete;

    expect(el.shadowRoot.querySelectorAll("palette-item")).toHaveLength(2);
    expect(el.shadowRoot.querySelector("palette-item[typename='Delay']").typeName).toBe("Delay");
    expect(el.shadowRoot.querySelector("palette-item[typename='ExpressionDecision']").typeName).toBe("ExpressionDecision");
  });

  it("filters palette-items by search query", async () => {
    fetchBlockSchemas.mockResolvedValue([
      { type_name: "Delay", type_id: 1046, category: "action", doc_summary: "Waits", fields: [] },
      { type_name: "ExpressionDecision", type_id: 1058, category: "decision", doc_summary: "Branches", fields: [] }
    ]);

    const el = document.createElement("block-palette");
    document.body.appendChild(el);
    await new Promise(r => setTimeout(r, 0));
    await el.updateComplete;

    el.shadowRoot.querySelector("input").value = "Delay";
    el.shadowRoot.querySelector("input").dispatchEvent(new Event("input"));
    await el.updateComplete;

    expect(el.shadowRoot.querySelectorAll("palette-item")).toHaveLength(1);
    expect(el.shadowRoot.querySelector("palette-item[typename='Delay']").typeName).toBe("Delay");
  });

  it("displays error message on fetch failure", async () => {
    fetchBlockSchemas.mockRejectedValueOnce(new Error("Fetch failed"));

    const el = document.createElement("block-palette");
    document.body.appendChild(el);
    await new Promise(r => setTimeout(r, 0));
    await el.updateComplete;

    expect(el.shadowRoot.querySelector(".error").textContent).toContain("Fetch failed");
  });
});

afterEach(() => {
  document.body.removeChild(document.body.querySelector("block-palette"));
  fetchBlockSchemas.mockReset();
});

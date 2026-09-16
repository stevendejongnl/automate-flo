import { describe, it, expect, vi, beforeEach, afterEach } from "vitest";
import { FlowStore } from "../helpers/flow-store.js";
import { getBlockSchemas } from "../helpers/schema-cache.js";
import "./node-inspector.js";
import type { NodeInspector } from "./node-inspector.js";
import type { InspectorField } from "./inspector-field.js";
import { createEl } from "../helpers/test-utils.js";

vi.mock("../helpers/schema-cache.js", () => ({ getBlockSchemas: vi.fn() }));

describe("NodeInspector", () => {
  let el: NodeInspector;
  let store: FlowStore;
  const mockFetchBlockSchemas = vi.mocked(getBlockSchemas);

  beforeEach(() => {
    store = new FlowStore();
    el = createEl<NodeInspector>("node-inspector");
    el.store = store;
    // Not appended yet -- each test configures the fetchBlockSchemas mock
    // first, then appends (which triggers connectedCallback/_loadSchemas),
    // so the mock's resolved value is in place before the component's one
    // and only call to it.
  });

  afterEach(() => {
    if (el.isConnected) {
      document.body.removeChild(el);
    }
    mockFetchBlockSchemas.mockReset();
  });

  it("shows 'No node selected' when no node is selected", async () => {
    mockFetchBlockSchemas.mockResolvedValue([]);
    document.body.appendChild(el);
    await el.updateComplete;
    expect(el.shadowRoot!.querySelector(".empty")!.textContent!.trim()).toBe("No node selected");
  });

  it("shows 'Loading...' when schemas are loading", async () => {
    mockFetchBlockSchemas.mockResolvedValue([]);
    store.nodes = [{ id: "n1", type: "Delay", x: 0, y: 0, fields: { seconds: 5 } }];
    store.selectNode("n1");
    document.body.appendChild(el);
    await el.updateComplete;
    expect(el.shadowRoot!.querySelector(".empty")!.textContent!.trim()).toBe("Loading...");
  });

  it("renders inspector fields when a node is selected and schema is available", async () => {
    mockFetchBlockSchemas.mockResolvedValue([
      { type_name: "Delay", type_id: 1046, category: "action", doc_summary: "Waits", fields: [{ name: "seconds", required: true, default: null, kind: "number" }] }
    ]);
    store.nodes = [{ id: "n1", type: "Delay", x: 0, y: 0, fields: { seconds: 5 } }];
    store.selectNode("n1");
    document.body.appendChild(el);
    await new Promise(r => setTimeout(r, 0));
    await el.updateComplete;
    const field = el.shadowRoot!.querySelector("inspector-field") as InspectorField;
    expect(field.fieldName).toBe("seconds");
    expect(field.fieldKind).toBe("number");
    expect(field.value).toBe(5);
    expect(field.required).toBe(true);
  });

  it("updates store when a field is changed", async () => {
    mockFetchBlockSchemas.mockResolvedValue([
      { type_name: "Delay", type_id: 1046, category: "action", doc_summary: "Waits", fields: [{ name: "seconds", required: true, default: null, kind: "number" }] }
    ]);
    store.nodes = [{ id: "n1", type: "Delay", x: 0, y: 0, fields: { seconds: 5 } }];
    store.selectNode("n1");
    document.body.appendChild(el);
    await new Promise(r => setTimeout(r, 0));
    await el.updateComplete;
    const field = el.shadowRoot!.querySelector("inspector-field") as InspectorField;
    field.dispatchEvent(new CustomEvent("field-changed", { detail: { fieldName: "seconds", value: 8 }, bubbles: true, composed: true }));
    await el.updateComplete;
    expect(store.nodes[0].fields.seconds).toBe(8);
  });
});

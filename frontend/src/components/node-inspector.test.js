import { describe, it, expect, vi, beforeEach, afterEach } from "vitest";
import { FlowStore } from "../helpers/flow-store.js";
import { fetchBlockSchemas } from "../helpers/api-client.js";
import "./node-inspector.js";

vi.mock("../helpers/api-client.js", () => ({ fetchBlockSchemas: vi.fn() }));

describe("NodeInspector", () => {
  let el, store;

  beforeEach(() => {
    store = new FlowStore();
    el = document.createElement("node-inspector");
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
    fetchBlockSchemas.mockReset();
  });

  it("shows 'No node selected' when no node is selected", async () => {
    fetchBlockSchemas.mockResolvedValue([]);
    document.body.appendChild(el);
    await el.updateComplete;
    expect(el.shadowRoot.querySelector(".empty").textContent.trim()).toBe("No node selected");
  });

  it("shows 'Loading...' when schemas are loading", async () => {
    fetchBlockSchemas.mockResolvedValue([]);
    store.nodes = [{ id: 1, type: "Delay", fields: { seconds: 5 } }];
    store.selectNode(1);
    document.body.appendChild(el);
    await el.updateComplete;
    expect(el.shadowRoot.querySelector(".empty").textContent.trim()).toBe("Loading...");
  });

  it("renders inspector fields when a node is selected and schema is available", async () => {
    fetchBlockSchemas.mockResolvedValue([
      { type_name: "Delay", type_id: 1046, category: "action", doc_summary: "Waits", fields: [{ name: "seconds", required: true, default: null, kind: "number" }] }
    ]);
    store.nodes = [{ id: 1, type: "Delay", fields: { seconds: 5 } }];
    store.selectNode(1);
    document.body.appendChild(el);
    await new Promise(r => setTimeout(r, 0));
    await el.updateComplete;
    const field = el.shadowRoot.querySelector("inspector-field");
    expect(field.fieldName).toBe("seconds");
    expect(field.fieldKind).toBe("number");
    expect(field.value).toBe(5);
  });

  it("updates store when a field is changed", async () => {
    fetchBlockSchemas.mockResolvedValue([
      { type_name: "Delay", type_id: 1046, category: "action", doc_summary: "Waits", fields: [{ name: "seconds", required: true, default: null, kind: "number" }] }
    ]);
    store.nodes = [{ id: 1, type: "Delay", fields: { seconds: 5 } }];
    store.selectNode(1);
    document.body.appendChild(el);
    await new Promise(r => setTimeout(r, 0));
    await el.updateComplete;
    const field = el.shadowRoot.querySelector("inspector-field");
    field.dispatchEvent(new CustomEvent("field-changed", { detail: { fieldName: "seconds", value: 8 }, bubbles: true, composed: true }));
    await new Promise(r => setTimeout(r, 0));
    await el.updateComplete;
    expect(store.nodes[0].fields.seconds).toBe(8);
  });
});

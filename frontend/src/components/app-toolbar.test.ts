import { describe, it, expect, vi, beforeEach, afterEach } from "vitest";
import { FlowStore } from "../helpers/flow-store.js";
import { importFlow, exportFlow } from "../helpers/api-client.js";
import { getBlockSchemas } from "../helpers/schema-cache.js";
import { createEl } from "../helpers/test-utils.js";
import "./app-toolbar.js";
import type { AppToolbar } from "./app-toolbar.js";

vi.mock("../helpers/api-client.js", () => ({
  importFlow: vi.fn(),
  exportFlow: vi.fn(),
}));
vi.mock("../helpers/schema-cache.js", () => ({
  getBlockSchemas: vi.fn(),
}));

describe("AppToolbar", () => {
  let el: AppToolbar;
  let store: FlowStore;
  const mockGetBlockSchemas = vi.mocked(getBlockSchemas);

  beforeEach(() => {
    store = new FlowStore();
    el = createEl<AppToolbar>("app-toolbar");
    el.store = store;
    // Not appended yet -- each test configures the getBlockSchemas mock
    // first, then appends (which triggers connectedCallback/_loadSchemas),
    // so the mock's resolved value is in place before the component's one
    // and only call to it (see node-inspector.test.ts for the same pattern
    // and why it matters).
  });

  afterEach(() => {
    if (el.isConnected) {
      document.body.removeChild(el);
    }
    vi.resetAllMocks();
  });

  it("clicking 'New' resets the store", async () => {
    mockGetBlockSchemas.mockResolvedValue([]);
    document.body.appendChild(el);
    await el.updateComplete;
    store.addNode("Delay", 0, 0);
    store.selectNode("n1");
    [...el.shadowRoot!.querySelectorAll("button")].find(b => b.textContent === "New")!.click();
    expect(store.nodes).toEqual([]);
    expect(store.selectedNodeId).toBeNull();
  });

  it("clicking 'Open' triggers a click on the hidden file input", async () => {
    mockGetBlockSchemas.mockResolvedValue([]);
    document.body.appendChild(el);
    await el.updateComplete;
    const clickSpy = vi.spyOn(HTMLInputElement.prototype, "click");
    [...el.shadowRoot!.querySelectorAll("button")].find(b => b.textContent === "Open")!.click();
    expect(clickSpy).toHaveBeenCalled();
  });

  it("selecting a file loads the graph into the store", async () => {
    mockGetBlockSchemas.mockResolvedValue([]);
    document.body.appendChild(el);
    await el.updateComplete;
    URL.createObjectURL = vi.fn(() => "blob:mock-url");
    URL.revokeObjectURL = vi.fn();
    // jsdom's File/Blob don't implement .arrayBuffer() in this project's
    // version, so stub a minimal file-like object with just that method
    // instead of using a real File instance.
    const fakeBuffer = new Uint8Array([1, 2, 3]).buffer;
    const file = { arrayBuffer: () => Promise.resolve(fakeBuffer) } as unknown as File;
    vi.mocked(importFlow).mockResolvedValue({ next_id: 1, nodes: [{ id: "n1", type: "Delay", x: 0, y: 0, fields: {} }], edges: [] });
    const input = el.renderRoot.querySelector<HTMLInputElement>("input[type='file']")!;
    Object.defineProperty(input, "files", { value: [file], configurable: true });
    input.dispatchEvent(new Event("change"));
    await new Promise(r => setTimeout(r, 0));
    expect(importFlow).toHaveBeenCalledWith(fakeBuffer);
    expect(store.nodes).toEqual([{ id: "n1", type: "Delay", x: 0, y: 0, fields: {} }]);
  });

  it("clicking 'Save' triggers a download when all required fields are filled", async () => {
    mockGetBlockSchemas.mockResolvedValue([
      { type_name: "Delay", type_id: 1046, category: "action", is_entry_point: false, doc_summary: "Waits", fields: [{ name: "seconds", required: true, default: null, kind: "number" }] }
    ]);
    document.body.appendChild(el);
    await el.updateComplete;
    URL.createObjectURL = vi.fn(() => "blob:mock-url");
    URL.revokeObjectURL = vi.fn();
    const clickSpy = vi.spyOn(HTMLAnchorElement.prototype, "click").mockImplementation(() => {});
    store.addNode("Delay", 0, 0, { seconds: 5 });
    const graph = { next_id: 1, nodes: [{ id: "n1", type: "Delay", x: 0, y: 0, fields: { seconds: 5 } }], edges: [] };
    vi.mocked(exportFlow).mockResolvedValue(new TextEncoder().encode("fake flo bytes").buffer);
    [...el.shadowRoot!.querySelectorAll("button")].find(b => b.textContent === "Save")!.click();
    await new Promise(r => setTimeout(r, 0));
    expect(exportFlow).toHaveBeenCalledWith(graph);
    expect(clickSpy).toHaveBeenCalled();
  });

  it("blocks 'Save' and shows an inline message when a required field is empty", async () => {
    mockGetBlockSchemas.mockResolvedValue([
      { type_name: "Delay", type_id: 1046, category: "action", is_entry_point: false, doc_summary: "Waits", fields: [{ name: "seconds", required: true, default: null, kind: "number" }] }
    ]);
    document.body.appendChild(el);
    await el.updateComplete;
    store.addNode("Delay", 0, 0);
    [...el.shadowRoot!.querySelectorAll("button")].find(b => b.textContent === "Save")!.click();
    await new Promise(r => setTimeout(r, 0));
    await el.updateComplete;
    expect(exportFlow).not.toHaveBeenCalled();
    expect(el.shadowRoot!.querySelector(".error")).not.toBeNull();
  });

  it("shows an inline error message when importing a file fails", async () => {
    mockGetBlockSchemas.mockResolvedValue([]);
    document.body.appendChild(el);
    await el.updateComplete;
    vi.mocked(importFlow).mockRejectedValue(new Error("importFlow failed: Unknown/unhandled type id 16 at byte 57"));
    const input = el.renderRoot.querySelector<HTMLInputElement>("input[type='file']")!;
    Object.defineProperty(input, "files", { value: [{ arrayBuffer: () => Promise.resolve(new Uint8Array([1, 2, 3]).buffer) }], configurable: true });
    input.dispatchEvent(new Event("change"));
    await new Promise(r => setTimeout(r, 0));
    await el.updateComplete;
    expect(el.shadowRoot!.querySelector(".error")!.textContent).toContain("Unknown/unhandled type id 16 at byte 57");
    expect(store.nodes).toEqual([]);
  });

  it("shows an inline error message when saving fails", async () => {
    mockGetBlockSchemas.mockResolvedValue([]);
    document.body.appendChild(el);
    await el.updateComplete;
    store.addNode("Delay", 0, 0);
    vi.mocked(exportFlow).mockRejectedValue(new Error("exportFlow failed: some backend error"));
    [...el.shadowRoot!.querySelectorAll("button")].find(b => b.textContent === "Save")!.click();
    await new Promise(r => setTimeout(r, 0));
    await el.updateComplete;
    expect(el.shadowRoot!.querySelector(".error")!.textContent).toContain("exportFlow failed: some backend error");
  });
});

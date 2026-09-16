import { describe, it, expect, vi, beforeEach, afterEach } from "vitest";
import { FlowStore } from "../helpers/flow-store.js";
import { importFlow, exportFlow } from "../helpers/api-client.js";
import { createEl } from "../helpers/test-utils.js";
import "./app-toolbar.js";
import type { AppToolbar } from "./app-toolbar.js";

vi.mock("../helpers/api-client.js", () => ({
  importFlow: vi.fn(),
  exportFlow: vi.fn(),
}));

describe("AppToolbar", () => {
  let el: AppToolbar;
  let store: FlowStore;

  beforeEach(async () => {
    store = new FlowStore();
    el = createEl<AppToolbar>("app-toolbar");
    el.store = store;
    document.body.appendChild(el);
    await el.updateComplete;
  });

  afterEach(() => {
    if (el.isConnected) {
      document.body.removeChild(el);
    }
    vi.resetAllMocks();
  });

  it("clicking 'New' resets the store", async () => {
    store.addNode("Delay", 0, 0);
    store.selectNode("n1");
    [...el.shadowRoot!.querySelectorAll("button")].find(b => b.textContent === "New")!.click();
    expect(store.nodes).toEqual([]);
    expect(store.selectedNodeId).toBeNull();
  });

  it("clicking 'Open' triggers a click on the hidden file input", async () => {
    const clickSpy = vi.spyOn(HTMLInputElement.prototype, "click");
    [...el.shadowRoot!.querySelectorAll("button")].find(b => b.textContent === "Open")!.click();
    expect(clickSpy).toHaveBeenCalled();
  });

  it("selecting a file loads the graph into the store", async () => {
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

  it("clicking 'Save' triggers a download", async () => {
    URL.createObjectURL = vi.fn(() => "blob:mock-url");
    URL.revokeObjectURL = vi.fn();
    const clickSpy = vi.spyOn(HTMLAnchorElement.prototype, "click").mockImplementation(() => {});
    store.addNode("Delay", 0, 0);
    const graph = { next_id: 1, nodes: [{ id: "n1", type: "Delay", x: 0, y: 0, fields: {} }], edges: [] };
    vi.mocked(exportFlow).mockResolvedValue(new TextEncoder().encode("fake flo bytes").buffer);
    [...el.shadowRoot!.querySelectorAll("button")].find(b => b.textContent === "Save")!.click();
    await new Promise(r => setTimeout(r, 0));
    expect(exportFlow).toHaveBeenCalledWith(graph);
    expect(clickSpy).toHaveBeenCalled();
  });
});

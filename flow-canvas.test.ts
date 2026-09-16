import { describe, it, expect, vi, beforeEach, afterEach } from "vitest";
import { FlowStore } from "../helpers/flow-store.js";
import "./flow-canvas.js";
import type { FlowCanvas } from "./flow-canvas.js";
import { createEl } from "../helpers/test-utils.js";

vi.mock("../helpers/flow-store.js", () => ({ FlowStore: vi.fn() }));

describe("FlowCanvas", () => {
  let store: FlowStore;
  let el: FlowCanvas;

  beforeEach(() => {
    store = new FlowStore();
    el = createEl<FlowCanvas>("flow-canvas");
    el.store = store;
    document.body.appendChild(el);
  });

  afterEach(() => {
    document.body.removeChild(el);
  });

  it("renders a flow-node when a node is added to the store", async () => {
    store.addNode("Delay", 6, 0);
    await el.updateComplete;
    expect(el.shadowRoot!.querySelector("flow-node")).toHaveProperty("blockType", "Delay");
    expect(el.shadowRoot!.querySelector("flow-node")).toHaveProperty("x", 96);
  });

  it("selects a node when it is selected in the store", async () => {
    const nodeId = store.addNode("Delay", 6, 0);
    const otherId = store.addNode("Delay", 12, 0);
    store.selectNode(nodeId);
    await el.updateComplete;
    const nodeEls = [...el.shadowRoot!.querySelectorAll("flow-node") as FlowNode[]];
    const selectedEl = nodeEls.find(n => n.nodeId === nodeId);
    const otherEl = nodeEls.find(n => n.nodeId === otherId);
    expect(selectedEl).toHaveProperty("selected", true);
    expect(otherEl).toHaveProperty("selected", false);
  });

  it("updates the store when a flow-node is selected", async () => {
    const nodeId = store.addNode("Delay", 6, 0);
    await el.updateComplete;
    const flowNodeEl = el.shadowRoot!.querySelector("flow-node") as FlowNode;
    flowNodeEl.dispatchEvent(new CustomEvent("flow-node-selected", { detail: { nodeId }, bubbles: true, composed: true }));
    await el.updateComplete;
    expect(store.selectedNodeId).toBe(nodeId);
  });

  it("updates the store when a flow-node is moved", async () => {
    const nodeId = store.addNode("Delay", 6, 0);
    await el.updateComplete;
    const flowNodeEl = el.shadowRoot!.querySelector("flow-node") as FlowNode;
    flowNodeEl.dispatchEvent(new CustomEvent("flow-node-moved", { detail: { nodeId, x: 96, y: 32 }, bubbles: true, composed: true }));
    await el.updateComplete;
    const node = store.nodes.find(n => n.id === nodeId);
    expect(node.x).toBe(6);
    expect(node.y).toBe(2);
  });

  it("deselects when clicking on the canvas background", async () => {
    const nodeId = store.addNode("Delay", 6, 0);
    store.selectNode(nodeId);
    await el.updateComplete;
    el.shadowRoot!.querySelector(".surface")!.click();
    await el.updateComplete;
    expect(store.selectedNodeId).toBe(null);
  });
});

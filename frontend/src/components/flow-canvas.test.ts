import { describe, it, expect, beforeEach, afterEach } from "vitest";
import { FlowStore } from "../helpers/flow-store.js";
import "./flow-canvas.js";
import type { FlowCanvas } from "./flow-canvas.js";
import type { FlowNode } from "./flow-node.js";
import { createEl } from "../helpers/test-utils.js";

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
    const nodeEls = [...el.shadowRoot!.querySelectorAll("flow-node")] as FlowNode[];
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
    expect(node!.x).toBe(6);
    expect(node!.y).toBe(2);
  });

  it("deselects when clicking on the canvas background", async () => {
    const nodeId = store.addNode("Delay", 6, 0);
    store.selectNode(nodeId);
    await el.updateComplete;
    el.shadowRoot!.querySelector<HTMLElement>(".surface")!.click();
    await el.updateComplete;
    expect(store.selectedNodeId).toBe(null);
  });

  it("renders a connector line for each edge in the store", async () => {
    const n1 = store.addNode("Delay", 0, 0);
    const n2 = store.addNode("Delay", 6, 0);
    store.addEdge(n1, n2, "complete");
    await el.updateComplete;
    expect(el.shadowRoot!.querySelectorAll("svg.edges line")).toHaveLength(1);
  });

  it("updates the store when a flow-node dispatches flow-node-connected", async () => {
    const n1 = store.addNode("Delay", 0, 0);
    const n2 = store.addNode("Delay", 6, 0);
    await el.updateComplete;
    const flowNodeEl = el.shadowRoot!.querySelector("flow-node") as FlowNode;
    flowNodeEl.dispatchEvent(new CustomEvent("flow-node-connected", { detail: { from: n1, kind: "complete", to: n2 }, bubbles: true, composed: true }));
    await el.updateComplete;
    expect(store.edges).toEqual([{ from: n1, to: n2, kind: "complete" }]);
  });

  it("removes the selected node when Delete is pressed", async () => {
    const nodeId = store.addNode("Delay", 0, 0);
    store.selectNode(nodeId);
    await el.updateComplete;
    window.dispatchEvent(new KeyboardEvent("keydown", { key: "Delete" }));
    expect(store.nodes).toEqual([]);
  });

  it("does not delete when Backspace is pressed while an input is focused", async () => {
    const nodeId = store.addNode("Delay", 0, 0);
    store.selectNode(nodeId);
    await el.updateComplete;
    const input = document.createElement("input");
    document.body.appendChild(input);
    input.focus();
    input.dispatchEvent(new KeyboardEvent("keydown", { key: "Backspace", bubbles: true }));
    expect(store.nodes).toHaveLength(1);
    document.body.removeChild(input);
  });
});

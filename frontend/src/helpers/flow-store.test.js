import { describe, it, expect, vi, beforeEach } from "vitest";
import { FlowStore } from "./flow-store.js";

describe("FlowStore", () => {
  let store;
  let onChangeCallback;
  let unsubscribe;

  beforeEach(() => {
    store = new FlowStore();
    onChangeCallback = vi.fn();
    unsubscribe = store.onChange(onChangeCallback);
  });

  it("adds a node and notifies listeners", () => {
    const nodeId = store.addNode("type", 100, 200);
    expect(nodeId).toBe("n1");
    expect(store.nodes).toEqual([{ id: "n1", type: "type", x: 100, y: 200, fields: {} }]);
    expect(onChangeCallback).toHaveBeenCalled();
  });

  it("moves a node", () => {
    store.addNode("type", 100, 200);
    store.moveNode("n1", 150, 250);
    expect(store.nodes).toEqual([{ id: "n1", type: "type", x: 150, y: 250, fields: {} }]);
  });

  it("updates node fields", () => {
    store.addNode("type", 100, 200);
    store.updateNodeFields("n1", { key: "value" });
    expect(store.nodes).toEqual([{ id: "n1", type: "type", x: 100, y: 200, fields: { key: "value" } }]);
  });

  it("removes a node and cascades to remove edges", () => {
    store.addNode("type", 100, 200);
    store.addEdge("n1", "n2", "kind");
    store.removeNode("n1");
    expect(store.nodes).toEqual([]);
    expect(store.edges).toEqual([]);
  });

  it("selects a node", () => {
    store.addNode("type", 100, 200);
    store.selectNode("n1");
    expect(store.selectedNodeId).toBe("n1");
  });

  it("adds an edge and replaces existing edge", () => {
    store.addNode("type", 100, 200);
    store.addEdge("n1", "n2", "kind");
    store.addEdge("n1", "n2", "kind");
    expect(store.edges).toEqual([{ from: "n1", to: "n2", kind: "kind" }]);
  });

  it("removes an edge", () => {
    store.addNode("type", 100, 200);
    store.addEdge("n1", "n2", "kind");
    store.removeEdge("n1", "kind");
    expect(store.edges).toEqual([]);
  });

  it("loads a graph and resumes _genNodeId numbering", () => {
    store.loadGraph({ nodes: [{ id: "n1" }, { id: "n3" }], edges: [] });
    expect(store.nodes).toEqual([{ id: "n1" }, { id: "n3" }]);
    expect(store.edges).toEqual([]);
    expect(store._nextNodeNum).toBe(4);
  });

  it("returns the expected shape from toGraph", () => {
    store.addNode("type", 100, 200);
    store.addEdge("n1", "n2", "kind");
    expect(store.toGraph()).toEqual({
      next_id: 1,
      nodes: [{ id: "n1", type: "type", x: 100, y: 200, fields: {} }],
      edges: [{ from: "n1", to: "n2", kind: "kind" }]
    });
  });

  it("unsubscribes from onChange", () => {
    store.addNode("type", 100, 200);
    expect(onChangeCallback).toHaveBeenCalled();
    unsubscribe();
    store.addNode("type", 100, 200);
    expect(onChangeCallback).toHaveBeenCalledTimes(1);
  });
});

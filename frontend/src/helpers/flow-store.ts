import type { GraphNode, GraphEdge, EdgeKind, Graph } from "../types.js";

export class FlowStore {
  nodes: GraphNode[];
  edges: GraphEdge[];
  selectedNodeId: string | null;
  private _listeners: Array<() => void>;
  _nextNodeNum: number;

  constructor() {
    this.nodes = [];
    this.edges = [];
    this.selectedNodeId = null;
    this._listeners = [];
    this._nextNodeNum = 1;
  }

  onChange(callback: () => void): () => void {
    this._listeners.push(callback);
    return () => {
      this._listeners = this._listeners.filter(cb => cb !== callback);
    };
  }

  private _notify(): void {
    this._listeners.forEach(listener => listener());
  }

  addNode(type: string, x: number, y: number, fields?: Record<string, unknown>): string {
    const id = this._genNodeId();
    const node: GraphNode = { id, type, x, y, fields: fields || {} };
    this.nodes.push(node);
    this._notify();
    return id;
  }

  private _genNodeId(): string {
    return `n${this._nextNodeNum++}`;
  }

  moveNode(id: string, x: number, y: number): void {
    const node = this.nodes.find(n => n.id === id);
    if (node) {
      node.x = x;
      node.y = y;
      this._notify();
    }
  }

  updateNodeFields(id: string, fields: Record<string, unknown>): void {
    const node = this.nodes.find(n => n.id === id);
    if (node) {
      Object.assign(node.fields, fields);
      this._notify();
    }
  }

  removeNode(id: string): void {
    const index = this.nodes.findIndex(n => n.id === id);
    if (index !== -1) {
      this.nodes.splice(index, 1);
      this.edges = this.edges.filter(e => e.from !== id && e.to !== id);
      if (this.selectedNodeId === id) {
        this.selectedNodeId = null;
      }
      this._notify();
    }
  }

  selectNode(id: string | null): void {
    this.selectedNodeId = id;
    this._notify();
  }

  addEdge(from: string, to: string, kind: EdgeKind): void {
    this.edges = this.edges.filter(e => !(e.from === from && e.kind === kind));
    this.edges.push({ from, to, kind });
    this._notify();
  }

  removeEdge(from: string, kind: EdgeKind): void {
    this.edges = this.edges.filter(e => !(e.from === from && e.kind === kind));
    this._notify();
  }

  loadGraph(graph: Graph): void {
    this.nodes = graph.nodes;
    this.edges = graph.edges;
    this.selectedNodeId = null;
    const maxId = Math.max(0, ...this.nodes.map(n => parseInt(n.id.slice(1), 10) || 0));
    this._nextNodeNum = maxId + 1;
    this._notify();
  }

  toGraph(): Graph {
    return {
      next_id: this.nodes.length,
      nodes: this.nodes,
      edges: this.edges
    };
  }
}

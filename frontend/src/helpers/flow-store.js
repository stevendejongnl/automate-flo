export class FlowStore {
  constructor() {
    this.nodes = [];
    this.edges = [];
    this.selectedNodeId = null;
    this._listeners = [];
    this._nextNodeNum = 1;
  }

  onChange(callback) {
    this._listeners.push(callback);
    return () => {
      this._listeners = this._listeners.filter(cb => cb !== callback);
    };
  }

  _notify() {
    this._listeners.forEach(listener => listener());
  }

  addNode(type, x, y, fields = {}) {
    const id = this._genNodeId();
    const node = { id, type, x, y, fields };
    this.nodes.push(node);
    this._notify();
    return id;
  }

  _genNodeId() {
    return `n${this._nextNodeNum++}`;
  }

  moveNode(id, x, y) {
    const node = this.nodes.find(n => n.id === id);
    if (node) {
      node.x = x;
      node.y = y;
      this._notify();
    }
  }

  updateNodeFields(id, fields) {
    const node = this.nodes.find(n => n.id === id);
    if (node) {
      Object.assign(node.fields, fields);
      this._notify();
    }
  }

  removeNode(id) {
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

  selectNode(id) {
    this.selectedNodeId = id;
    this._notify();
  }

  addEdge(from, to, kind) {
    this.edges = this.edges.filter(e => !(e.from === from && e.kind === kind));
    this.edges.push({ from, to, kind });
    this._notify();
  }

  removeEdge(from, kind) {
    this.edges = this.edges.filter(e => !(e.from === from && e.kind === kind));
    this._notify();
  }

  loadGraph(graph) {
    this.nodes = graph?.nodes || [];
    this.edges = graph?.edges || [];
    this.selectedNodeId = null;
    const maxId = Math.max(0, ...this.nodes.map(n => parseInt(n.id.slice(1), 10) || 0));
    this._nextNodeNum = maxId + 1;
    this._notify();
  }

  toGraph() {
    return {
      next_id: this.nodes.length,
      nodes: this.nodes,
      edges: this.edges
    };
  }
}

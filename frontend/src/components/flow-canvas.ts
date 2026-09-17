import { LitElement, html, css, svg } from "lit";
import { cellToPixel, pixelToCell } from "../helpers/grid.js";
import { inputAnchor, outputAnchor } from "../helpers/port-geometry.js";
import { getBlockSchemas } from "../helpers/schema-cache.js";
import "./flow-node.js";
import { FlowStore } from "../helpers/flow-store.js";
import type { BlockSchema, BlockCategory, GraphNode, GraphEdge } from "../types.js";

export class FlowCanvas extends LitElement {
  static properties = {
    store: { type: Object, attribute: false },
    _schemas: { type: Array, state: true },
  };

  static styles = css`
    :host {
      position: relative;
      width: 100%;
      height: 100%;
      overflow: auto;
      background: #f5f5f5;
    }
    .surface {
      position: relative;
      width: 100%;
      height: 100%;
    }
    .edges {
      position: absolute;
      top: 0;
      left: 0;
      width: 100%;
      height: 100%;
      pointer-events: none;
    }
  `;

  declare store: FlowStore;
  declare _schemas: BlockSchema[];
  private _unsubscribe: (() => void) | null = null;

  constructor() {
    super();
    this._schemas = [];
    this._onKeyDown = this._onKeyDown.bind(this);
  }

  connectedCallback(): void {
    super.connectedCallback();
    if (this.store) {
      this._unsubscribe = this.store.onChange(() => this.requestUpdate());
    }
    this._loadSchemas();
    window.addEventListener("keydown", this._onKeyDown);
  }

  disconnectedCallback(): void {
    super.disconnectedCallback();
    if (this._unsubscribe) {
      this._unsubscribe();
    }
    window.removeEventListener("keydown", this._onKeyDown);
  }

  async _loadSchemas(): Promise<void> {
    try {
      this._schemas = await getBlockSchemas();
    } catch {
      this._schemas = [];
    }
  }

  _categoryFor(type: string): BlockCategory {
    return this._schemas.find(s => s.type_name === type)?.category ?? "action";
  }

  _onKeyDown(event: KeyboardEvent): void {
    if (event.target instanceof HTMLInputElement || event.target instanceof HTMLTextAreaElement) {
      return;
    }
    if ((event.key === "Delete" || event.key === "Backspace") && this.store?.selectedNodeId) {
      this.store.removeNode(this.store.selectedNodeId);
    }
  }

  _renderEdge(edge: GraphEdge) {
    const fromNode = this.store.nodes.find(n => n.id === edge.from);
    const toNode = this.store.nodes.find(n => n.id === edge.to);
    if (!fromNode || !toNode) return null;
    const fromPos = { x: cellToPixel(fromNode.x), y: cellToPixel(fromNode.y) };
    const toPos = { x: cellToPixel(toNode.x), y: cellToPixel(toNode.y) };
    const from = outputAnchor(fromPos, edge.kind, this._categoryFor(fromNode.type));
    const to = inputAnchor(toPos);
    return svg`<line x1=${from.x} y1=${from.y} x2=${to.x} y2=${to.y} stroke="#94a3b8" stroke-width="2"></line>`;
  }

  render() {
    if (!this.store) return html``;
    return html`
      <div class="surface" @click=${this._onCanvasClick}>
        <svg class="edges">
          ${this.store.edges.map((edge: GraphEdge) => this._renderEdge(edge))}
        </svg>
        ${this.store.nodes.map((node: GraphNode) => html`
          <flow-node
            .nodeId=${node.id}
            .blockType=${node.type}
            .category=${this._categoryFor(node.type)}
            .x=${cellToPixel(node.x)}
            .y=${cellToPixel(node.y)}
            .selected=${node.id === this.store.selectedNodeId}
            @flow-node-selected=${this._onNodeSelected}
            @flow-node-moved=${this._onNodeMoved}
            @flow-node-connected=${this._onNodeConnected}
          ></flow-node>
        `)}
      </div>
    `;
  }

  _onNodeSelected(event: CustomEvent<{ nodeId: string }>): void {
    this.store.selectNode(event.detail.nodeId);
  }

  _onNodeMoved(event: CustomEvent<{ nodeId: string; x: number; y: number }>): void {
    const { nodeId, x, y } = event.detail;
    this.store.moveNode(nodeId, pixelToCell(x), pixelToCell(y));
  }

  _onNodeConnected(event: CustomEvent<{ from: string; kind: GraphEdge["kind"]; to: string }>): void {
    const { from, kind, to } = event.detail;
    this.store.addEdge(from, to, kind);
  }

  _onCanvasClick(): void {
    this.store.selectNode(null);
  }
}

if (!customElements.get("flow-canvas")) {
  customElements.define("flow-canvas", FlowCanvas);
}

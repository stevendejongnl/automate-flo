import { LitElement, html, css } from "lit";
import { cellToPixel, pixelToCell } from "../helpers/grid.js";
import "./flow-node.js";

class FlowCanvas extends LitElement {
  static properties = {
    store: { type: Object, attribute: false },
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
      width: 100%;
      height: 100%;
    }
  `;

  constructor() {
    super();
    this._unsubscribe = null;
  }

  connectedCallback() {
    super.connectedCallback();
    if (this.store) {
      this._unsubscribe = this.store.onChange(() => this.requestUpdate());
    }
  }

  disconnectedCallback() {
    super.disconnectedCallback();
    if (this._unsubscribe) {
      this._unsubscribe();
    }
  }

  render() {
    if (!this.store) return html``;
    return html`
      <div class="surface" @click=${this._onCanvasClick}>
        ${this.store.nodes.map(node => html`
          <flow-node
            .nodeId=${node.id}
            .nodeType=${node.type}
            .x=${cellToPixel(node.x)}
            .y=${cellToPixel(node.y)}
            .selected=${node.id === this.store.selectedNodeId}
            @flow-node-selected=${this._onNodeSelected}
            @flow-node-moved=${this._onNodeMoved}
          ></flow-node>
        `)}
      </div>
    `;
  }

  _onNodeSelected(event) {
    this.store.selectNode(event.detail.nodeId);
  }

  _onNodeMoved(event) {
    const { nodeId, x, y } = event.detail;
    this.store.moveNode(nodeId, pixelToCell(x), pixelToCell(y));
  }

  _onCanvasClick() {
    this.store.selectNode(null);
  }
}

if (!customElements.get("flow-canvas")) {
  customElements.define("flow-canvas", FlowCanvas);
}

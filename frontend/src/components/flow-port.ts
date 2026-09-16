import { LitElement, html, css } from "lit";
import type { EdgeKind } from "../types.js";

export class FlowPort extends LitElement {
  static properties = {
    kind: { type: String },
  };

  declare kind: EdgeKind;

  static styles = css`
    :host {
      display: inline-block;
      width: 10px;
      height: 10px;
    }
    .dot {
      width: 100%;
      height: 100%;
      border-radius: 50%;
      background: #2563eb;
      border: 2px solid white;
      cursor: crosshair;
    }
    .dot:hover {
      background: #1d4ed8;
    }
  `;

  constructor() {
    super();
    this._onPointerUp = this._onPointerUp.bind(this);
  }

  _onPointerDown(event: PointerEvent): void {
    event.stopPropagation();
    try {
      (event.target as Element).setPointerCapture(event.pointerId);
    } catch (e) {
      // not supported in jsdom, fine
    }
    window.addEventListener('pointerup', this._onPointerUp);
  }

  _onPointerUp(event: PointerEvent): void {
    window.removeEventListener('pointerup', this._onPointerUp);
    const dropEl = document.elementFromPoint(event.clientX, event.clientY);
    if (!dropEl) return;
    const targetFlowNode = findFlowNodeAncestor(dropEl);
    if (!targetFlowNode) return;
    const targetNodeId = (targetFlowNode as unknown as { nodeId: string }).nodeId;
    this.dispatchEvent(new CustomEvent("flow-port-connected", {
      detail: { kind: this.kind, targetNodeId },
      bubbles: true,
      composed: true,
    }));
  }

  render() {
    return html`<div class="dot" @pointerdown=${this._onPointerDown}></div>`;
  }
}

function findFlowNodeAncestor(el: Element): Element | null {
  let node: Node | null = el;
  while (node) {
    if (node instanceof Element && node.tagName.toLowerCase() === "flow-node") {
      return node;
    }
    const root = node.getRootNode();
    node = root instanceof ShadowRoot ? root.host : null;
  }
  return null;
}

if (!customElements.get("flow-port")) {
  customElements.define("flow-port", FlowPort);
}

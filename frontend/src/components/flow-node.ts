import { LitElement, html, css } from "lit";

export class FlowNode extends LitElement {
  static properties = {
    nodeId: { type: String },
    blockType: { type: String },
    x: { type: Number },
    y: { type: Number },
    selected: { type: Boolean, reflect: false, attribute: false, hasChanged: (newVal: boolean, oldVal: boolean) => newVal !== oldVal },
  };

  static styles = css`
    :host {
      position: absolute;
      display: block;
    }
    .card {
      border: 1px solid #888;
      border-radius: 4px;
      background: white;
      padding: 6px 10px;
      cursor: grab;
      user-select: none;
      min-width: 80px;
    }
    .card.selected {
      border-color: #2563eb;
      box-shadow: 0 0 0 2px #2563eb;
    }
    .type { font-weight: bold; }
    .id { font-size: 11px; color: #888; }
  `;

  declare nodeId: string;
  declare blockType: string;
  declare x: number;
  declare y: number;
  declare selected: boolean;

  private _dragStartPointer: { x: number; y: number } | null = null;
  private _dragStartPos: { x: number; y: number } | null = null;

  constructor() {
    super();
    this._dragStartPointer = null;
    this._dragStartPos = null;
    this._onPointerMove = this._onPointerMove.bind(this);
    this._onPointerUp = this._onPointerUp.bind(this);
  }

  updated(changedProperties: Map<string, unknown>): void {
    if (changedProperties.has('x') || changedProperties.has('y')) {
      this.style.left = `${this.x}px`;
      this.style.top = `${this.y}px`;
    }
  }

  _onClick(event: MouseEvent): void {
    event.stopPropagation();
    this.dispatchEvent(new CustomEvent('flow-node-selected', {
      detail: { nodeId: this.nodeId },
      bubbles: true,
      composed: true,
    }));
  }

  _onPointerDown(event: PointerEvent): void {
    event.stopPropagation();
    this._dragStartPointer = { x: event.clientX, y: event.clientY };
    this._dragStartPos = { x: this.x, y: this.y };
    try {
      (event.target as Element).setPointerCapture(event.pointerId);
    } catch (e) {
      // not supported in jsdom, fine
    }
    this.addEventListener('pointermove', this._onPointerMove);
    this.addEventListener('pointerup', this._onPointerUp);
  }

  _onPointerMove(event: PointerEvent): void {
    if (!this._dragStartPointer) return;
    const dx = event.clientX - this._dragStartPointer.x;
    const dy = event.clientY - this._dragStartPointer.y;
    this.dispatchEvent(new CustomEvent('flow-node-moved', {
      detail: { nodeId: this.nodeId, x: this._dragStartPos!.x + dx, y: this._dragStartPos!.y + dy },
      bubbles: true,
      composed: true,
    }));
  }

  _onPointerUp(_event: PointerEvent): void {
    this._dragStartPointer = null;
    this._dragStartPos = null;
    this.removeEventListener('pointermove', this._onPointerMove);
    this.removeEventListener('pointerup', this._onPointerUp);
  }

  render() {
    return html`
      <div class="card ${this.selected ? 'selected' : ''}"
           @pointerdown=${this._onPointerDown}
           @click=${this._onClick}>
        <div class="type">${this.blockType}</div>
        <div class="id">${this.nodeId}</div>
      </div>
    `;
  }
}

if (!customElements.get("flow-node")) {
  customElements.define("flow-node", FlowNode);
}

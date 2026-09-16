import { LitElement, html, css } from "lit";
import { getBlockSchemas } from "../helpers/schema-cache.js";
import { FlowStore } from "../helpers/flow-store.js";
import type { BlockSchema } from "../types.js";
import type { GraphNode } from "../types.js";
import "./inspector-field.js";

export class NodeInspector extends LitElement {
  static properties = {
    store: { type: Object, attribute: false },
    _schemas: { type: Array, state: true },
  };

  declare store: FlowStore;
  declare _schemas: BlockSchema[];

  private _unsubscribe: (() => void) | null = null;

  constructor() {
    super();
    this._schemas = [];
  }

  connectedCallback(): void {
    super.connectedCallback();
    if (this.store) {
      this._unsubscribe = this.store.onChange(() => this.requestUpdate());
    }
    this._loadSchemas();
  }

  disconnectedCallback(): void {
    super.disconnectedCallback();
    if (this._unsubscribe) {
      this._unsubscribe();
    }
  }

  get _selectedNode(): GraphNode | undefined {
    return this.store?.nodes.find(n => n.id === this.store.selectedNodeId);
  }

  get _selectedSchema(): BlockSchema | undefined {
    return this._schemas.find(s => s.type_name === this._selectedNode?.type);
  }

  static styles = css`
    :host {
      display: block;
      padding: 8px;
      overflow-y: auto;
    }
    h3 {
      margin-top: 0;
    }
  `;

  async _loadSchemas(): Promise<void> {
    try {
      this._schemas = await getBlockSchemas();
    } catch {
      this._schemas = [];
    }
  }

  _onFieldChanged(event: CustomEvent<{ fieldName: string; value: unknown }>): void {
    this.store.updateNodeFields(this._selectedNode!.id, { [event.detail.fieldName]: event.detail.value });
  }

  render() {
    if (!this._selectedNode) {
      return html`<p class="empty">No node selected</p>`;
    }
    if (!this._selectedSchema) {
      return html`<p class="empty">Loading...</p>`;
    }
    const node = this._selectedNode!;
    const schema = this._selectedSchema!;
    return html`
      <h3>${schema.type_name}</h3>
      ${schema.fields.map(field => html`
        <inspector-field
          .fieldName=${field.name}
          .fieldKind=${field.kind}
          .value=${node.fields[field.name]}
          .required=${field.required}
          @field-changed=${this._onFieldChanged}
        ></inspector-field>
      `)}
    `;
  }
}

if (!customElements.get("node-inspector")) {
  customElements.define("node-inspector", NodeInspector);
}

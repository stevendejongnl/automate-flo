import { LitElement, html, css } from "lit";
import { fetchBlockSchemas } from "../helpers/api-client.js";
import "./inspector-field.js";

class NodeInspector extends LitElement {
  static properties = {
    store: { type: Object, attribute: false },
    _schemas: { type: Array, state: true, default: [] },
  };

  constructor() {
    super();
    this._schemas = [];
  }

  connectedCallback() {
    super.connectedCallback();
    if (this.store) {
      this._unsubscribe = this.store.onChange(() => this.requestUpdate());
    }
    this._loadSchemas();
  }

  disconnectedCallback() {
    super.disconnectedCallback();
    if (this._unsubscribe) {
      this._unsubscribe();
    }
  }

  get _selectedNode() {
    return this.store?.nodes.find(n => n.id === this.store.selectedNodeId);
  }

  get _selectedSchema() {
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

  async _loadSchemas() {
    try {
      this._schemas = await fetchBlockSchemas();
    } catch {
      this._schemas = [];
    }
  }

  _onFieldChanged(event) {
    this.store.updateNodeFields(this._selectedNode.id, { [event.detail.fieldName]: event.detail.value });
  }

  render() {
    if (!this._selectedNode) {
      return html`<p class="empty">No node selected</p>`;
    }
    if (!this._selectedSchema) {
      return html`<p class="empty">Loading...</p>`;
    }
    return html`
      <h3>${this._selectedNode.type}</h3>
      ${this._selectedSchema.fields.map(field => html`
        <inspector-field
          .fieldName=${field.name}
          .fieldKind=${field.kind}
          .value=${this._selectedNode.fields[field.name]}
          @field-changed=${this._onFieldChanged}
        ></inspector-field>
      `)}
    `;
  }
}

if (!customElements.get("node-inspector")) {
  customElements.define("node-inspector", NodeInspector);
}

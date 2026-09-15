import { LitElement, html, css } from "lit";
import { fetchBlockSchemas } from "../helpers/api-client.js";
import "./palette-item.js";

class BlockPalette extends LitElement {
  static properties = {
    _schemas: { type: Array, state: true },
    _query: { type: String, state: true },
    _error: { type: String, state: true },
  };

  constructor() {
    super();
    this._schemas = [];
    this._query = "";
    this._error = null;
  }

  async connectedCallback() {
    super.connectedCallback();
    await this._loadSchemas();
  }

  async _loadSchemas() {
    try {
      const result = await fetchBlockSchemas();
      this._schemas = result;
    } catch (error) {
      this._error = error.message;
    }
  }

  get _filteredSchemas() {
    return this._schemas.filter(schema =>
      schema.type_name.toLowerCase().includes(this._query.toLowerCase())
    );
  }

  get _groupedSchemas() {
    const grouped = { action: [], decision: [] };
    for (const schema of this._filteredSchemas) {
      if (schema.category === "action") {
        grouped.action.push(schema);
      } else if (schema.category === "decision") {
        grouped.decision.push(schema);
      }
    }
    return grouped;
  }

  render() {
    return html`
      <input type="search" .value=${this._query} @input=${e => this._query = e.target.value} />
      ${this._error ? html`<p class="error">${this._error}</p>` : null}
      ${["action", "decision"].map(category => {
        if (this._groupedSchemas[category].length > 0) {
          return html`
            <h3>${category}</h3>
            ${this._groupedSchemas[category].map(schema => html`
              <palette-item .typeName=${schema.type_name} .docSummary=${schema.doc_summary}></palette-item>
            `)}
          `;
        }
        return null;
      })}
    `;
  }

  static styles = css`
    :host {
      display: flex;
      flex-direction: column;
      height: 100%;
      overflow-y: auto;
    }
    .error {
      color: red;
    }
  `;
}

if (!customElements.get("block-palette")) {
  customElements.define("block-palette", BlockPalette);
}

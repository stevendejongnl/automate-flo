import { LitElement, html, css } from "lit";
import { FlowStore } from "../helpers/flow-store.js";
import { importFlow, exportFlow } from "../helpers/api-client.js";
import { getBlockSchemas } from "../helpers/schema-cache.js";
import { graphHasEmptyRequiredFields } from "../helpers/validation.js";
import type { BlockSchema } from "../types.js";

export class AppToolbar extends LitElement {
  static properties = {
    store: { type: Object, attribute: false },
    _schemas: { type: Array, state: true },
    _errorMessage: { type: String, state: true },
  };

  declare store: FlowStore;
  declare _schemas: BlockSchema[];
  declare _errorMessage: string | null;

  constructor() {
    super();
    this._schemas = [];
    this._errorMessage = null;
  }

  connectedCallback(): void {
    super.connectedCallback();
    this._loadSchemas();
  }

  async _loadSchemas(): Promise<void> {
    try {
      this._schemas = await getBlockSchemas();
    } catch {
      this._schemas = [];
    }
  }

  static styles = css`
    :host {
      display: flex;
      align-items: center;
      gap: 8px;
      padding: 8px;
    }
    button {
      padding: 4px 12px;
    }
    .error {
      color: #dc2626;
      font-size: 13px;
    }
  `;

  render() {
    return html`
      <button @click=${this._onNew}>New</button>
      <button @click=${this._onOpenClick}>Open</button>
      <input type="file" accept=".flo" style="display: none" @change=${this._onFileSelected} />
      <button @click=${this._onSave}>Save</button>
      ${this._errorMessage ? html`<span class="error">${this._errorMessage}</span>` : null}
    `;
  }

  _onNew(): void {
    this._errorMessage = null;
    this.store.loadGraph({ next_id: 0, nodes: [], edges: [] });
  }

  _onOpenClick(): void {
    this._errorMessage = null;
    this.renderRoot.querySelector<HTMLInputElement>("input[type='file']")?.click();
  }

  async _onFileSelected(event: Event): Promise<void> {
    const input = event.target as HTMLInputElement;
    this._errorMessage = null;
    try {
      const file = input.files?.[0];
      if (!file) return;
      const bytes = await file.arrayBuffer();
      const graph = await importFlow(bytes);
      this.store.loadGraph(graph);
    } catch (error) {
      this._errorMessage = error instanceof Error ? error.message : String(error);
    } finally {
      input.value = "";
    }
  }

  async _onSave(): Promise<void> {
    if (graphHasEmptyRequiredFields(this.store.nodes, this._schemas)) {
      this._errorMessage = "Fill in all required fields before saving.";
      return;
    }
    this._errorMessage = null;
    try {
      const graph = this.store.toGraph();
      const bytes = await exportFlow(graph);
      const blob = new Blob([bytes], { type: "application/octet-stream" });
      const url = URL.createObjectURL(blob);
      const a = document.createElement("a");
      a.href = url;
      a.download = "flow.flo";
      a.click();
      URL.revokeObjectURL(url);
    } catch (error) {
      this._errorMessage = error instanceof Error ? error.message : String(error);
    }
  }
}

if (!customElements.get("app-toolbar")) {
  customElements.define("app-toolbar", AppToolbar);
}

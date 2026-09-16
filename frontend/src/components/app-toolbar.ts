import { LitElement, html, css } from "lit";
import { FlowStore } from "../helpers/flow-store.js";
import { importFlow, exportFlow } from "../helpers/api-client.js";

export class AppToolbar extends LitElement {
  static properties = {
    store: { type: Object, attribute: false },
  };

  declare store: FlowStore;

  static styles = css`
    :host {
      display: flex;
      gap: 8px;
      padding: 8px;
    }
    button {
      padding: 4px 12px;
    }
  `;

  render() {
    return html`
      <button @click=${this._onNew}>New</button>
      <button @click=${this._onOpenClick}>Open</button>
      <input type="file" accept=".flo" style="display: none" @change=${this._onFileSelected} />
      <button @click=${this._onSave}>Save</button>
    `;
  }

  _onNew(): void {
    this.store.loadGraph({ next_id: 0, nodes: [], edges: [] });
  }

  _onOpenClick(): void {
    this.renderRoot.querySelector<HTMLInputElement>("input[type='file']")?.click();
  }

  async _onFileSelected(event: Event): Promise<void> {
    const input = event.target as HTMLInputElement;
    const file = input.files?.[0];
    if (!file) return;
    const bytes = await file.arrayBuffer();
    const graph = await importFlow(bytes);
    this.store.loadGraph(graph);
    input.value = "";
  }

  async _onSave(): Promise<void> {
    const graph = this.store.toGraph();
    const bytes = await exportFlow(graph);
    const blob = new Blob([bytes], { type: "application/octet-stream" });
    const url = URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = "flow.flo";
    a.click();
    URL.revokeObjectURL(url);
  }
}

if (!customElements.get("app-toolbar")) {
  customElements.define("app-toolbar", AppToolbar);
}

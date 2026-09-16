import { LitElement, html, css } from 'lit';

export class PaletteItem extends LitElement {
  static properties = {
    typeName: { type: String, reflect: true },
    docSummary: { type: String, reflect: true },
  };

  declare typeName: string;
  declare docSummary: string;

  static styles = css`
    .item {
      cursor: pointer;
      padding: 8px;
      border: 1px solid #ccc;
      border-radius: 4px;
      margin: 4px;
    }
    .name {
      font-weight: bold;
      font-size: 16px;
      color: #333;
    }
    .doc {
      font-size: 14px;
      color: #666;
    }
  `;

  _onClick() {
    this.dispatchEvent(new CustomEvent('palette-item-selected', {
      detail: { typeName: this.typeName },
      bubbles: true,
      composed: true,
    }));
  }

  render() {
    return html`
      <div class="item" @click=${this._onClick} tabindex="0" role="button">
        <div class="name">${this.typeName}</div>
        <div class="doc">${this.docSummary}</div>
      </div>
    `;
  }
}

if (!customElements.get("palette-item")) {
  customElements.define("palette-item", PaletteItem);
}

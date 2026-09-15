import { LitElement, html, css } from "lit";

class InspectorField extends LitElement {
  static properties = {
    fieldName: { type: String },
    fieldKind: { type: String },
    value: { type: Object },
  };

  static styles = css`
    :host { display: block; margin-bottom: 8px; }
    label { display: block; font-size: 12px; color: #555; margin-bottom: 2px; }
    input { width: 100%; box-sizing: border-box; padding: 4px 6px; font-size: 13px; }
    input[type="checkbox"] { width: auto; }
  `;

  render() {
    return html`
      <label>${this.fieldName}</label>
      ${this._renderInput()}
    `;
  }

  _renderInput() {
    if (this.fieldKind === "boolean") {
      return html`<input type="checkbox" .checked=${!!this.value} @change=${this._onChange} />`;
    } else if (this.fieldKind === "number") {
      return html`<input type="number" .value=${this.value ?? ""} @change=${this._onChange} />`;
    } else {
      return html`<input type="text" .value=${this.value ?? ""} @change=${this._onChange} />`;
    }
  }

  _onChange(event) {
    let newValue;
    if (this.fieldKind === "boolean") {
      newValue = event.target.checked;
    } else if (this.fieldKind === "number") {
      newValue = event.target.valueAsNumber;
    } else {
      newValue = event.target.value;
    }
    this.dispatchEvent(new CustomEvent("field-changed", {
      detail: { fieldName: this.fieldName, value: newValue },
      bubbles: true,
      composed: true,
    }));
  }
}

if (!customElements.get("inspector-field")) {
  customElements.define("inspector-field", InspectorField);
}

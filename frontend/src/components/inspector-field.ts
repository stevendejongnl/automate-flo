import { LitElement, html, css } from "lit";
import type { FieldKind } from "../types.js";
import { isFieldEmpty } from "../helpers/validation.js";

export class InspectorField extends LitElement {
  static properties = {
    fieldName: { type: String },
    fieldKind: { type: String },
    value: { type: Object },
    required: { type: Boolean },
  };

  declare fieldName: string;
  declare fieldKind: FieldKind;
  declare value: unknown;
  declare required: boolean;

  static styles = css`
    :host { display: block; margin-bottom: 8px; }
    label { display: block; font-size: 12px; color: #555; margin-bottom: 2px; }
    input { width: 100%; box-sizing: border-box; padding: 4px 6px; font-size: 13px; }
    input[type="checkbox"] { width: auto; }
    input.missing { border-color: #dc2626; background: #fef2f2; }
  `;

  get _isMissing(): boolean {
    return this.required && isFieldEmpty(this.fieldKind, this.value);
  }

  render() {
    return html`
      <label>${this.fieldName}</label>
      ${this._renderInput()}
    `;
  }

  _renderInput() {
    const missingClass = this._isMissing ? "missing" : "";
    if (this.fieldKind === "boolean") {
      return html`<input type="checkbox" class=${missingClass} .checked=${!!this.value} @change=${this._onChange} />`;
    } else if (this.fieldKind === "number") {
      return html`<input type="number" class=${missingClass} .value=${this.value ?? ""} @change=${this._onChange} />`;
    } else {
      return html`<input type="text" class=${missingClass} .value=${this.value ?? ""} @change=${this._onChange} />`;
    }
  }

  _onChange(event: Event): void {
    const target = event.target as HTMLInputElement;
    let newValue: boolean | number | string;
    if (this.fieldKind === "boolean") {
      newValue = target.checked;
    } else if (this.fieldKind === "number") {
      newValue = target.valueAsNumber;
    } else {
      newValue = target.value;
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

import { LitElement, svg } from "lit";
import type { Point } from "../helpers/port-geometry.js";

export class EdgeLine extends LitElement {
  static properties = {
    from: { type: Object, attribute: false },
    to: { type: Object, attribute: false },
  };

  declare from: Point;
  declare to: Point;

  createRenderRoot() {
    return this;
  }

  render() {
    return svg`
      <line
        x1=${this.from.x}
        y1=${this.from.y}
        x2=${this.to.x}
        y2=${this.to.y}
        stroke="#94a3b8"
        stroke-width="2"
      ></line>
    `;
  }
}

if (!customElements.get("edge-line")) {
  customElements.define("edge-line", EdgeLine);
}

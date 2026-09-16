import { LitElement, html, css } from 'lit';

export class AppShell extends LitElement {
  static styles = css`
    :host {
      display: grid;
      grid-template-columns: 240px 1fr 280px;
      grid-template-rows: auto 1fr;
      grid-template-areas:
        "toolbar toolbar toolbar"
        "palette canvas inspector";
      height: 100vh;
    }
    .toolbar { grid-area: toolbar; }
    .palette { grid-area: palette; overflow-y: auto; }
    .canvas { grid-area: canvas; overflow: auto; }
    .inspector { grid-area: inspector; overflow-y: auto; }
  `;

  render() {
    return html`
      <div class="toolbar"><slot name="toolbar"></slot></div>
      <div class="palette"><slot name="palette"></slot></div>
      <div class="canvas"><slot name="canvas"></slot></div>
      <div class="inspector"><slot name="inspector"></slot></div>
    `;
  }
}

if (!customElements.get("app-shell")) {
  customElements.define("app-shell", AppShell);
}

import { describe, it, expect, vi, beforeEach, afterEach } from "vitest";
import "./flow-node.js";

describe("FlowNode", () => {
  let el;

  beforeEach(() => {
    el = document.createElement("flow-node");
    document.body.appendChild(el);
  });

  afterEach(() => {
    document.body.removeChild(el);
  });

  it("renders nodeType and nodeId text in its shadow DOM", async () => {
    el.nodeType = "Delay";
    el.nodeId = "n1";
    await el.updateComplete;
    expect(el.shadowRoot.querySelector(".type").textContent).toBe("Delay");
    expect(el.shadowRoot.querySelector(".id").textContent).toBe("n1");
  });

  it("has class 'selected' on the .card div when `selected` is true, and does not have it when `selected` is false", async () => {
    el.selected = true;
    await el.updateComplete;
    expect(el.shadowRoot.querySelector(".card").classList.contains("selected")).toBe(true);
    el.selected = false;
    await el.updateComplete;
    expect(el.shadowRoot.querySelector(".card").classList.contains("selected")).toBe(false);
  });

  it("sets `this.style.left`/`this.style.top` based on `x`/`y` properties", async () => {
    el.x = 32;
    el.y = 48;
    await el.updateComplete;
    expect(el.style.left).toBe("32px");
    expect(el.style.top).toBe("48px");
  });

  it("clicking the `.card` div dispatches a 'flow-node-selected' event with `detail.nodeId` matching", () => {
    const spy = vi.fn();
    el.addEventListener('flow-node-selected', spy);
    el.shadowRoot.querySelector(".card").click();
    expect(spy).toHaveBeenCalledWith(expect.objectContaining({ detail: { nodeId: el.nodeId } }));
  });

  it("a simplified drag test", async () => {
    el.x = 32;
    el.y = 48;
    await el.updateComplete;

    const pointerdown = new MouseEvent("pointerdown", { clientX: 100, clientY: 100, bubbles: true });
    pointerdown.pointerId = 1;
    el.shadowRoot.querySelector(".card").dispatchEvent(pointerdown);

    const spy = vi.fn();
    el.addEventListener('flow-node-moved', spy);

    const pointermove = new MouseEvent("pointermove", { clientX: 120, clientY: 115, bubbles: true });
    pointermove.pointerId = 1;
    el.dispatchEvent(pointermove);
    await el.updateComplete;
    expect(spy).toHaveBeenCalledWith(expect.objectContaining({ detail: { nodeId: el.nodeId, x: 52, y: 63 } }));
  });
});

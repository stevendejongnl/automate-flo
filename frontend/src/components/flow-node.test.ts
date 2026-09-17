import { describe, it, expect, vi, beforeEach, afterEach } from "vitest";
import "./flow-node.js";
import type { FlowNode } from "./flow-node.js";
import { createEl } from "../helpers/test-utils.js";

describe("FlowNode", () => {
  let el: FlowNode;

  beforeEach(() => {
    el = createEl<FlowNode>("flow-node");
    document.body.appendChild(el);
  });

  afterEach(() => {
    document.body.removeChild(el);
  });

  it("renders blockType and nodeId text in its shadow DOM", async () => {
    el.blockType = "Delay";
    el.nodeId = "n1";
    await el.updateComplete;
    expect(el.shadowRoot!.querySelector(".type")!.textContent).toBe("Delay");
    expect(el.shadowRoot!.querySelector(".id")!.textContent).toBe("n1");
  });

  it("has class 'selected' on the .card div when `selected` is true, and does not have it when `selected` is false", async () => {
    el.selected = true;
    await el.updateComplete;
    expect(el.shadowRoot!.querySelector(".card")!.classList.contains("selected")).toBe(true);
    el.selected = false;
    await el.updateComplete;
    expect(el.shadowRoot!.querySelector(".card")!.classList.contains("selected")).toBe(false);
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
    el.shadowRoot!.querySelector<HTMLElement>(".card")!.click();
    expect(spy).toHaveBeenCalledWith(expect.objectContaining({ detail: { nodeId: el.nodeId } }));
  });

  it("a simplified drag test", async () => {
    el.x = 32;
    el.y = 48;
    await el.updateComplete;

    const pointerdown = Object.assign(new MouseEvent("pointerdown", { clientX: 100, clientY: 100, bubbles: true }), { pointerId: 1 });
    el.shadowRoot!.querySelector(".card")!.dispatchEvent(pointerdown);

    const spy = vi.fn();
    el.addEventListener('flow-node-moved', spy);

    const pointermove = Object.assign(new MouseEvent("pointermove", { clientX: 120, clientY: 115, bubbles: true }), { pointerId: 1 });
    el.dispatchEvent(pointermove);
    await el.updateComplete;
    expect(spy).toHaveBeenCalledWith(expect.objectContaining({ detail: { nodeId: el.nodeId, x: 52, y: 63 } }));
  });

  it("renders one .port for an action-category node", async () => {
    el.category = "action";
    await el.updateComplete;
    const ports = el.shadowRoot!.querySelectorAll(".port");
    expect(ports).toHaveLength(1);
    expect(ports[0].classList.contains("port-complete")).toBe(true);
  });

  it("renders two .port elements for a decision-category node", async () => {
    el.category = "decision";
    await el.updateComplete;
    const ports = el.shadowRoot!.querySelectorAll(".port");
    expect(ports).toHaveLength(2);
    expect(ports[0].classList.contains("port-positive")).toBe(true);
    expect(ports[1].classList.contains("port-negative")).toBe(true);
  });

  it("re-dispatches a port's 'flow-port-connected' event as 'flow-node-connected' with its own id as 'from'", async () => {
    el.nodeId = "n1";
    el.category = "action";
    await el.updateComplete;
    const spy = vi.fn();
    el.addEventListener('flow-node-connected', spy);
    const port = el.shadowRoot!.querySelector("flow-port")!;
    port.dispatchEvent(new CustomEvent('flow-port-connected', {
      detail: { kind: "complete", targetNodeId: "n2" },
      bubbles: true,
      composed: true,
    }));
    expect(spy).toHaveBeenCalledWith(expect.objectContaining({ detail: { from: "n1", kind: "complete", to: "n2" } }));
  });
});

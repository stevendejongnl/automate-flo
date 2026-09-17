import { describe, it, expect, vi, beforeEach, afterEach } from "vitest";
import "./flow-port.js";
import type { FlowPort } from "./flow-port.js";
import "./flow-node.js";
import type { FlowNode } from "./flow-node.js";
import { createEl } from "../helpers/test-utils.js";

describe("FlowPort", () => {
  let el: FlowPort;
  let flowNode: FlowNode;
  // jsdom doesn't implement document.elementFromPoint at all, so it must be
  // assigned directly (vi.spyOn requires the property to already exist).
  const mockElementFromPoint = vi.fn<(x: number, y: number) => Element | null>();

  beforeEach(() => {
    el = createEl<FlowPort>("flow-port");
    flowNode = createEl<FlowNode>("flow-node");
    flowNode.nodeId = "n2";
    document.body.appendChild(el);
    document.body.appendChild(flowNode);
    document.elementFromPoint = mockElementFromPoint;
  });

  afterEach(() => {
    document.body.removeChild(el);
    document.body.removeChild(flowNode);
    mockElementFromPoint.mockReset();
  });

  it("renders a .dot element in its shadow DOM", () => {
    expect(el.shadowRoot!.querySelector(".dot")).not.toBeNull();
  });

  it("dispatches a 'flow-port-connected' event on pointerup", () => {
    el.kind = "complete";
    const spy = vi.fn();
    el.addEventListener('flow-port-connected', spy);
    const pointerdown = Object.assign(new MouseEvent("pointerdown", { clientX: 10, clientY: 10, bubbles: true }), { pointerId: 1 });
    el.shadowRoot!.querySelector<HTMLElement>(".dot")!.dispatchEvent(pointerdown);
    mockElementFromPoint.mockReturnValue(flowNode.shadowRoot!.querySelector(".card")!);
    const pointerup = Object.assign(new MouseEvent("pointerup", { clientX: 50, clientY: 50 }), { pointerId: 1 });
    window.dispatchEvent(pointerup);
    expect(spy).toHaveBeenCalledWith(expect.objectContaining({ detail: { kind: "complete", targetNodeId: "n2" } }));
  });

  it("does not dispatch a 'flow-port-connected' event if no flow-node ancestor is found", () => {
    const spy = vi.fn();
    el.addEventListener('flow-port-connected', spy);
    const pointerdown = Object.assign(new MouseEvent("pointerdown", { clientX: 10, clientY: 10, bubbles: true }), { pointerId: 1 });
    el.shadowRoot!.querySelector<HTMLElement>(".dot")!.dispatchEvent(pointerdown);
    mockElementFromPoint.mockReturnValue(document.body);
    const pointerup = Object.assign(new MouseEvent("pointerup", { clientX: 50, clientY: 50 }), { pointerId: 1 });
    window.dispatchEvent(pointerup);
    expect(spy).not.toHaveBeenCalled();
  });
});

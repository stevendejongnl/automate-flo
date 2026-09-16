import { describe, it, expect } from "vitest";
import "./edge-line.js";
import type { EdgeLine } from "./edge-line.js";
import { createEl } from "../helpers/test-utils.js";

describe("EdgeLine", () => {
  it("renders a line between two points", async () => {
    const el = createEl<EdgeLine>("edge-line");
    el.from = { x: 0, y: 0 };
    el.to = { x: 100, y: 50 };
    document.body.appendChild(el);
    await el.updateComplete;
    const line = el.querySelector("line");
    expect(line).not.toBeNull();
    expect(line!.getAttribute("x1")).toBe("0");
    expect(line!.getAttribute("y1")).toBe("0");
    expect(line!.getAttribute("x2")).toBe("100");
    expect(line!.getAttribute("y2")).toBe("50");
  });

  it("does not have a shadow root", () => {
    const el = createEl<EdgeLine>("edge-line");
    expect(el.shadowRoot).toBeNull();
  });
});

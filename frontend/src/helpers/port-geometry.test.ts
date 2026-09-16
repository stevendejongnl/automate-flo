import { describe, it, expect } from "vitest";
import { inputAnchor, outputAnchor } from "./port-geometry.js";

describe("port-geometry", () => {
  it("inputAnchor", () => {
    expect(inputAnchor({ x: 100, y: 200 })).toEqual({ x: 100, y: 220 });
  });

  it("outputAnchor action", () => {
    expect(outputAnchor({ x: 100, y: 200 }, "complete", "action")).toEqual({ x: 180, y: 220 });
  });

  it("outputAnchor decision positive", () => {
    const point = outputAnchor({ x: 100, y: 200 }, "positive", "decision");
    expect(point.x).toBe(180);
    expect(point.y).toBeCloseTo(213.33, 1);
  });

  it("outputAnchor decision negative", () => {
    const point = outputAnchor({ x: 100, y: 200 }, "negative", "decision");
    expect(point.x).toBe(180);
    expect(point.y).toBeCloseTo(226.67, 1);
  });

  it("outputAnchor decision positive and negative have different y values", () => {
    const positiveY = outputAnchor({ x: 100, y: 200 }, "positive", "decision").y;
    const negativeY = outputAnchor({ x: 100, y: 200 }, "negative", "decision").y;
    expect(positiveY).not.toEqual(negativeY);
  });

  it("outputAnchor decision positive and negative have the same x", () => {
    const positiveX = outputAnchor({ x: 100, y: 200 }, "positive", "decision").x;
    const negativeX = outputAnchor({ x: 100, y: 200 }, "negative", "decision").x;
    expect(positiveX).toEqual(negativeX);
  });
});

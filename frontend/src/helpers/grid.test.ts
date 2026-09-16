import { describe, it, expect } from "vitest";
import { cellToPixel, pixelToCell } from "./grid.js";

describe("grid helpers", () => {
  it("cellToPixel(0) === 0", () => {
    expect(cellToPixel(0)).toBe(0);
  });

  it("cellToPixel(6) === 96", () => {
    expect(cellToPixel(6)).toBe(96);
  });

  it("pixelToCell(96) === 6", () => {
    expect(pixelToCell(96)).toBe(6);
  });

  it("pixelToCell(100) rounds to the nearest cell", () => {
    expect(pixelToCell(100)).toBe(6);
  });

  it("round-trip: pixelToCell(cellToPixel(10)) === 10", () => {
    expect(pixelToCell(cellToPixel(10))).toBe(10);
  });
});

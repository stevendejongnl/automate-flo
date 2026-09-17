import { describe, it, expect } from "vitest";
import { createEl } from "./test-utils.js";

describe("createEl", () => {
  it("creates an element with the given tag name", () => {
    const el = createEl<HTMLDivElement>("div");
    expect(el.tagName.toLowerCase()).toBe("div");
    expect(el).toBeInstanceOf(HTMLElement);
  });
});

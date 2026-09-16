import { describe, it, expect } from "vitest";
import { isFieldEmpty, graphHasEmptyRequiredFields } from "./validation.js";
import type { BlockSchema } from "../types.js";

const schemas: BlockSchema[] = [
  {
    type_name: "Delay",
    type_id: 1046,
    category: "action",
    doc_summary: "Waits",
    fields: [
      { name: "seconds", required: true, default: null, kind: "number" },
      { name: "wakeup", required: false, default: null, kind: "boolean" },
    ],
  },
];

describe("isFieldEmpty", () => {
  it("returns true for empty string", () => {
    expect(isFieldEmpty("string", "")).toBe(true);
  });
  it("returns false for non-empty string", () => {
    expect(isFieldEmpty("string", "hello")).toBe(false);
  });
  it("returns true for null", () => {
    expect(isFieldEmpty("string", null)).toBe(true);
  });
  it("returns true for undefined", () => {
    expect(isFieldEmpty("string", undefined)).toBe(true);
  });
  it("returns true for NaN", () => {
    expect(isFieldEmpty("number", NaN)).toBe(true);
  });
  it("returns false for zero", () => {
    expect(isFieldEmpty("number", 0)).toBe(false);
  });
  it("returns false for non-NaN number", () => {
    expect(isFieldEmpty("number", 5)).toBe(false);
  });
  it("returns true for null number", () => {
    expect(isFieldEmpty("number", null)).toBe(true);
  });
  it("returns false for boolean false", () => {
    expect(isFieldEmpty("boolean", false)).toBe(false);
  });
  it("returns false for boolean true", () => {
    expect(isFieldEmpty("boolean", true)).toBe(false);
  });
  it("returns true for empty unknown", () => {
    expect(isFieldEmpty("unknown", "")).toBe(true);
  });
  it("returns false for non-empty unknown", () => {
    expect(isFieldEmpty("unknown", "x")).toBe(false);
  });
});

describe("graphHasEmptyRequiredFields", () => {
  it("returns false for node with filled required field", () => {
    expect(graphHasEmptyRequiredFields([{ id: "1", type: "Delay", x: 0, y: 0, fields: { seconds: 5 } }], schemas)).toBe(false);
  });
  it("returns true for node with empty required field", () => {
    expect(graphHasEmptyRequiredFields([{ id: "1", type: "Delay", x: 0, y: 0, fields: { seconds: NaN } }], schemas)).toBe(true);
  });
  it("returns true for node with missing required field", () => {
    expect(graphHasEmptyRequiredFields([{ id: "1", type: "Delay", x: 0, y: 0, fields: {} }], schemas)).toBe(true);
  });
  it("returns false for node of unknown type", () => {
    expect(graphHasEmptyRequiredFields([{ id: "1", type: "SomeUnknownType", x: 0, y: 0, fields: {} }], schemas)).toBe(false);
  });
  it("returns false for empty nodes array", () => {
    expect(graphHasEmptyRequiredFields([], schemas)).toBe(false);
  });
  it("returns true for multiple nodes where only one has an empty required field", () => {
    expect(graphHasEmptyRequiredFields([
      { id: "1", type: "Delay", x: 0, y: 0, fields: { seconds: 5 } },
      { id: "2", type: "Delay", x: 0, y: 0, fields: { seconds: NaN } },
    ], schemas)).toBe(true);
  });
});

import { describe, it, expect, vi, afterEach } from "vitest";
import "./inspector-field.js";
import type { InspectorField } from "./inspector-field.js";
import { createEl } from "../helpers/test-utils.js";

describe("InspectorField", () => {
  let el: InspectorField;

  afterEach(() => {
    if (el) {
      document.body.removeChild(el);
    }
  });

  it("renders a text input for string fields", async () => {
    el = createEl<InspectorField>("inspector-field");
    el.fieldName = "seconds";
    el.fieldKind = "string";
    el.value = "10";
    document.body.appendChild(el);
    await el.updateComplete;

    const input = el.shadowRoot!.querySelector<HTMLInputElement>("input[type='text']")!;
    expect(input).not.toBeNull();
    expect(input.value).toBe("10");
  });

  it("renders a number input for number fields", async () => {
    el = createEl<InspectorField>("inspector-field");
    el.fieldName = "seconds";
    el.fieldKind = "number";
    el.value = 10;
    document.body.appendChild(el);
    await el.updateComplete;

    const input = el.shadowRoot!.querySelector<HTMLInputElement>("input[type='number']")!;
    expect(input).not.toBeNull();
    expect(input.value).toBe("10");
  });

  it("renders a checkbox for boolean fields", async () => {
    el = createEl<InspectorField>("inspector-field");
    el.fieldName = "enabled";
    el.fieldKind = "boolean";
    el.value = true;
    document.body.appendChild(el);
    await el.updateComplete;

    const input = el.shadowRoot!.querySelector<HTMLInputElement>("input[type='checkbox']")!;
    expect(input).not.toBeNull();
    expect(input.checked).toBe(true);
  });

  it("fires field-changed event when text input changes", async () => {
    el = createEl<InspectorField>("inspector-field");
    el.fieldName = "seconds";
    el.fieldKind = "string";
    el.value = "10";
    document.body.appendChild(el);
    await el.updateComplete;

    const spy = vi.fn();
    el.addEventListener("field-changed", spy);

    const input = el.shadowRoot!.querySelector<HTMLInputElement>("input[type='text']")!;
    input.value = "20";
    input.dispatchEvent(new Event("change"));

    expect(spy).toHaveBeenCalledTimes(1);
    expect(spy.mock.calls[0][0].detail).toEqual({ fieldName: "seconds", value: "20" });
  });

  it("fires field-changed event when checkbox changes", async () => {
    el = createEl<InspectorField>("inspector-field");
    el.fieldName = "enabled";
    el.fieldKind = "boolean";
    el.value = true;
    document.body.appendChild(el);
    await el.updateComplete;

    const spy = vi.fn();
    el.addEventListener("field-changed", spy);

    const input = el.shadowRoot!.querySelector<HTMLInputElement>("input[type='checkbox']")!;
    input.checked = false;
    input.dispatchEvent(new Event("change"));

    expect(spy).toHaveBeenCalledTimes(1);
    expect(spy.mock.calls[0][0].detail).toEqual({ fieldName: "enabled", value: false });
  });

  it("fires field-changed event when number input changes", async () => {
    el = createEl<InspectorField>("inspector-field");
    el.fieldName = "seconds";
    el.fieldKind = "number";
    el.value = 10;
    document.body.appendChild(el);
    await el.updateComplete;

    const spy = vi.fn();
    el.addEventListener("field-changed", spy);

    const input = el.shadowRoot!.querySelector<HTMLInputElement>("input[type='number']")!;
    input.value = "20";
    input.dispatchEvent(new Event("change"));

    expect(spy).toHaveBeenCalledTimes(1);
    expect(spy.mock.calls[0][0].detail).toEqual({ fieldName: "seconds", value: 20 });
  });
});

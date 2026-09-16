import { describe, it, expect, vi, beforeEach, afterEach } from 'vitest';
import './palette-item.js';
import type { PaletteItem } from './palette-item.js';
import { createEl } from '../helpers/test-utils.js';

describe('PaletteItem', () => {
  let el: PaletteItem;

  beforeEach(() => {
    el = createEl<PaletteItem>('palette-item');
    document.body.appendChild(el);
  });

  afterEach(() => {
    document.body.removeChild(el);
  });

  it('renders with typeName and docSummary', async () => {
    el.typeName = 'Delay';
    el.docSummary = 'Waits N seconds';
    await el.updateComplete;
    expect(el.shadowRoot!.textContent).toContain('Delay');
    expect(el.shadowRoot!.textContent).toContain('Waits N seconds');
  });

  it('dispatches palette-item-selected event on click', async () => {
    el.typeName = 'Delay';
    await el.updateComplete;
    const handler = vi.fn();
    el.addEventListener('palette-item-selected', handler);
    el.shadowRoot!.querySelector<HTMLElement>('.item')!.click();
    await el.updateComplete;
    expect(handler).toHaveBeenCalledWith(expect.any(CustomEvent));
    expect(handler.mock.calls[0][0].detail.typeName).toBe('Delay');
  });
});

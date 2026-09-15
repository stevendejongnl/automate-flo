import { describe, it, expect, afterEach } from 'vitest';
import './app-shell.js';

describe('AppShell', () => {
  let el;

  afterEach(() => {
    if (el) {
      document.body.removeChild(el);
      el = null;
    }
  });

  it('renders with all slots', async () => {
    el = document.createElement('app-shell');
    document.body.appendChild(el);
    await el.updateComplete;

    expect(el.shadowRoot.querySelector('.toolbar')).not.toBeNull();
    expect(el.shadowRoot.querySelector('.palette')).not.toBeNull();
    expect(el.shadowRoot.querySelector('.canvas')).not.toBeNull();
    expect(el.shadowRoot.querySelector('.inspector')).not.toBeNull();
  });

  it('renders slotted content', async () => {
    const toolbarContent = document.createElement('div');
    toolbarContent.setAttribute('slot', 'toolbar');
    toolbarContent.textContent = 'Toolbar Content';

    el = document.createElement('app-shell');
    document.body.appendChild(el);
    el.appendChild(toolbarContent);
    await el.updateComplete;

    expect(el.querySelector('[slot="toolbar"]')).toBe(toolbarContent);
  });
});

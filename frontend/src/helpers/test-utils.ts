export function createEl<T extends HTMLElement>(tag: string): T {
  return document.createElement(tag) as T;
}

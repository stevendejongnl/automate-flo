import "./components/app-shell.js";
import "./components/block-palette.js";
import "./components/flow-canvas.js";
import "./components/node-inspector.js";
import "./components/app-toolbar.js";
import type { AppShell } from "./components/app-shell.js";
import type { FlowCanvas } from "./components/flow-canvas.js";
import type { NodeInspector } from "./components/node-inspector.js";
import type { AppToolbar } from "./components/app-toolbar.js";
import { FlowStore } from "./helpers/flow-store.js";

const store = new FlowStore();

const appShell = document.querySelector<AppShell>("app-shell")!;

const toolbar = document.createElement("app-toolbar") as AppToolbar;
toolbar.setAttribute("slot", "toolbar");
toolbar.store = store;
appShell.appendChild(toolbar);

const palette = document.createElement("block-palette");
palette.setAttribute("slot", "palette");
appShell.appendChild(palette);

const canvas = document.createElement("flow-canvas") as FlowCanvas;
canvas.setAttribute("slot", "canvas");
canvas.store = store;
appShell.appendChild(canvas);

const inspector = document.createElement("node-inspector") as NodeInspector;
inspector.setAttribute("slot", "inspector");
inspector.store = store;
appShell.appendChild(inspector);

let nextSpawnX = 0;
palette.addEventListener("palette-item-selected", ((event: CustomEvent<{ typeName: string }>) => {
  store.addNode(event.detail.typeName, nextSpawnX, 0);
  nextSpawnX += 6;
}) as EventListener);

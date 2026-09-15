import "./components/app-shell.js";
import "./components/block-palette.js";
import "./components/flow-canvas.js";
import "./components/node-inspector.js";
import { FlowStore } from "./helpers/flow-store.js";

const store = new FlowStore();

const appShell = document.querySelector("app-shell");

const palette = document.createElement("block-palette");
palette.setAttribute("slot", "palette");
appShell.appendChild(palette);

const canvas = document.createElement("flow-canvas");
canvas.setAttribute("slot", "canvas");
canvas.store = store;
appShell.appendChild(canvas);

const inspector = document.createElement("node-inspector");
inspector.setAttribute("slot", "inspector");
inspector.store = store;
appShell.appendChild(inspector);

let nextSpawnX = 0;
palette.addEventListener("palette-item-selected", (event) => {
  store.addNode(event.detail.typeName, nextSpawnX, 0);
  nextSpawnX += 6;
});

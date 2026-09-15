import "./components/app-shell.js";
import "./components/block-palette.js";

const appShell = document.querySelector("app-shell");
const palette = document.createElement("block-palette");
palette.setAttribute("slot", "palette");
appShell.appendChild(palette);

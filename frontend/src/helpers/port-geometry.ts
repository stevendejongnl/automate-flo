import type { EdgeKind, BlockCategory } from "../types.js";

export interface Point {
  x: number;
  y: number;
}

export const NODE_WIDTH_PX = 80;
export const NODE_HEIGHT_PX = 40;

export function inputAnchor(nodePos: Point): Point {
  return { x: nodePos.x, y: nodePos.y + NODE_HEIGHT_PX / 2 };
}

export function outputAnchor(nodePos: Point, kind: EdgeKind, category: BlockCategory): Point {
  if (category === "action") {
    return { x: nodePos.x + NODE_WIDTH_PX, y: nodePos.y + NODE_HEIGHT_PX / 2 };
  } else if (category === "decision") {
    if (kind === "positive") {
      return { x: nodePos.x + NODE_WIDTH_PX, y: nodePos.y + NODE_HEIGHT_PX / 3 };
    } else {
      return { x: nodePos.x + NODE_WIDTH_PX, y: nodePos.y + (2 * NODE_HEIGHT_PX) / 3 };
    }
  }
  throw new Error("Invalid category or kind");
}

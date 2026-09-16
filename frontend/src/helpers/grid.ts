export const CELL_SIZE_PX = 16;

export function cellToPixel(cellValue: number): number {
  return cellValue * CELL_SIZE_PX;
}

export function pixelToCell(pixelValue: number): number {
  return Math.round(pixelValue / CELL_SIZE_PX);
}

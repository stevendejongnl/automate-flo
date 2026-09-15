export const CELL_SIZE_PX = 16;

export function cellToPixel(cellValue) {
  return cellValue * CELL_SIZE_PX;
}

export function pixelToCell(pixelValue) {
  return Math.round(pixelValue / CELL_SIZE_PX);
}

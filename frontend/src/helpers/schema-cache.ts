import { fetchBlockSchemas } from "./api-client.js";
import type { BlockSchema } from "../types.js";

let cached: Promise<BlockSchema[]> | null = null;

export function getBlockSchemas(): Promise<BlockSchema[]> {
  if (!cached) {
    cached = fetchBlockSchemas();
  }
  return cached;
}

export function resetSchemaCache(): void {
  cached = null;
}

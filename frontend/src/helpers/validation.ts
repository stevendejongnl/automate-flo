import type { FieldKind, BlockSchema, GraphNode } from "../types.js";

export function isFieldEmpty(kind: FieldKind, value: unknown): boolean {
  if (kind === "boolean") {
    return false;
  } else if (kind === "number") {
    return value === null || value === undefined || (typeof value === "number" && Number.isNaN(value));
  } else {
    return value === null || value === undefined || value === "";
  }
}

export function graphHasEmptyRequiredFields(nodes: GraphNode[], schemas: BlockSchema[]): boolean {
  return nodes.some(node => {
    const schema = schemas.find(s => s.type_name === node.type);
    if (!schema) return false;
    return schema.fields.some(field => field.required && isFieldEmpty(field.kind, node.fields[field.name]));
  });
}

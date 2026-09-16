export interface GraphNode {
  id: string;
  type: string;
  x: number;
  y: number;
  fields: Record<string, unknown>;
}

export type EdgeKind = "complete" | "positive" | "negative";

export interface GraphEdge {
  from: string;
  to: string;
  kind: EdgeKind;
}

export interface Graph {
  next_id: number;
  nodes: GraphNode[];
  edges: GraphEdge[];
}

export type FieldKind = "string" | "number" | "boolean" | "unknown";

export interface BlockField {
  name: string;
  required: boolean;
  default: unknown;
  kind: FieldKind;
}

export type BlockCategory = "action" | "decision";

export interface BlockSchema {
  type_name: string;
  type_id: number;
  category: BlockCategory;
  doc_summary: string;
  fields: BlockField[];
}

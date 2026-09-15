from ..base import Action

TYPE_ID = 1411


class BarcodeScan(Action):
    """id 1411, UI name "Scan barcode". Extends Action directly. Fields, in order: uri, formats (generic expressions), var_raw_values, var_formats, var_bounding_boxes (VariableExpr output vars)."""
    type_id = TYPE_ID

    def __init__(self, stmt_id, cell_x=0, cell_y=0, on_complete=None, uri=None, formats=None, var_raw_values=None, var_formats=None, var_bounding_boxes=None):
        super().__init__(stmt_id, cell_x, cell_y, on_complete)
        self.uri = uri
        self.formats = formats
        self.var_raw_values = var_raw_values
        self.var_formats = var_formats
        self.var_bounding_boxes = var_bounding_boxes

    def write_fields(self, writer):
        super().write_fields(writer)
        writer.write_object(self.uri)
        writer.write_object(self.formats)
        writer.write_object(self.var_raw_values)
        writer.write_object(self.var_formats)
        writer.write_object(self.var_bounding_boxes)

    def read_fields(self, reader):
        super().read_fields(reader)
        self.uri = reader.read_object()
        self.formats = reader.read_object()
        self.var_raw_values = reader.read_object()
        self.var_formats = reader.read_object()
        self.var_bounding_boxes = reader.read_object()

    def describe(self):
        return f"BarcodeScan(id={self.stmt_id})"

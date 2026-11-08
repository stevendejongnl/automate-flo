from ..base import IntermittentDecision

TYPE_ID = 1174


class FileExists(IntermittentDecision):
    """id 1174, UI name "File exists". Extends IntermittentDecision
    (YES/NO branches + proceed/continuity). Own fields in wire order:
    path, varType, varSize, varLastModified -- output variables (Type:
    1 for a file, 2 for a directory; Size in bytes; Last modified as a
    unix timestamp). Cross-verified between two real exports."""

    type_id = TYPE_ID

    def __init__(self, stmt_id, cell_x=0, cell_y=0, on_positive=None,
                 on_negative=None, continuity=None, path=None,
                 var_type=None, var_size=None, var_last_modified=None):
        super().__init__(stmt_id, cell_x, cell_y)
        self.on_positive = on_positive
        self.on_negative = on_negative
        self.continuity = continuity
        self.path = path
        self.var_type = var_type
        self.var_size = var_size
        self.var_last_modified = var_last_modified

    def write_fields(self, writer):
        super().write_fields(writer)
        writer.write_object(writer.wrap_str(self.path))
        writer.write_object(self.var_type)
        writer.write_object(self.var_size)
        writer.write_object(self.var_last_modified)

    def read_fields(self, reader):
        super().read_fields(reader)
        self.path = reader.read_object()
        self.var_type = reader.read_object()
        self.var_size = reader.read_object()
        self.var_last_modified = reader.read_object()

    def describe(self):
        return f"FileExists(id={self.stmt_id})"

from ..base import Action

TYPE_ID = 1062


class FileDelete(Action):
    """id 1062, UI name "File delete". Extends Action directly. Own
    fields in wire order: path (final level may be a glob), recursive.
    Cross-verified between two real exports."""

    type_id = TYPE_ID

    def __init__(self, stmt_id, cell_x=0, cell_y=0, on_complete=None,
                 path=None, recursive=None):
        super().__init__(stmt_id, cell_x, cell_y, on_complete)
        self.path = path
        self.recursive = recursive

    def write_fields(self, writer):
        super().write_fields(writer)
        writer.write_object(writer.wrap_str(self.path))
        writer.write_object(writer.wrap_double(self.recursive))

    def read_fields(self, reader):
        super().read_fields(reader)
        self.path = reader.read_object()
        self.recursive = reader.read_object()

    def describe(self):
        return f"FileDelete(id={self.stmt_id})"

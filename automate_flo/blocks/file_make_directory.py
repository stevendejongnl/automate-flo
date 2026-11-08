from ..base import Action

TYPE_ID = 1066


class FileMakeDirectory(Action):
    """id 1066, UI name "File make directory". Extends Action directly.
    Single own field: path (parent directories are created as needed).
    Cross-verified between two real exports."""

    type_id = TYPE_ID

    def __init__(self, stmt_id, cell_x=0, cell_y=0, on_complete=None,
                 path=None):
        super().__init__(stmt_id, cell_x, cell_y, on_complete)
        self.path = path

    def write_fields(self, writer):
        super().write_fields(writer)
        writer.write_object(writer.wrap_str(self.path))

    def read_fields(self, reader):
        super().read_fields(reader)
        self.path = reader.read_object()

    def describe(self):
        return f"FileMakeDirectory(id={self.stmt_id})"

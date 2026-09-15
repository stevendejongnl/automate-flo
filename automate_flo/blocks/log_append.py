from ..base import Action

TYPE_ID = 1093


class LogAppend(Action):
    """id 1093, UI name "Append to log". Extends Action."""
    type_id = TYPE_ID

    def __init__(self, stmt_id, message, cell_x=0, cell_y=0, on_complete=None,
                 when_logging=None):
        super().__init__(stmt_id, cell_x, cell_y, on_complete)
        self.message = message
        self.when_logging = when_logging

    def write_fields(self, writer):
        super().write_fields(writer)
        writer.write_object(writer.wrap_str(self.message))
        writer.write_object(self.when_logging)

    def read_fields(self, reader):
        super().read_fields(reader)
        self.message = reader.read_object()
        self.when_logging = reader.read_object()

    def describe(self):
        return f"LogAppend(id={self.stmt_id})"

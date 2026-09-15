from ..base import Action

TYPE_ID = 1336


class AlternativeLaunch(Action):
    """id 1336, UI name "Alternative launch". Extends Action -- one nullable
    "title" string-expression field."""
    type_id = TYPE_ID

    def __init__(self, stmt_id, cell_x=0, cell_y=0, on_complete=None,
                 title=None):
        super().__init__(stmt_id, cell_x, cell_y, on_complete)
        self.title = title

    def write_fields(self, writer):
        super().write_fields(writer)
        writer.write_object(writer.wrap_str(self.title))

    def read_fields(self, reader):
        super().read_fields(reader)
        self.title = reader.read_object()

    def describe(self):
        return f"AlternativeLaunch(id={self.stmt_id})"

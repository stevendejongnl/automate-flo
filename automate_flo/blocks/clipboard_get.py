from ..base import IntermittentAction

TYPE_ID = 1032


class ClipboardGet(IntermittentAction):
    """id 1032, UI name "Get clipboard". Extends IntermittentAction."""
    type_id = TYPE_ID

    def __init__(self, stmt_id, var_content=None, cell_x=0, cell_y=0,
                 on_complete=None, continuity=None):
        super().__init__(stmt_id, cell_x, cell_y, on_complete)
        self.continuity = continuity
        self.var_content = var_content

    def write_fields(self, writer):
        super().write_fields(writer)
        writer.write_object(self.var_content)

    def read_fields(self, reader):
        super().read_fields(reader)
        self.var_content = reader.read_object()

    def describe(self):
        return f"ClipboardGet(id={self.stmt_id})"

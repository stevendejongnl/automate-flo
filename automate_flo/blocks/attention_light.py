from ..base import Action

TYPE_ID = 1205


class AttentionLight(Action):
    """id 1205, UI name "Attention light". Extends SetStateAction extends Action -- state duplicated inline per this library's convention (SetStateAction not modeled as a shared Python base, same as AtomicAction). Fields, in order: state (generic expression, inherited from SetStateAction), color (generic expression, this block's own)."""
    type_id = TYPE_ID

    def __init__(self, stmt_id, cell_x=0, cell_y=0, on_complete=None, state=None, color=None):
        super().__init__(stmt_id, cell_x, cell_y, on_complete)
        self.state = state
        self.color = color

    def write_fields(self, writer):
        super().write_fields(writer)
        writer.write_object(self.state)
        writer.write_object(self.color)

    def read_fields(self, reader):
        super().read_fields(reader)
        self.state = reader.read_object()
        self.color = reader.read_object()

    def describe(self):
        return f"AttentionLight(id={self.stmt_id})"

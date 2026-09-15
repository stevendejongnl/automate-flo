from ..base import IntermittentAction

TYPE_ID = 1120


class ToastShow(IntermittentAction):
    """id 1120, UI name "Show toast message". Extends IntermittentAction."""
    type_id = TYPE_ID

    def __init__(self, stmt_id, message, cell_x=0, cell_y=0, on_complete=None,
                 continuity=None, duration=None):
        super().__init__(stmt_id, cell_x, cell_y, on_complete)
        self.continuity = continuity
        self.message = message
        self.duration = duration

    def write_fields(self, writer):
        super().write_fields(writer)
        writer.write_object(writer.wrap_str(self.message))
        writer.write_object(self.duration)

    def read_fields(self, reader):
        super().read_fields(reader)
        self.message = reader.read_object()
        self.duration = reader.read_object()

    def describe(self):
        return f"ToastShow(id={self.stmt_id})"

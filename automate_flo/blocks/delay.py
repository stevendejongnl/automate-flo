from ..base import IntermittentAction, DoubleExpr

TYPE_ID = 1046


class Delay(IntermittentAction):
    """id 1046. Extends IntermittentAction extends Action."""
    type_id = TYPE_ID

    def __init__(self, stmt_id, seconds, cell_x=0, cell_y=0, on_complete=None,
                 continuity=None, wakeup=None):
        super().__init__(stmt_id, cell_x, cell_y, on_complete)
        self.seconds = seconds
        self.continuity = continuity
        self.wakeup = wakeup

    def write_fields(self, writer):
        super().write_fields(writer)
        writer.write_object(self.wakeup)
        writer.write_object(DoubleExpr(self.seconds))

    def read_fields(self, reader):
        super().read_fields(reader)
        self.wakeup = reader.read_object()
        dur = reader.read_object()
        self.seconds = dur.value if dur is not None else None

    def describe(self):
        return f"Delay(id={self.stmt_id}, seconds={self.seconds!r})"

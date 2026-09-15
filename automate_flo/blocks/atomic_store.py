from ..base import Action

TYPE_ID = 1257


class AtomicStore(Action):
    """id 1257, UI name "Atomic store". Extends AtomicAction extends Action -- varAtomic duplicated inline per this library's convention (see AtomicAdd). Single field: varAtomic (VariableExpr) -- atomically stores this variable's current value."""
    type_id = TYPE_ID

    def __init__(self, stmt_id, cell_x=0, cell_y=0, on_complete=None, var_atomic=None):
        super().__init__(stmt_id, cell_x, cell_y, on_complete)
        self.var_atomic = var_atomic

    def write_fields(self, writer):
        super().write_fields(writer)
        writer.write_object(self.var_atomic)

    def read_fields(self, reader):
        super().read_fields(reader)
        self.var_atomic = reader.read_object()

    def describe(self):
        return f"AtomicStore(id={self.stmt_id})"

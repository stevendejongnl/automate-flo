from ..base import Action

TYPE_ID = 1253


class AtomicAdd(Action):
    """id 1253, UI name "Atomic add". Extends AtomicAction extends Action -- varAtomic duplicated inline per this library's convention (only AtomicAdd/AtomicClearAll/AtomicCompareAndStore/AtomicLoad/AtomicStore share it, not modeled as a shared Python base). Fields: varAtomic (VariableExpr), delta (numeric expression)."""
    type_id = TYPE_ID

    def __init__(self, stmt_id, cell_x=0, cell_y=0, on_complete=None, var_atomic=None, delta=None):
        super().__init__(stmt_id, cell_x, cell_y, on_complete)
        self.var_atomic = var_atomic
        self.delta = delta

    def write_fields(self, writer):
        super().write_fields(writer)
        writer.write_object(self.var_atomic)
        writer.write_object(writer.wrap_double(self.delta))

    def read_fields(self, reader):
        super().read_fields(reader)
        self.var_atomic = reader.read_object()
        self.delta = reader.read_object()

    def describe(self):
        return f"AtomicAdd(id={self.stmt_id})"

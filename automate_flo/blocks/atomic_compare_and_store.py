from ..base import Decision

TYPE_ID = 1255


class AtomicCompareAndStore(Decision):
    """id 1255, UI name "Atomic compare and store". Extends AtomicDecision extends Decision -- onPositive/onNegative, not onComplete. varAtomic/expect duplicated inline per this library's convention (see AtomicAdd). Fields: varAtomic (VariableExpr), expect (generic expression to compare against before storing)."""
    type_id = TYPE_ID

    def __init__(self, stmt_id, cell_x=0, cell_y=0, on_positive=None, on_negative=None, var_atomic=None, expect=None):
        super().__init__(stmt_id, cell_x, cell_y, on_complete=None)
        self.on_positive = on_positive
        self.on_negative = on_negative
        self.var_atomic = var_atomic
        self.expect = expect

    def write_fields(self, writer):
        super().write_fields(writer)
        writer.write_object(self.var_atomic)
        writer.write_object(self.expect)

    def read_fields(self, reader):
        super().read_fields(reader)
        self.var_atomic = reader.read_object()
        self.expect = reader.read_object()

    def describe(self):
        return f"AtomicCompareAndStore(id={self.stmt_id})"

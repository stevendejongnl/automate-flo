from ..base import LevelDecision

TYPE_ID = 1030


class CellSignalLevel(LevelDecision):
    """id 1030, UI name "Cell signal level". Extends LevelDecision extends
    IntermittentDecision extends Decision -- onPositive/onNegative, not
    onComplete. Adds one field of its own on top of LevelDecision's
    min_level/max_level/var_level: subscription_id (wrap_double)."""
    type_id = TYPE_ID

    def __init__(self, stmt_id, cell_x=0, cell_y=0, on_positive=None,
                 on_negative=None, continuity=None, min_level=None,
                 max_level=None, var_level=None, subscription_id=None):
        super().__init__(stmt_id, cell_x, cell_y, on_complete=None)
        self.on_positive = on_positive
        self.on_negative = on_negative
        self.continuity = continuity
        self.min_level = min_level
        self.max_level = max_level
        self.var_level = var_level
        self.subscription_id = subscription_id

    def write_fields(self, writer):
        super().write_fields(writer)
        writer.write_object(writer.wrap_double(self.subscription_id))

    def read_fields(self, reader):
        super().read_fields(reader)
        self.subscription_id = reader.read_object()

    def describe(self):
        return f"CellSignalLevel(id={self.stmt_id})"

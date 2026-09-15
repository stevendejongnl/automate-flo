from ..base import IntermittentDecision

TYPE_ID = 1147


class WifiEnabled(IntermittentDecision):
    """id 1147, UI name "Wifi enabled?". Extends IntermittentDecision
    directly -- no extra fields beyond onPositive/onNegative/continuity."""
    type_id = TYPE_ID

    def __init__(self, stmt_id, cell_x=0, cell_y=0, on_positive=None,
                 on_negative=None, continuity=None):
        super().__init__(stmt_id, cell_x, cell_y, on_complete=None)
        self.on_positive = on_positive
        self.on_negative = on_negative
        self.continuity = continuity

    def describe(self):
        return f"WifiEnabled(id={self.stmt_id})"

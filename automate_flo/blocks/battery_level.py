from ..base import LevelDecision

TYPE_ID = 1021


class BatteryLevel(LevelDecision):
    """id 1021, UI name "Battery level". Extends LevelDecision extends
    IntermittentDecision extends Decision -- onPositive/onNegative, not
    onComplete."""
    type_id = TYPE_ID

    def __init__(self, stmt_id, cell_x=0, cell_y=0, on_positive=None,
                 on_negative=None, continuity=None, min_level=None,
                 max_level=None, var_level=None):
        super().__init__(stmt_id, cell_x, cell_y, on_complete=None)
        self.on_positive = on_positive
        self.on_negative = on_negative
        self.continuity = continuity
        self.min_level = min_level
        self.max_level = max_level
        self.var_level = var_level

    def describe(self):
        return f"BatteryLevel(id={self.stmt_id})"

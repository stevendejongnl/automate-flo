from ..base import IntermittentDecision

TYPE_ID = 1050


class DeviceUnlocked(IntermittentDecision):
    """id 1050, UI name "Device unlocked?". Extends IntermittentDecision
    directly -- onPositive/onNegative/continuity, no extra fields of its
    own at all."""
    type_id = TYPE_ID

    def __init__(self, stmt_id, cell_x=0, cell_y=0, on_positive=None,
                 on_negative=None, continuity=None):
        super().__init__(stmt_id, cell_x, cell_y, on_complete=None)
        self.on_positive = on_positive
        self.on_negative = on_negative
        self.continuity = continuity

    def describe(self):
        return f"DeviceUnlocked(id={self.stmt_id})"

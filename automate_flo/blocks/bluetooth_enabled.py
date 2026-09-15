from ..base import IntermittentDecision

TYPE_ID = 1155


class BluetoothEnabled(IntermittentDecision):
    """id 1155, UI name "Bluetooth enabled?". Same shape as WifiEnabled --
    bare IntermittentDecision, no extra fields."""
    type_id = TYPE_ID

    def __init__(self, stmt_id, cell_x=0, cell_y=0, on_positive=None,
                 on_negative=None, continuity=None):
        super().__init__(stmt_id, cell_x, cell_y, on_complete=None)
        self.on_positive = on_positive
        self.on_negative = on_negative
        self.continuity = continuity

    def describe(self):
        return f"BluetoothEnabled(id={self.stmt_id})"

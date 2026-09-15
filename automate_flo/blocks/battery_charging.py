from ..base import IntermittentDecision

TYPE_ID = 1369


class BatteryCharging(IntermittentDecision):
    """id 1369, UI name "Battery charging?". Extends IntermittentDecision extends Decision -- onPositive/onNegative/continuity. Single field: var_until_fully_charged (VariableExpr output var)."""
    type_id = TYPE_ID

    def __init__(self, stmt_id, cell_x=0, cell_y=0, on_positive=None, on_negative=None, continuity=None, var_until_fully_charged=None):
        super().__init__(stmt_id, cell_x, cell_y, on_complete=None)
        self.on_positive = on_positive
        self.on_negative = on_negative
        self.continuity = continuity
        self.var_until_fully_charged = var_until_fully_charged

    def write_fields(self, writer):
        super().write_fields(writer)
        writer.write_object(self.var_until_fully_charged)

    def read_fields(self, reader):
        super().read_fields(reader)
        self.var_until_fully_charged = reader.read_object()

    def describe(self):
        return f"BatteryCharging(id={self.stmt_id})"

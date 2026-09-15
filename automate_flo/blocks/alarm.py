from ..base import IntermittentDecision

TYPE_ID = 1210


class Alarm(IntermittentDecision):
    """id 1210, UI name "Alarm". Extends IntermittentDecision directly --
    onPositive/onNegative/continuity, plus varAlarmTimestamp (a VariableExpr
    reference the block writes the next alarm's epoch-seconds timestamp
    into, or None if unused)."""
    type_id = TYPE_ID

    def __init__(self, stmt_id, cell_x=0, cell_y=0, on_positive=None,
                 on_negative=None, continuity=None, var_alarm_timestamp=None):
        super().__init__(stmt_id, cell_x, cell_y, on_complete=None)
        self.on_positive = on_positive
        self.on_negative = on_negative
        self.continuity = continuity
        self.var_alarm_timestamp = var_alarm_timestamp

    def write_fields(self, writer):
        super().write_fields(writer)
        writer.write_object(self.var_alarm_timestamp)

    def read_fields(self, reader):
        super().read_fields(reader)
        self.var_alarm_timestamp = reader.read_object()

    def describe(self):
        return f"Alarm(id={self.stmt_id})"

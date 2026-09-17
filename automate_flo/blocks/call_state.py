from ..base import IntermittentDecision

TYPE_ID = 1029


class CallState(IntermittentDecision):
    """id 1029, UI name "Call state?". Extends IntermittentDecision directly -- onPositive/onNegative/continuity, then state and subscription_id (both wrap_double), in that order. Checks/waits for whether the call state (idle/ringing/offhook) on a given subscription matches."""
    type_id = TYPE_ID

    def __init__(self, stmt_id, cell_x=0, cell_y=0, on_positive=None,
                 on_negative=None, continuity=None, state=None, subscription_id=None):
        super().__init__(stmt_id, cell_x, cell_y, on_complete=None)
        self.on_positive = on_positive
        self.on_negative = on_negative
        self.continuity = continuity
        self.state = state
        self.subscription_id = subscription_id

    def write_fields(self, writer):
        super().write_fields(writer)
        writer.write_object(writer.wrap_double(self.state))
        writer.write_object(writer.wrap_double(self.subscription_id))

    def read_fields(self, reader):
        super().read_fields(reader)
        self.state = reader.read_object()
        self.subscription_id = reader.read_object()

    def describe(self):
        return f"CallState(id={self.stmt_id})"

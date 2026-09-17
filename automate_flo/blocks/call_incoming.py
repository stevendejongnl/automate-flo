from ..base import IntermittentAction

TYPE_ID = 1026


class CallIncoming(IntermittentAction):
    """id 1026, UI name "Call incoming", extends IntermittentAction directly (flattening CallEvent's fields inline, mirroring the shared field layout also used by CallOutgoing) -- onComplete/continuity, then phone_number (wrap_str), subscription_id (wrap_double), var_phone_number and var_subscription_id (VariableExpr, raw pass-through), in that order. Fires when an incoming call is detected (ringing/answered/missed)."""
    type_id = TYPE_ID

    def __init__(self, stmt_id, cell_x=0, cell_y=0, on_complete=None,
                 continuity=None, phone_number=None, subscription_id=None,
                 var_phone_number=None, var_subscription_id=None):
        super().__init__(stmt_id, cell_x, cell_y, on_complete)
        self.continuity = continuity
        self.phone_number = phone_number
        self.subscription_id = subscription_id
        self.var_phone_number = var_phone_number
        self.var_subscription_id = var_subscription_id

    def write_fields(self, writer):
        super().write_fields(writer)
        writer.write_object(writer.wrap_str(self.phone_number))
        writer.write_object(writer.wrap_double(self.subscription_id))
        writer.write_object(self.var_phone_number)
        writer.write_object(self.var_subscription_id)

    def read_fields(self, reader):
        super().read_fields(reader)
        self.phone_number = reader.read_object()
        self.subscription_id = reader.read_object()
        self.var_phone_number = reader.read_object()
        self.var_subscription_id = reader.read_object()

    def describe(self):
        return f"CallIncoming(id={self.stmt_id})"

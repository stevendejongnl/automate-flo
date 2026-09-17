from ..base import Action

TYPE_ID = 1027


class CallNumber(Action):
    """id 1027, UI name "Call number" -- extends Action directly (flattening DialerAction's 3 fields inline, plus CallNumber's own flags field) -- onComplete only, no continuity. Required phone_number field (wrap_str). Optional subscription_id, sim_slot_index, flags (all wrap_double)."""
    type_id = TYPE_ID

    def __init__(self, stmt_id, phone_number, cell_x=0, cell_y=0, on_complete=None,
                 subscription_id=None, sim_slot_index=None, flags=None):
        super().__init__(stmt_id, cell_x, cell_y, on_complete)
        self.phone_number = phone_number
        self.subscription_id = subscription_id
        self.sim_slot_index = sim_slot_index
        self.flags = flags

    def write_fields(self, writer):
        super().write_fields(writer)
        writer.write_object(writer.wrap_str(self.phone_number))
        writer.write_object(writer.wrap_double(self.subscription_id))
        writer.write_object(writer.wrap_double(self.sim_slot_index))
        writer.write_object(writer.wrap_double(self.flags))

    def read_fields(self, reader):
        super().read_fields(reader)
        self.phone_number = reader.read_object()
        self.subscription_id = reader.read_object()
        self.sim_slot_index = reader.read_object()
        self.flags = reader.read_object()

    def describe(self):
        return f"CallNumber(id={self.stmt_id})"

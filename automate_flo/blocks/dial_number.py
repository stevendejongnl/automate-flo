from ..base import Action

TYPE_ID = 1051


class DialNumber(Action):
    """id 1051, UI name "Dial number". Extends DialerAction extends Action
    directly, flattening DialerAction's 3 fields inline (same as
    CallNumber, but with no extra field of its own and no required
    field) -- onComplete only, no continuity."""
    type_id = TYPE_ID

    def __init__(self, stmt_id, cell_x=0, cell_y=0, on_complete=None,
                 phone_number=None, subscription_id=None, sim_slot_index=None):
        super().__init__(stmt_id, cell_x, cell_y, on_complete)
        self.phone_number = phone_number
        self.subscription_id = subscription_id
        self.sim_slot_index = sim_slot_index

    def write_fields(self, writer):
        super().write_fields(writer)
        writer.write_object(writer.wrap_str(self.phone_number))
        writer.write_object(writer.wrap_double(self.subscription_id))
        writer.write_object(writer.wrap_double(self.sim_slot_index))

    def read_fields(self, reader):
        super().read_fields(reader)
        self.phone_number = reader.read_object()
        self.subscription_id = reader.read_object()
        self.sim_slot_index = reader.read_object()

    def describe(self):
        return f"DialNumber(id={self.stmt_id})"

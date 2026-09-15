from ..base import Action

TYPE_ID = 1165


class AirplaneModeSetState(Action):
    """id 1165, UI name "Set airplane mode state". Extends SetStateAction (Action + one 'state' boolean-expression field)."""
    type_id = TYPE_ID

    def __init__(self, stmt_id, state, cell_x=0, cell_y=0, on_complete=None):
        super().__init__(stmt_id, cell_x, cell_y, on_complete)
        self.state = state

    def write_fields(self, writer):
        super().write_fields(writer)
        writer.write_object(writer.wrap_bool(self.state))

    def read_fields(self, reader):
        super().read_fields(reader)
        self.state = reader.read_object()

    def describe(self):
        return f"AirplaneModeSetState(id={self.stmt_id})"

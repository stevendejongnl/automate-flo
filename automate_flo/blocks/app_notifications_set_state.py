from ..base import Action

TYPE_ID = 1243


class AppNotificationsSetState(Action):
    """id 1243, UI name "Set app notifications state". Extends Action -- packageName (string expression, wrapped via writer.wrap_str), state (boolean-valued expression, wrapped via writer.wrap_bool -- same pattern as SetStateAction blocks like WifiSetState)."""
    type_id = TYPE_ID

    def __init__(self, stmt_id, cell_x=0, cell_y=0, on_complete=None, package_name=None, state=None):
        super().__init__(stmt_id, cell_x, cell_y, on_complete)
        self.package_name = package_name
        self.state = state

    def write_fields(self, writer):
        super().write_fields(writer)
        writer.write_object(writer.wrap_str(self.package_name))
        writer.write_object(writer.wrap_bool(self.state))

    def read_fields(self, reader):
        super().read_fields(reader)
        self.package_name = reader.read_object()
        self.state = reader.read_object()

    def describe(self):
        return f"AppNotificationsSetState(id={self.stmt_id})"

from ..base import Action

TYPE_ID = 1309


class AppNotificationsVisibilitySet(Action):
    """id 1309, UI name "Set app notifications visibility". Extends Action -- packageName (string expression, wrapped via writer.wrap_str), visibility (numeric expression, wrapped via writer.wrap_double)."""

    type_id = TYPE_ID

    def __init__(self, stmt_id, cell_x=0, cell_y=0, on_complete=None, package_name=None, visibility=None):
        super().__init__(stmt_id, cell_x, cell_y, on_complete)
        self.package_name = package_name
        self.visibility = visibility

    def write_fields(self, writer):
        super().write_fields(writer)
        writer.write_object(writer.wrap_str(self.package_name))
        writer.write_object(writer.wrap_double(self.visibility))

    def read_fields(self, reader):
        super().read_fields(reader)
        self.package_name = reader.read_object()
        self.visibility = reader.read_object()

    def describe(self):
        return f"AppNotificationsVisibilitySet(id={self.stmt_id})"

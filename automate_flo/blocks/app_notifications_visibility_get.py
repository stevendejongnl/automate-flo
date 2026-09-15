from ..base import Action

TYPE_ID = 1308


class AppNotificationsVisibilityGet(Action):
    """id 1308, UI name "Get app notifications visibility". Extends Action -- packageName (string expression, wrapped via writer.wrap_str), varVisibility (variable-reference, raw pass-through, no wrapping)."""
    type_id = TYPE_ID

    def __init__(self, stmt_id, cell_x=0, cell_y=0, on_complete=None, package_name=None, var_visibility=None):
        super().__init__(stmt_id, cell_x, cell_y, on_complete)
        self.package_name = package_name
        self.var_visibility = var_visibility

    def write_fields(self, writer):
        super().write_fields(writer)
        writer.write_object(writer.wrap_str(self.package_name))
        writer.write_object(self.var_visibility)

    def read_fields(self, reader):
        super().read_fields(reader)
        self.package_name = reader.read_object()
        self.var_visibility = reader.read_object()

    def describe(self):
        return f"AppNotificationsVisibilityGet(id={self.stmt_id})"

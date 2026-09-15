from ..base import Action

TYPE_ID = 1306


class AppNotificationsPriorityGet(Action):
    """id 1306, UI name "Get app notifications priority". Extends Action -- packageName (string expression, wrapped via writer.wrap_str), varPriority (variable-reference, raw pass-through, no wrapping)."""
    type_id = TYPE_ID

    def __init__(self, stmt_id, cell_x=0, cell_y=0, on_complete=None, package_name=None, var_priority=None):
        super().__init__(stmt_id, cell_x, cell_y, on_complete)
        self.package_name = package_name
        self.var_priority = var_priority

    def write_fields(self, writer):
        super().write_fields(writer)
        writer.write_object(writer.wrap_str(self.package_name))
        writer.write_object(self.var_priority)

    def read_fields(self, reader):
        super().read_fields(reader)
        self.package_name = reader.read_object()
        self.var_priority = reader.read_object()

    def describe(self):
        return f"AppNotificationsPriorityGet(id={self.stmt_id})"

from ..base import Action

TYPE_ID = 1307


class AppNotificationsPrioritySet(Action):
    """id 1307, UI name "Set app notifications priority". Extends Action -- packageName (string expression, wrapped via writer.wrap_str), priority (numeric expression, wrapped via writer.wrap_double so plain ints can be passed)."""

    type_id = TYPE_ID

    def __init__(self, stmt_id, cell_x=0, cell_y=0, on_complete=None, package_name=None, priority=None):
        super().__init__(stmt_id, cell_x, cell_y, on_complete)
        self.package_name = package_name
        self.priority = priority

    def write_fields(self, writer):
        super().write_fields(writer)
        writer.write_object(writer.wrap_str(self.package_name))
        writer.write_object(writer.wrap_double(self.priority))

    def read_fields(self, reader):
        super().read_fields(reader)
        self.package_name = reader.read_object()
        self.priority = reader.read_object()

    def describe(self):
        return f"AppNotificationsPrioritySet(id={self.stmt_id})"

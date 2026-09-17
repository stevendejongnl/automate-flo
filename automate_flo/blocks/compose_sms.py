from ..base import Action

TYPE_ID = 1036


class ComposeSms(Action):
    """id 1036, UI name "Compose SMS". Extends Action directly -- onComplete
    only, no continuity. phone_number is a multi-value expression, raw
    pass-through (not wrap_str, same as ComposeMms). message/package_name
    are plain string expressions, wrap_str. No field is required."""
    type_id = TYPE_ID

    def __init__(self, stmt_id, cell_x=0, cell_y=0, on_complete=None,
                 phone_number=None, message=None, package_name=None):
        super().__init__(stmt_id, cell_x, cell_y, on_complete)
        self.phone_number = phone_number
        self.message = message
        self.package_name = package_name

    def write_fields(self, writer):
        super().write_fields(writer)
        writer.write_object(self.phone_number)
        writer.write_object(writer.wrap_str(self.message))
        writer.write_object(writer.wrap_str(self.package_name))

    def read_fields(self, reader):
        super().read_fields(reader)
        self.phone_number = reader.read_object()
        self.message = reader.read_object()
        self.package_name = reader.read_object()

    def describe(self):
        return f"ComposeSms(id={self.stmt_id})"

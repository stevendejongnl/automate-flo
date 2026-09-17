from ..base import Action

TYPE_ID = 1035


class ComposeMms(Action):
    """id 1035, UI name "Compose MMS". Extends Action directly -- onComplete
    only, no continuity. phone_number is a multi-value expression, raw
    pass-through (not wrap_str, same as ComposeEmail's "to"). subject/
    message/package_name are plain string expressions, wrap_str.
    attachment is a single file-path expression, raw pass-through. No
    field is required."""
    type_id = TYPE_ID

    def __init__(self, stmt_id, cell_x=0, cell_y=0, on_complete=None,
                 phone_number=None, subject=None, message=None,
                 attachment=None, package_name=None):
        super().__init__(stmt_id, cell_x, cell_y, on_complete)
        self.phone_number = phone_number
        self.subject = subject
        self.message = message
        self.attachment = attachment
        self.package_name = package_name

    def write_fields(self, writer):
        super().write_fields(writer)
        writer.write_object(self.phone_number)
        writer.write_object(writer.wrap_str(self.subject))
        writer.write_object(writer.wrap_str(self.message))
        writer.write_object(self.attachment)
        writer.write_object(writer.wrap_str(self.package_name))

    def read_fields(self, reader):
        super().read_fields(reader)
        self.phone_number = reader.read_object()
        self.subject = reader.read_object()
        self.message = reader.read_object()
        self.attachment = reader.read_object()
        self.package_name = reader.read_object()

    def describe(self):
        return f"ComposeMms(id={self.stmt_id})"

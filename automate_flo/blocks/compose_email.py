from ..base import Action

TYPE_ID = 1034


class ComposeEmail(Action):
    """id 1034, UI name "Compose email". Extends EmailAction extends Action
    directly (flattening EmailAction's fields inline, same convention as
    call_incoming.py flattens CallEvent) -- onComplete only, no continuity.
    to/cc/bcc/attachments are multi-value expressions, raw pass-through
    (not wrap_str). subject/message and ComposeEmail's own package_name
    are plain string expressions, wrap_str. No field is required."""
    type_id = TYPE_ID

    def __init__(self, stmt_id, cell_x=0, cell_y=0, on_complete=None,
                 to=None, cc=None, bcc=None, subject=None, message=None,
                 attachments=None, package_name=None):
        super().__init__(stmt_id, cell_x, cell_y, on_complete)
        self.to = to
        self.cc = cc
        self.bcc = bcc
        self.subject = subject
        self.message = message
        self.attachments = attachments
        self.package_name = package_name

    def write_fields(self, writer):
        super().write_fields(writer)
        writer.write_object(self.to)
        writer.write_object(self.cc)
        writer.write_object(self.bcc)
        writer.write_object(writer.wrap_str(self.subject))
        writer.write_object(writer.wrap_str(self.message))
        writer.write_object(self.attachments)
        writer.write_object(writer.wrap_str(self.package_name))

    def read_fields(self, reader):
        super().read_fields(reader)
        self.to = reader.read_object()
        self.cc = reader.read_object()
        self.bcc = reader.read_object()
        self.subject = reader.read_object()
        self.message = reader.read_object()
        self.attachments = reader.read_object()
        self.package_name = reader.read_object()

    def describe(self):
        return f"ComposeEmail(id={self.stmt_id})"

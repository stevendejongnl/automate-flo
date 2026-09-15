from ..base import Action

TYPE_ID = 1033


class ClipboardSet(Action):
    """id 1033, UI name "Set clipboard". Extends Action."""
    type_id = TYPE_ID

    def __init__(self, stmt_id, text=None, cell_x=0, cell_y=0, on_complete=None,
                 html_text=None, uri=None, mime_type=None, label=None, sensitive=None):
        super().__init__(stmt_id, cell_x, cell_y, on_complete)
        self.text = text
        self.html_text = html_text
        self.uri = uri
        self.mime_type = mime_type
        self.label = label
        self.sensitive = sensitive

    def write_fields(self, writer):
        super().write_fields(writer)
        writer.write_object(writer.wrap_str(self.text))
        writer.write_object(self.html_text)
        writer.write_object(self.uri)
        writer.write_object(self.mime_type)
        writer.write_object(self.label)
        writer.write_object(self.sensitive)

    def read_fields(self, reader):
        super().read_fields(reader)
        self.text = reader.read_object()
        self.html_text = reader.read_object()
        self.uri = reader.read_object()
        self.mime_type = reader.read_object()
        self.label = reader.read_object()
        self.sensitive = reader.read_object()

    def describe(self):
        return f"ClipboardSet(id={self.stmt_id})"

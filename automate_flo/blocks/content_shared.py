from ..base import Action

TYPE_ID = 1041


class ContentShared(Action):
    """id 1041, UI name "Content shared". Extends Action directly --
    onComplete only, no continuity. title/mime_type are plain string
    expressions (wrap_str). multiple is a boolean-valued expression
    (wrap_bool). Then 4 VariableExpr output fields, raw pass-through:
    var_content_text, var_content_subject, var_content_uri,
    var_content_mime_type. No field is required."""
    type_id = TYPE_ID

    def __init__(self, stmt_id, cell_x=0, cell_y=0, on_complete=None,
                 title=None, mime_type=None, multiple=None,
                 var_content_text=None, var_content_subject=None,
                 var_content_uri=None, var_content_mime_type=None):
        super().__init__(stmt_id, cell_x, cell_y, on_complete)
        self.title = title
        self.mime_type = mime_type
        self.multiple = multiple
        self.var_content_text = var_content_text
        self.var_content_subject = var_content_subject
        self.var_content_uri = var_content_uri
        self.var_content_mime_type = var_content_mime_type

    def write_fields(self, writer):
        super().write_fields(writer)
        writer.write_object(writer.wrap_str(self.title))
        writer.write_object(writer.wrap_str(self.mime_type))
        writer.write_object(writer.wrap_bool(self.multiple))
        writer.write_object(self.var_content_text)
        writer.write_object(self.var_content_subject)
        writer.write_object(self.var_content_uri)
        writer.write_object(self.var_content_mime_type)

    def read_fields(self, reader):
        super().read_fields(reader)
        self.title = reader.read_object()
        self.mime_type = reader.read_object()
        self.multiple = reader.read_object()
        self.var_content_text = reader.read_object()
        self.var_content_subject = reader.read_object()
        self.var_content_uri = reader.read_object()
        self.var_content_mime_type = reader.read_object()

    def describe(self):
        return f"ContentShared(id={self.stmt_id})"

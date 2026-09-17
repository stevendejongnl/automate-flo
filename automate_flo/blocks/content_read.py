from ..base import Action

TYPE_ID = 1039


class ContentRead(Action):
    """id 1039, UI name "Read content". Extends Action directly --
    onComplete only, no continuity. Required source_uri field (wrap_str
    -- RequiredArgumentNullException at runtime if null). Optional
    target_path (wrap_str), then 3 VariableExpr output fields (raw
    pass-through): var_content_file, var_content_display_name,
    var_content_mime_type."""
    type_id = TYPE_ID

    def __init__(self, stmt_id, source_uri, cell_x=0, cell_y=0, on_complete=None,
                 target_path=None, var_content_file=None,
                 var_content_display_name=None, var_content_mime_type=None):
        super().__init__(stmt_id, cell_x, cell_y, on_complete)
        self.source_uri = source_uri
        self.target_path = target_path
        self.var_content_file = var_content_file
        self.var_content_display_name = var_content_display_name
        self.var_content_mime_type = var_content_mime_type

    def write_fields(self, writer):
        super().write_fields(writer)
        writer.write_object(writer.wrap_str(self.source_uri))
        writer.write_object(writer.wrap_str(self.target_path))
        writer.write_object(self.var_content_file)
        writer.write_object(self.var_content_display_name)
        writer.write_object(self.var_content_mime_type)

    def read_fields(self, reader):
        super().read_fields(reader)
        self.source_uri = reader.read_object()
        self.target_path = reader.read_object()
        self.var_content_file = reader.read_object()
        self.var_content_display_name = reader.read_object()
        self.var_content_mime_type = reader.read_object()

    def describe(self):
        return f"ContentRead(id={self.stmt_id})"

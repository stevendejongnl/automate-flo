from ..base import Action

TYPE_ID = 1042


class ContentView(Action):
    """id 1042, UI name "View content". Extends Action directly --
    onComplete only, no continuity. Required uri field (wrap_str --
    RequiredArgumentNullException at runtime if null). Optional
    mime_type/package_name (wrap_str) and chooser (a boolean-valued
    expression, wrap_bool)."""
    type_id = TYPE_ID

    def __init__(self, stmt_id, uri, cell_x=0, cell_y=0, on_complete=None,
                 mime_type=None, package_name=None, chooser=None):
        super().__init__(stmt_id, cell_x, cell_y, on_complete)
        self.uri = uri
        self.mime_type = mime_type
        self.package_name = package_name
        self.chooser = chooser

    def write_fields(self, writer):
        super().write_fields(writer)
        writer.write_object(writer.wrap_str(self.uri))
        writer.write_object(writer.wrap_str(self.mime_type))
        writer.write_object(writer.wrap_str(self.package_name))
        writer.write_object(writer.wrap_bool(self.chooser))

    def read_fields(self, reader):
        super().read_fields(reader)
        self.uri = reader.read_object()
        self.mime_type = reader.read_object()
        self.package_name = reader.read_object()
        self.chooser = reader.read_object()

    def describe(self):
        return f"ContentView(id={self.stmt_id})"

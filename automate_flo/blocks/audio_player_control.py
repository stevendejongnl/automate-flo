from ..base import Action

TYPE_ID = 1152


class AudioPlayerControl(Action):
    """id 1152, UI name "Audio player control". Extends Action directly. The "position" field is version-gated (version>=79) in the app but this library always writes version 114, so it is always present."""
    type_id = TYPE_ID

    def __init__(self, stmt_id, cell_x=0, cell_y=0, on_complete=None, command=None, position=None, method=None, package_name=None, class_name=None):
        super().__init__(stmt_id, cell_x, cell_y, on_complete)
        self.command = command
        self.position = position
        self.method = method
        self.package_name = package_name
        self.class_name = class_name

    def write_fields(self, writer):
        super().write_fields(writer)
        writer.write_object(self.command)
        writer.write_object(self.position)
        writer.write_object(self.method)
        writer.write_object(self.package_name)
        writer.write_object(self.class_name)

    def read_fields(self, reader):
        super().read_fields(reader)
        self.command = reader.read_object()
        self.position = reader.read_object()
        self.method = reader.read_object()
        self.package_name = reader.read_object()
        self.class_name = reader.read_object()

    def describe(self):
        return f"AudioPlayerControl(id={self.stmt_id})"

from ..base import Action

TYPE_ID = 1018


class AudioVolumeSet(Action):
    """id 1018, UI name "Set audio volume". Extends Action directly. Fields, in order: stream, level, play_sound, show_popup (all generic expressions)."""
    type_id = TYPE_ID

    def __init__(self, stmt_id, cell_x=0, cell_y=0, on_complete=None, stream=None, level=None, play_sound=None, show_popup=None):
        super().__init__(stmt_id, cell_x, cell_y, on_complete)
        self.stream = stream
        self.level = level
        self.play_sound = play_sound
        self.show_popup = show_popup

    def write_fields(self, writer):
        super().write_fields(writer)
        writer.write_object(self.stream)
        writer.write_object(self.level)
        writer.write_object(self.play_sound)
        writer.write_object(self.show_popup)

    def read_fields(self, reader):
        super().read_fields(reader)
        self.stream = reader.read_object()
        self.level = reader.read_object()
        self.play_sound = reader.read_object()
        self.show_popup = reader.read_object()

    def describe(self):
        return f"AudioVolumeSet(id={self.stmt_id})"

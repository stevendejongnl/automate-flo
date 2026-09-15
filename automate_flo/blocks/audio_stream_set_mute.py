from ..base import Action

TYPE_ID = 1318


class AudioStreamSetMute(Action):
    """id 1318, UI name "Set audio stream mute". Extends SetStateAction extends Action -- state duplicated inline per this library's convention (see AttentionLight). Fields, in order: state (inherited from SetStateAction), stream, play_sound, show_popup (this block's own)."""
    type_id = TYPE_ID

    def __init__(self, stmt_id, cell_x=0, cell_y=0, on_complete=None, state=None, stream=None, play_sound=None, show_popup=None):
        super().__init__(stmt_id, cell_x, cell_y, on_complete)
        self.state = state
        self.stream = stream
        self.play_sound = play_sound
        self.show_popup = show_popup

    def write_fields(self, writer):
        super().write_fields(writer)
        writer.write_object(self.state)
        writer.write_object(self.stream)
        writer.write_object(self.play_sound)
        writer.write_object(self.show_popup)

    def read_fields(self, reader):
        super().read_fields(reader)
        self.state = reader.read_object()
        self.stream = reader.read_object()
        self.play_sound = reader.read_object()
        self.show_popup = reader.read_object()

    def describe(self):
        return f"AudioStreamSetMute(id={self.stmt_id})"

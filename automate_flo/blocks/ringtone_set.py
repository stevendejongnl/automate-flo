from ..base import Action

TYPE_ID = 1045


class RingtoneSet(Action):
    """id 1045, UI name "Set ringtone". Extends RingtoneAction extends
    Action directly, flattening RingtoneAction's ringtone_type field
    inline (wrap_double), plus its own required sound_uri (wrap_str --
    RequiredArgumentNullException at runtime if null) -- onComplete
    only, no continuity."""
    type_id = TYPE_ID

    def __init__(self, stmt_id, sound_uri, cell_x=0, cell_y=0, on_complete=None,
                 ringtone_type=None):
        super().__init__(stmt_id, cell_x, cell_y, on_complete)
        self.ringtone_type = ringtone_type
        self.sound_uri = sound_uri

    def write_fields(self, writer):
        super().write_fields(writer)
        writer.write_object(writer.wrap_double(self.ringtone_type))
        writer.write_object(writer.wrap_str(self.sound_uri))

    def read_fields(self, reader):
        super().read_fields(reader)
        self.ringtone_type = reader.read_object()
        self.sound_uri = reader.read_object()

    def describe(self):
        return f"RingtoneSet(id={self.stmt_id})"

from ..base import Action

TYPE_ID = 1182


class AlarmAdd(Action):
    """id 1182, UI name "Add alarm". Extends Action -- timeOfDay, weekdays,
    label, soundUri, vibrate, all nullable expression fields."""
    type_id = TYPE_ID

    def __init__(self, stmt_id, cell_x=0, cell_y=0, on_complete=None,
                 time_of_day=None, weekdays=None, label=None, sound_uri=None,
                 vibrate=None):
        super().__init__(stmt_id, cell_x, cell_y, on_complete)
        self.time_of_day = time_of_day
        self.weekdays = weekdays
        self.label = label
        self.sound_uri = sound_uri
        self.vibrate = vibrate

    def write_fields(self, writer):
        super().write_fields(writer)
        writer.write_object(writer.wrap_double(self.time_of_day))
        writer.write_object(writer.wrap_double(self.weekdays))
        writer.write_object(writer.wrap_str(self.label))
        writer.write_object(writer.wrap_str(self.sound_uri))
        writer.write_object(writer.wrap_bool(self.vibrate))

    def read_fields(self, reader):
        super().read_fields(reader)
        self.time_of_day = reader.read_object()
        self.weekdays = reader.read_object()
        self.label = reader.read_object()
        self.sound_uri = reader.read_object()
        self.vibrate = reader.read_object()

    def describe(self):
        return f"AlarmAdd(id={self.stmt_id})"

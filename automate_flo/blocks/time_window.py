from ..base import IntermittentAction

TYPE_ID = 1169


class TimeWindow(IntermittentAction):
    """id 1169, UI name "Time window" (inferred). Extends
    IntermittentAction (onComplete + proceed/continuity). Own fields in
    wire order: timeOfDay, field4, durationSeconds, field6, field7,
    field8, field9.

    The UI-name mapping is inferred from observed field values in two
    real exports (proceed = Inexact, timeOfDay = 0.0 = midnight,
    durationSeconds = 9000.0) rather than corroborated against the
    live block editor. field4 and field6-field9 were null in every
    instance observed; the documented input list (Timestamp, Duration,
    Time of day, Weekdays, Day of month, Month, Year, Time zone, Wake
    up) does not line up one-to-one with these seven slots, so the
    unknown ones are left opaque rather than guessed."""

    type_id = TYPE_ID

    def __init__(self, stmt_id, cell_x=0, cell_y=0, on_complete=None,
                 continuity=None, time_of_day=None, field4=None,
                 duration_seconds=None, field6=None, field7=None,
                 field8=None, field9=None):
        super().__init__(stmt_id, cell_x, cell_y, on_complete)
        self.continuity = continuity
        self.time_of_day = time_of_day
        self.field4 = field4
        self.duration_seconds = duration_seconds
        self.field6 = field6
        self.field7 = field7
        self.field8 = field8
        self.field9 = field9

    def write_fields(self, writer):
        super().write_fields(writer)
        writer.write_object(self.time_of_day)
        writer.write_object(self.field4)
        writer.write_object(self.duration_seconds)
        writer.write_object(self.field6)
        writer.write_object(self.field7)
        writer.write_object(self.field8)
        writer.write_object(self.field9)

    def read_fields(self, reader):
        super().read_fields(reader)
        self.time_of_day = reader.read_object()
        self.field4 = reader.read_object()
        self.duration_seconds = reader.read_object()
        self.field6 = reader.read_object()
        self.field7 = reader.read_object()
        self.field8 = reader.read_object()
        self.field9 = reader.read_object()

    def describe(self):
        return f"TimeWindow(id={self.stmt_id})"

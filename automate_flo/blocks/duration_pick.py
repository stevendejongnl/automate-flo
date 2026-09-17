from ..base import Decision

TYPE_ID = 1057


class DurationPick(Decision):
    """id 1057, UI name "Duration pick". Extends ActivityDecision extends
    Decision directly (onPositive/onNegative, no continuity -- same
    family as DialogConfirm). Flattens ActivityDecision's timeout/
    start_activity/notification_channel_id (raw pass-through) inline,
    then adds title (wrap_str), signed/show_seconds (wrap_bool),
    initial_duration (wrap_double, seconds), and var_duration
    (VariableExpr, raw pass-through)."""
    type_id = TYPE_ID

    def __init__(self, stmt_id, cell_x=0, cell_y=0, on_positive=None, on_negative=None,
                 timeout=None, start_activity=None, notification_channel_id=None,
                 title=None, signed=None, show_seconds=None, initial_duration=None,
                 var_duration=None):
        super().__init__(stmt_id, cell_x, cell_y, on_complete=None)
        self.on_positive = on_positive
        self.on_negative = on_negative
        self.timeout = timeout
        self.start_activity = start_activity
        self.notification_channel_id = notification_channel_id
        self.title = title
        self.signed = signed
        self.show_seconds = show_seconds
        self.initial_duration = initial_duration
        self.var_duration = var_duration

    def write_fields(self, writer):
        super().write_fields(writer)
        writer.write_object(self.timeout)
        writer.write_object(self.start_activity)
        writer.write_object(self.notification_channel_id)
        writer.write_object(writer.wrap_str(self.title))
        writer.write_object(writer.wrap_bool(self.signed))
        writer.write_object(writer.wrap_bool(self.show_seconds))
        writer.write_object(writer.wrap_double(self.initial_duration))
        writer.write_object(self.var_duration)

    def read_fields(self, reader):
        super().read_fields(reader)
        self.timeout = reader.read_object()
        self.start_activity = reader.read_object()
        self.notification_channel_id = reader.read_object()
        self.title = reader.read_object()
        self.signed = reader.read_object()
        self.show_seconds = reader.read_object()
        self.initial_duration = reader.read_object()
        self.var_duration = reader.read_object()

    def describe(self):
        return f"DurationPick(id={self.stmt_id})"

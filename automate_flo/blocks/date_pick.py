from ..base import Decision

TYPE_ID = 1043


class DatePick(Decision):
    """id 1043, UI name "Date pick". Extends ActivityDecision extends
    Decision directly (onPositive/onNegative, no continuity -- same
    family as ContentPick). Flattens ActivityDecision's timeout/
    start_activity/notification_channel_id (raw pass-through) inline,
    then adds title (wrap_str), style and initial_timestamp (both
    wrap_double), and var_timestamp (VariableExpr, raw pass-through)."""
    type_id = TYPE_ID

    def __init__(self, stmt_id, cell_x=0, cell_y=0, on_positive=None, on_negative=None,
                 timeout=None, start_activity=None, notification_channel_id=None,
                 title=None, style=None, initial_timestamp=None, var_timestamp=None):
        super().__init__(stmt_id, cell_x, cell_y, on_complete=None)
        self.on_positive = on_positive
        self.on_negative = on_negative
        self.timeout = timeout
        self.start_activity = start_activity
        self.notification_channel_id = notification_channel_id
        self.title = title
        self.style = style
        self.initial_timestamp = initial_timestamp
        self.var_timestamp = var_timestamp

    def write_fields(self, writer):
        super().write_fields(writer)
        writer.write_object(self.timeout)
        writer.write_object(self.start_activity)
        writer.write_object(self.notification_channel_id)
        writer.write_object(writer.wrap_str(self.title))
        writer.write_object(writer.wrap_double(self.style))
        writer.write_object(writer.wrap_double(self.initial_timestamp))
        writer.write_object(self.var_timestamp)

    def read_fields(self, reader):
        super().read_fields(reader)
        self.timeout = reader.read_object()
        self.start_activity = reader.read_object()
        self.notification_channel_id = reader.read_object()
        self.title = reader.read_object()
        self.style = reader.read_object()
        self.initial_timestamp = reader.read_object()
        self.var_timestamp = reader.read_object()

    def describe(self):
        return f"DatePick(id={self.stmt_id})"

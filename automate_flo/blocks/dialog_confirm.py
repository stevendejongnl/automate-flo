from ..base import Decision

TYPE_ID = 1053


class DialogConfirm(Decision):
    """id 1053, UI name "Confirm dialog". Extends ActivityDecision extends
    Decision directly (onPositive/onNegative, no continuity -- same
    family as DialogChoice). Flattens ActivityDecision's timeout/
    start_activity/notification_channel_id (raw pass-through) inline,
    then adds title/message/positive/negative (all wrap_str) and
    linkify (a bitmask, wrap_double)."""
    type_id = TYPE_ID

    def __init__(self, stmt_id, cell_x=0, cell_y=0, on_positive=None, on_negative=None,
                 timeout=None, start_activity=None, notification_channel_id=None,
                 title=None, message=None, linkify=None, positive=None, negative=None):
        super().__init__(stmt_id, cell_x, cell_y, on_complete=None)
        self.on_positive = on_positive
        self.on_negative = on_negative
        self.timeout = timeout
        self.start_activity = start_activity
        self.notification_channel_id = notification_channel_id
        self.title = title
        self.message = message
        self.linkify = linkify
        self.positive = positive
        self.negative = negative

    def write_fields(self, writer):
        super().write_fields(writer)
        writer.write_object(self.timeout)
        writer.write_object(self.start_activity)
        writer.write_object(self.notification_channel_id)
        writer.write_object(writer.wrap_str(self.title))
        writer.write_object(writer.wrap_str(self.message))
        writer.write_object(writer.wrap_double(self.linkify))
        writer.write_object(writer.wrap_str(self.positive))
        writer.write_object(writer.wrap_str(self.negative))

    def read_fields(self, reader):
        super().read_fields(reader)
        self.title = reader.read_object()
        self.message = reader.read_object()
        self.linkify = reader.read_object()
        self.positive = reader.read_object()
        self.negative = reader.read_object()

    def describe(self):
        return f"DialogConfirm(id={self.stmt_id})"

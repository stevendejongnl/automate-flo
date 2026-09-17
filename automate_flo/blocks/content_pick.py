from ..base import Decision

TYPE_ID = 1040


class ContentPick(Decision):
    """id 1040, UI name "Content pick". Extends ActivityDecision extends
    Decision directly (onPositive/onNegative, no continuity -- same
    family as ContactPick). Flattens ActivityDecision's timeout/
    start_activity/notification_channel_id (raw pass-through) inline,
    then adds its own mime_type (wrap_str), persistent (wrap_bool),
    var_content_uri and var_content_mime_type (VariableExpr, raw
    pass-through)."""
    type_id = TYPE_ID

    def __init__(self, stmt_id, cell_x=0, cell_y=0, on_positive=None, on_negative=None,
                 timeout=None, start_activity=None, notification_channel_id=None,
                 mime_type=None, persistent=None, var_content_uri=None,
                 var_content_mime_type=None):
        super().__init__(stmt_id, cell_x, cell_y, on_complete=None)
        self.on_positive = on_positive
        self.on_negative = on_negative
        self.timeout = timeout
        self.start_activity = start_activity
        self.notification_channel_id = notification_channel_id
        self.mime_type = mime_type
        self.persistent = persistent
        self.var_content_uri = var_content_uri
        self.var_content_mime_type = var_content_mime_type

    def write_fields(self, writer):
        super().write_fields(writer)
        writer.write_object(self.timeout)
        writer.write_object(self.start_activity)
        writer.write_object(self.notification_channel_id)
        writer.write_object(writer.wrap_str(self.mime_type))
        writer.write_object(writer.wrap_bool(self.persistent))
        writer.write_object(self.var_content_uri)
        writer.write_object(self.var_content_mime_type)

    def read_fields(self, reader):
        super().read_fields(reader)
        self.timeout = reader.read_object()
        self.start_activity = reader.read_object()
        self.notification_channel_id = reader.read_object()
        self.mime_type = reader.read_object()
        self.persistent = reader.read_object()
        self.var_content_uri = reader.read_object()
        self.var_content_mime_type = reader.read_object()

    def describe(self):
        return f"ContentPick(id={self.stmt_id})"

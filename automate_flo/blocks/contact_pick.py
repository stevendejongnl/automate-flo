from ..base import Decision

TYPE_ID = 1038


class ContactPick(Decision):
    """id 1038, UI name "Contact pick". Extends ActivityDecision extends
    Decision directly (onPositive/onNegative, no continuity). Flattens
    ActivityDecision's timeout/start_activity/notification_channel_id
    (raw pass-through) inline, then adds one field of its own:
    var_contact_uri (VariableExpr, raw pass-through)."""
    type_id = TYPE_ID

    def __init__(self, stmt_id, cell_x=0, cell_y=0, on_positive=None, on_negative=None,
                 timeout=None, start_activity=None, notification_channel_id=None,
                 var_contact_uri=None):
        super().__init__(stmt_id, cell_x, cell_y, on_complete=None)
        self.on_positive = on_positive
        self.on_negative = on_negative
        self.timeout = timeout
        self.start_activity = start_activity
        self.notification_channel_id = notification_channel_id
        self.var_contact_uri = var_contact_uri

    def write_fields(self, writer):
        super().write_fields(writer)
        writer.write_object(self.timeout)
        writer.write_object(self.start_activity)
        writer.write_object(self.notification_channel_id)
        writer.write_object(self.var_contact_uri)

    def read_fields(self, reader):
        super().read_fields(reader)
        self.timeout = reader.read_object()
        self.start_activity = reader.read_object()
        self.notification_channel_id = reader.read_object()
        self.var_contact_uri = reader.read_object()

    def describe(self):
        return f"ContactPick(id={self.stmt_id})"

from ..base import Decision, StringExpr

TYPE_ID = 1002


class ActivityStartResult(Decision):
    """id 1002, UI name "App start for result". Extends ActivityIntentDecision
    extends IntentDecision extends Decision. Decision.S() calls its u(dVar)
    hook (overridden here to write timeout/startActivity/
    notificationChannelId) BEFORE IntentDecision.S() appends its own
    packageName..flags fields -- so the wire order interleaves the two
    parent classes: onPositive, onNegative, timeout, startActivity,
    notificationChannelId, THEN packageName..flags, THEN this class's own
    activityOptions/varResultUri/varResultExtras. All version gates (9, 73,
    77, 89) are always satisfied at version 114."""
    type_id = TYPE_ID

    def __init__(self, stmt_id, package_name, cell_x=0, cell_y=0,
                 on_positive=None, on_negative=None, timeout=None,
                 start_activity=None, notification_channel_id=None,
                 class_name=None, action=None, uri=None, mime_type=None,
                 categories=None, extras=None, flags=None,
                 activity_options=None, var_result_uri=None,
                 var_result_extras=None):
        super().__init__(stmt_id, cell_x, cell_y, on_complete=None)
        self.on_positive = on_positive
        self.on_negative = on_negative
        self.timeout = timeout
        self.start_activity = start_activity
        self.notification_channel_id = notification_channel_id
        self.package_name = package_name
        self.class_name = class_name
        self.action = action
        self.uri = uri
        self.mime_type = mime_type
        self.categories = categories
        self.extras = extras
        self.flags = flags
        self.activity_options = activity_options
        self.var_result_uri = var_result_uri
        self.var_result_extras = var_result_extras

    def write_fields(self, writer):
        super().write_fields(writer)
        writer.write_object(self.timeout)
        writer.write_object(self.start_activity)           # version 114 >= 9
        writer.write_object(self.notification_channel_id)  # version 114 >= 77
        writer.write_object(StringExpr(self.package_name))
        writer.write_object(self.class_name)
        writer.write_object(self.action)
        writer.write_object(self.uri)
        writer.write_object(self.mime_type)
        writer.write_object(self.categories)
        writer.write_object(self.extras)
        writer.write_object(self.flags)              # version 114 >= 73
        writer.write_object(self.activity_options)   # version 114 >= 89
        writer.write_object(self.var_result_uri)
        writer.write_object(self.var_result_extras)

    def read_fields(self, reader):
        super().read_fields(reader)
        self.timeout = reader.read_object()
        self.start_activity = reader.read_object()
        self.notification_channel_id = reader.read_object()
        pkg = reader.read_object()
        self.package_name = pkg.value if pkg is not None else None
        self.class_name = reader.read_object()
        self.action = reader.read_object()
        self.uri = reader.read_object()
        self.mime_type = reader.read_object()
        self.categories = reader.read_object()
        self.extras = reader.read_object()
        self.flags = reader.read_object()
        self.activity_options = reader.read_object()
        self.var_result_uri = reader.read_object()
        self.var_result_extras = reader.read_object()

    def describe(self):
        return f"ActivityStartResult(id={self.stmt_id}, package={self.package_name!r})"

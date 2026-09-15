from ..base import Decision

TYPE_ID = 1237


class AppPick(Decision):
    """id 1237, UI name "App pick". Extends ActivityDecision extends Decision directly. Decision.S() calls super() first (writing onPositive/onNegative), then ActivityDecision adds timeout/startActivity/notificationChannelId (all version gates satisfied at version 114), then AppPick's own flagsInclude/flagsExclude/states/varPackageName (also version-gated fields but all satisfied at 114)."""
    type_id = TYPE_ID

    def __init__(self, stmt_id, cell_x=0, cell_y=0, on_positive=None, on_negative=None, timeout=None, start_activity=None, notification_channel_id=None, flags_include=None, flags_exclude=None, states=None, var_package_name=None):
        super().__init__(stmt_id, cell_x, cell_y, on_complete=None)
        self.on_positive = on_positive
        self.on_negative = on_negative
        self.timeout = timeout
        self.start_activity = start_activity
        self.notification_channel_id = notification_channel_id
        self.flags_include = flags_include
        self.flags_exclude = flags_exclude
        self.states = states
        self.var_package_name = var_package_name

    def write_fields(self, writer):
        super().write_fields(writer)
        writer.write_object(self.timeout)
        writer.write_object(self.start_activity)
        writer.write_object(self.notification_channel_id)
        writer.write_object(writer.wrap_double(self.flags_include))
        writer.write_object(writer.wrap_double(self.flags_exclude))
        writer.write_object(writer.wrap_double(self.states))
        writer.write_object(self.var_package_name)

    def read_fields(self, reader):
        super().read_fields(reader)
        self.timeout = reader.read_object()
        self.start_activity = reader.read_object()
        self.notification_channel_id = reader.read_object()
        self.flags_include = reader.read_object()
        self.flags_exclude = reader.read_object()
        self.states = reader.read_object()
        self.var_package_name = reader.read_object()

    def describe(self):
        return f"AppPick(id={self.stmt_id})"

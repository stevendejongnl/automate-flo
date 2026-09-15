from ..base import Decision

TYPE_ID = 1000


class AccountPick(Decision):
    """id 1000, UI name "Account pick?". Extends ActivityDecision extends
    Decision DIRECTLY (like ExpressionDecision) -- onPositive/onNegative,
    no continuity, then ActivityDecision's own timeout/startActivity/
    notificationChannelId (all version-gated in source but always true
    for the version this library targets), then accountType (input
    filter) and the two output variables. The live edit screen only
    surfaces "Show window directly if possible" (startActivity) and the
    two output variables as visible widgets -- timeout/notificationChannelId/
    accountType aren't shown but are still always present in the wire
    format per source; confirmed null-safe on-device (this is the
    picker-block null-field escape hatch noted in HANDOFF.md)."""
    type_id = TYPE_ID

    def __init__(self, stmt_id, cell_x=0, cell_y=0, on_positive=None,
                 on_negative=None, timeout=None, start_activity=None,
                 notification_channel_id=None, account_type=None,
                 var_picked_account_name=None, var_picked_account_type=None):
        super().__init__(stmt_id, cell_x, cell_y, on_complete=None)
        self.on_positive = on_positive
        self.on_negative = on_negative
        self.timeout = timeout
        self.start_activity = start_activity
        self.notification_channel_id = notification_channel_id
        self.account_type = account_type
        self.var_picked_account_name = var_picked_account_name
        self.var_picked_account_type = var_picked_account_type

    def write_fields(self, writer):
        super().write_fields(writer)
        writer.write_object(self.timeout)
        writer.write_object(self.start_activity)          # version 114 >= 9
        writer.write_object(self.notification_channel_id)  # version 114 >= 77
        writer.write_object(self.account_type)
        writer.write_object(self.var_picked_account_name)
        writer.write_object(self.var_picked_account_type)

    def read_fields(self, reader):
        super().read_fields(reader)
        self.timeout = reader.read_object()
        self.start_activity = reader.read_object()
        self.notification_channel_id = reader.read_object()
        self.account_type = reader.read_object()
        self.var_picked_account_name = reader.read_object()
        self.var_picked_account_type = reader.read_object()

    def describe(self):
        return f"AccountPick(id={self.stmt_id})"

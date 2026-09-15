from ..base import IntermittentDecision

TYPE_ID = 1019


class AccountSyncEnabled(IntermittentDecision):
    """id 1019, UI name "Account sync enabled?". Extends IntermittentDecision
    directly -- onPositive/onNegative/continuity, plus accountName/
    accountType/authority. The live edit screen shows a "Pick account"
    picker widget instead of separate text fields, but the wire format
    always has all three per source; confirmed null-safe on-device."""
    type_id = TYPE_ID

    def __init__(self, stmt_id, cell_x=0, cell_y=0, on_positive=None,
                 on_negative=None, continuity=None, account_name=None,
                 account_type=None, authority=None):
        super().__init__(stmt_id, cell_x, cell_y, on_complete=None)
        self.on_positive = on_positive
        self.on_negative = on_negative
        self.continuity = continuity
        self.account_name = account_name
        self.account_type = account_type
        self.authority = authority

    def write_fields(self, writer):
        super().write_fields(writer)
        writer.write_object(writer.wrap_str(self.account_name))
        writer.write_object(writer.wrap_str(self.account_type))
        writer.write_object(writer.wrap_str(self.authority))

    def read_fields(self, reader):
        super().read_fields(reader)
        self.account_name = reader.read_object()
        self.account_type = reader.read_object()
        self.authority = reader.read_object()

    def describe(self):
        return f"AccountSyncEnabled(id={self.stmt_id})"

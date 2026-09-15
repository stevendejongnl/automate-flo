from ..base import Action

TYPE_ID = 1020


class AccountSyncSetState(Action):
    """id 1020, UI name "Account sync set state". Extends SetStateAction
    extends Action -- state (boolean expression), then accountName/
    accountType/authority, all nullable."""
    type_id = TYPE_ID

    def __init__(self, stmt_id, state, account_name=None, account_type=None,
                 authority=None, cell_x=0, cell_y=0, on_complete=None):
        super().__init__(stmt_id, cell_x, cell_y, on_complete)
        self.state = state
        self.account_name = account_name
        self.account_type = account_type
        self.authority = authority

    def write_fields(self, writer):
        super().write_fields(writer)
        writer.write_object(writer.wrap_bool(self.state))
        writer.write_object(writer.wrap_str(self.account_name))
        writer.write_object(writer.wrap_str(self.account_type))
        writer.write_object(writer.wrap_str(self.authority))

    def read_fields(self, reader):
        super().read_fields(reader)
        self.state = reader.read_object()
        self.account_name = reader.read_object()
        self.account_type = reader.read_object()
        self.authority = reader.read_object()

    def describe(self):
        return f"AccountSyncSetState(id={self.stmt_id})"

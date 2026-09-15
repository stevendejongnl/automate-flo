from ..base import Action

TYPE_ID = 1236


class AccountGenericAdd(Action):
    """id 1236, UI name "Account generic add" -- confirmed via live edit
    screen: exactly 3 text fields in order, accountName/username/password,
    all legal to leave null. Extends Action."""
    type_id = TYPE_ID

    def __init__(self, stmt_id, account_name=None, username=None, password=None,
                 cell_x=0, cell_y=0, on_complete=None):
        super().__init__(stmt_id, cell_x, cell_y, on_complete)
        self.account_name = account_name
        self.username = username
        self.password = password

    def write_fields(self, writer):
        super().write_fields(writer)
        writer.write_object(writer.wrap_str(self.account_name))
        writer.write_object(writer.wrap_str(self.username))
        writer.write_object(writer.wrap_str(self.password))

    def read_fields(self, reader):
        super().read_fields(reader)
        self.account_name = reader.read_object()
        self.username = reader.read_object()
        self.password = reader.read_object()

    def describe(self):
        return f"AccountGenericAdd(id={self.stmt_id})"

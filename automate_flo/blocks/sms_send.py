from ..base import IntermittentAction

TYPE_ID = 1122


class SmsSend(IntermittentAction):
    """id 1122, UI name "Send SMS". Extends IntermittentAction."""
    type_id = TYPE_ID

    def __init__(self, stmt_id, phone_number, message, cell_x=0, cell_y=0,
                 on_complete=None, continuity=None, subscription_id=None,
                 multipart_limit=None, hidden=None, var_multipart_count=None):
        super().__init__(stmt_id, cell_x, cell_y, on_complete)
        self.continuity = continuity
        self.phone_number = phone_number
        self.subscription_id = subscription_id
        self.message = message
        self.multipart_limit = multipart_limit
        self.hidden = hidden
        self.var_multipart_count = var_multipart_count

    def write_fields(self, writer):
        super().write_fields(writer)
        writer.write_object(writer.wrap_str(self.phone_number))
        writer.write_object(self.subscription_id)     # version 114 >= 45
        writer.write_object(writer.wrap_str(self.message))
        writer.write_object(self.multipart_limit)
        writer.write_object(self.hidden)
        writer.write_object(self.var_multipart_count)  # version 114 >= 97

    def read_fields(self, reader):
        super().read_fields(reader)
        self.phone_number = reader.read_object()
        self.subscription_id = reader.read_object()
        self.message = reader.read_object()
        self.multipart_limit = reader.read_object()
        self.hidden = reader.read_object()
        self.var_multipart_count = reader.read_object()

    def describe(self):
        return f"SmsSend(id={self.stmt_id})"

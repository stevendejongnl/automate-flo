from ..base import Decision

TYPE_ID = 1037


class ContactQuery(Decision):
    """id 1037, UI name "Contact query". Extends Decision directly
    (onPositive/onNegative, no continuity -- same family as AppPick).
    query_value/value_type are plain string expressions (wrap_str). The
    remaining 8 var_* fields are VariableExpr output bindings, raw
    pass-through, in order: var_display_name, var_nickname, var_company,
    var_phone_number, var_email, var_postal_address, var_groups, var_uri."""
    type_id = TYPE_ID

    def __init__(self, stmt_id, cell_x=0, cell_y=0, on_positive=None, on_negative=None,
                 query_value=None, value_type=None, var_display_name=None,
                 var_nickname=None, var_company=None, var_phone_number=None,
                 var_email=None, var_postal_address=None, var_groups=None, var_uri=None):
        super().__init__(stmt_id, cell_x, cell_y, on_complete=None)
        self.on_positive = on_positive
        self.on_negative = on_negative
        self.query_value = query_value
        self.value_type = value_type
        self.var_display_name = var_display_name
        self.var_nickname = var_nickname
        self.var_company = var_company
        self.var_phone_number = var_phone_number
        self.var_email = var_email
        self.var_postal_address = var_postal_address
        self.var_groups = var_groups
        self.var_uri = var_uri

    def write_fields(self, writer):
        super().write_fields(writer)
        writer.write_object(writer.wrap_str(self.query_value))
        writer.write_object(writer.wrap_str(self.value_type))
        writer.write_object(self.var_display_name)
        writer.write_object(self.var_nickname)
        writer.write_object(self.var_company)
        writer.write_object(self.var_phone_number)
        writer.write_object(self.var_email)
        writer.write_object(self.var_postal_address)
        writer.write_object(self.var_groups)
        writer.write_object(self.var_uri)

    def read_fields(self, reader):
        super().read_fields(reader)
        self.query_value = reader.read_object()
        self.value_type = reader.read_object()
        self.var_display_name = reader.read_object()
        self.var_nickname = reader.read_object()
        self.var_company = reader.read_object()
        self.var_phone_number = reader.read_object()
        self.var_email = reader.read_object()
        self.var_postal_address = reader.read_object()
        self.var_groups = reader.read_object()
        self.var_uri = reader.read_object()

    def describe(self):
        return f"ContactQuery(id={self.stmt_id})"

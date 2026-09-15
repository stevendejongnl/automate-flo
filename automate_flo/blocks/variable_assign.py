from ..base import Action, VariableExpr

TYPE_ID = 1012


class VariableAssign(Action):
    """id 1012, UI name "Assign variable". Extends Action."""
    type_id = TYPE_ID

    def __init__(self, stmt_id, variable_name, value, cell_x=0, cell_y=0, on_complete=None):
        super().__init__(stmt_id, cell_x, cell_y, on_complete)
        self.variable_name = variable_name
        self.value = value

    def write_fields(self, writer):
        super().write_fields(writer)
        writer.write_object(writer.wrap_str(self.value))
        writer.write_object(VariableExpr(self.variable_name))

    def read_fields(self, reader):
        super().read_fields(reader)
        self.value = reader.read_object()
        var = reader.read_object()
        self.variable_name = var.name if var is not None else None

    def describe(self):
        return f"VariableAssign(id={self.stmt_id}, variable={self.variable_name!r})"

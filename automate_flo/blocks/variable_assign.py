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
        # Pass an already-built VariableExpr through as-is: real flows
        # back-reference one shared variable object from several Assign
        # blocks, and re-constructing here would silently drop that
        # sharing on a parse->write round trip. Plain strings (the
        # common hand-built case) are wrapped as before.
        if self.variable_name is None or hasattr(self.variable_name, "type_id"):
            writer.write_object(self.variable_name)
        else:
            writer.write_object(VariableExpr(self.variable_name))

    def read_fields(self, reader):
        super().read_fields(reader)
        self.value = reader.read_object()
        # Keep the parsed object (not just its name) so a shared
        # variable reference survives a round trip.
        self.variable_name = reader.read_object()

    def describe(self):
        return f"VariableAssign(id={self.stmt_id}, variable={self.variable_name!r})"

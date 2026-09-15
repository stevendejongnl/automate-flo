from ..base import Action

TYPE_ID = 1010


class ArrayRemove(Action):
    """id 1010, UI name "Remove array element". Extends ArraySubscriptAction extends Action -- index and varArray duplicated inline. Fields: index (numeric expression), varArray (VariableExpr), varOldValue (VariableExpr, raw pass-through)."""
    type_id = TYPE_ID

    def __init__(self, stmt_id, cell_x=0, cell_y=0, on_complete=None, index=None, var_array=None, var_old_value=None):
        super().__init__(stmt_id, cell_x, cell_y, on_complete)
        self.index = index
        self.var_array = var_array
        self.var_old_value = var_old_value

    def write_fields(self, writer):
        super().write_fields(writer)
        writer.write_object(writer.wrap_double(self.index))
        writer.write_object(self.var_array)
        writer.write_object(self.var_old_value)

    def read_fields(self, reader):
        super().read_fields(reader)
        self.index = reader.read_object()
        self.var_array = reader.read_object()
        self.var_old_value = reader.read_object()

    def describe(self):
        return f"ArrayRemove(id={self.stmt_id})"

from ..base import Action

TYPE_ID = 1011


class ArraySet(Action):
    """id 1011, UI name "Set array element". Extends ArraySubscriptAction extends Action -- index and varArray duplicated inline per this library's convention (not a shared Python base, since only 3 blocks -- ArrayAdd/ArrayRemove/ArraySet -- share them). Fields: index (numeric expression), varArray (VariableExpr), value (generic expression field, wrap_str)."""
    type_id = TYPE_ID

    def __init__(self, stmt_id, cell_x=0, cell_y=0, on_complete=None, index=None, var_array=None, value=None):
        super().__init__(stmt_id, cell_x, cell_y, on_complete)
        self.index = index
        self.var_array = var_array
        self.value = value

    def write_fields(self, writer):
        super().write_fields(writer)
        writer.write_object(writer.wrap_double(self.index))
        writer.write_object(self.var_array)
        writer.write_object(writer.wrap_str(self.value))

    def read_fields(self, reader):
        super().read_fields(reader)
        self.index = reader.read_object()
        self.var_array = reader.read_object()
        self.value = reader.read_object()

    def describe(self):
        return f"ArraySet(id={self.stmt_id})"

from ..base import Action

TYPE_ID = 1305


class AppList(Action):
    """id 1305, UI name "List apps". Extends Action. Four optional numeric-expression fields (flags_include, flags_exclude, states, categories -- bitmask/enum values, wrapped via writer.wrap_double so plain ints can be passed), then two variable-reference fields (var_package_names, var_display_names -- raw VariableExpr pass-through, no wrapping)."""

    type_id = TYPE_ID

    def __init__(self, stmt_id, cell_x=0, cell_y=0, on_complete=None, flags_include=None, flags_exclude=None, states=None, categories=None, var_package_names=None, var_display_names=None):
        super().__init__(stmt_id, cell_x, cell_y, on_complete)
        self.flags_include = flags_include
        self.flags_exclude = flags_exclude
        self.states = states
        self.categories = categories
        self.var_package_names = var_package_names
        self.var_display_names = var_display_names

    def write_fields(self, writer):
        super().write_fields(writer)
        writer.write_object(writer.wrap_double(self.flags_include))
        writer.write_object(writer.wrap_double(self.flags_exclude))
        writer.write_object(writer.wrap_double(self.states))
        writer.write_object(writer.wrap_double(self.categories))
        writer.write_object(self.var_package_names)
        writer.write_object(self.var_display_names)

    def read_fields(self, reader):
        super().read_fields(reader)
        self.flags_include = reader.read_object()
        self.flags_exclude = reader.read_object()
        self.states = reader.read_object()
        self.categories = reader.read_object()
        self.var_package_names = reader.read_object()
        self.var_display_names = reader.read_object()

    def describe(self):
        return f"AppList(id={self.stmt_id})"

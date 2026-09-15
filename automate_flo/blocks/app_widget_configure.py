from ..base import Action

TYPE_ID = 1421


class AppWidgetConfigure(Action):
    """id 1421, UI name "App widget configure". Extends Action. Fields, no version gates: title (string expression), hostCategories (numeric expression), varInterfaceUri, varHostCategory (VariableExpr, raw pass-through)."""
    type_id = TYPE_ID

    def __init__(self, stmt_id, cell_x=0, cell_y=0, on_complete=None, title=None, host_categories=None, var_interface_uri=None, var_host_category=None):
        super().__init__(stmt_id, cell_x, cell_y, on_complete)
        self.title = title
        self.host_categories = host_categories
        self.var_interface_uri = var_interface_uri
        self.var_host_category = var_host_category

    def write_fields(self, writer):
        super().write_fields(writer)
        writer.write_object(writer.wrap_str(self.title))
        writer.write_object(writer.wrap_double(self.host_categories))
        writer.write_object(self.var_interface_uri)
        writer.write_object(self.var_host_category)

    def read_fields(self, reader):
        super().read_fields(reader)
        self.title = reader.read_object()
        self.host_categories = reader.read_object()
        self.var_interface_uri = reader.read_object()
        self.var_host_category = reader.read_object()

    def describe(self):
        return f"AppWidgetConfigure(id={self.stmt_id})"

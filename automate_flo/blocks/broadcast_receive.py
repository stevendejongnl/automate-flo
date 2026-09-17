from ..base import Action

TYPE_ID = 1022


class BroadcastReceive(Action):
    """id 1022, UI name "Broadcast received". Extends Action directly (onComplete only, no continuity).
    Required fields: action (string expression).
    Optional fields: categories (array-of-category-strings), uri_scheme (string expression),
    uri_authority (string expression), uri_path (string expression), mime_type (string expression),
    use_sticky (boolean expression), var_broadcast_action (VariableExpr), var_broadcast_categories (VariableExpr),
    var_broadcast_uri (VariableExpr), var_broadcast_mime_type (VariableExpr), var_broadcast_extras (VariableExpr)."""
    type_id = TYPE_ID

    def __init__(self, stmt_id, action, cell_x=0, cell_y=0, on_complete=None,
                 categories=None, uri_scheme=None, uri_authority=None, uri_path=None,
                 mime_type=None, use_sticky=None, var_broadcast_action=None,
                 var_broadcast_categories=None, var_broadcast_uri=None,
                 var_broadcast_mime_type=None, var_broadcast_extras=None):
        super().__init__(stmt_id, cell_x, cell_y, on_complete)
        self.action = action
        self.categories = categories
        self.uri_scheme = uri_scheme
        self.uri_authority = uri_authority
        self.uri_path = uri_path
        self.mime_type = mime_type
        self.use_sticky = use_sticky
        self.var_broadcast_action = var_broadcast_action
        self.var_broadcast_categories = var_broadcast_categories
        self.var_broadcast_uri = var_broadcast_uri
        self.var_broadcast_mime_type = var_broadcast_mime_type
        self.var_broadcast_extras = var_broadcast_extras

    def write_fields(self, writer):
        super().write_fields(writer)
        writer.write_object(writer.wrap_str(self.action))
        writer.write_object(self.categories)
        writer.write_object(writer.wrap_str(self.uri_scheme))
        writer.write_object(writer.wrap_str(self.uri_authority))
        writer.write_object(writer.wrap_str(self.uri_path))
        writer.write_object(writer.wrap_str(self.mime_type))
        writer.write_object(writer.wrap_bool(self.use_sticky))
        writer.write_object(self.var_broadcast_action)
        writer.write_object(self.var_broadcast_categories)
        writer.write_object(self.var_broadcast_uri)
        writer.write_object(self.var_broadcast_mime_type)
        writer.write_object(self.var_broadcast_extras)

    def read_fields(self, reader):
        super().read_fields(reader)
        self.action = reader.read_object()
        self.categories = reader.read_object()
        self.uri_scheme = reader.read_object()
        self.uri_authority = reader.read_object()
        self.uri_path = reader.read_object()
        self.mime_type = reader.read_object()
        self.use_sticky = reader.read_object()
        self.var_broadcast_action = reader.read_object()
        self.var_broadcast_categories = reader.read_object()
        self.var_broadcast_uri = reader.read_object()
        self.var_broadcast_mime_type = reader.read_object()
        self.var_broadcast_extras = reader.read_object()

    def describe(self):
        return f"BroadcastReceive(id={self.stmt_id})"

from ..base import Action

TYPE_ID = 1013


class AssistRequest(Action):
    """id 1013, UI name "Assist request". Extends Action. Fields, all version gates satisfied at version 114: title (string expression), visibility (numeric expression), varPackageName, varActivityClassName, varIntentAction, varIntentCategories, varIntentUri, varIntentMimeType, varIntentExtras, varWebUri (all VariableExpr, raw pass-through)."""
    type_id = TYPE_ID

    def __init__(self, stmt_id, cell_x=0, cell_y=0, on_complete=None, title=None, visibility=None, var_package_name=None, var_activity_class_name=None, var_intent_action=None, var_intent_categories=None, var_intent_uri=None, var_intent_mime_type=None, var_intent_extras=None, var_web_uri=None):
        super().__init__(stmt_id, cell_x, cell_y, on_complete)
        self.title = title
        self.visibility = visibility
        self.var_package_name = var_package_name
        self.var_activity_class_name = var_activity_class_name
        self.var_intent_action = var_intent_action
        self.var_intent_categories = var_intent_categories
        self.var_intent_uri = var_intent_uri
        self.var_intent_mime_type = var_intent_mime_type
        self.var_intent_extras = var_intent_extras
        self.var_web_uri = var_web_uri

    def write_fields(self, writer):
        super().write_fields(writer)
        writer.write_object(writer.wrap_str(self.title))
        writer.write_object(writer.wrap_double(self.visibility))
        writer.write_object(self.var_package_name)
        writer.write_object(self.var_activity_class_name)
        writer.write_object(self.var_intent_action)
        writer.write_object(self.var_intent_categories)
        writer.write_object(self.var_intent_uri)
        writer.write_object(self.var_intent_mime_type)
        writer.write_object(self.var_intent_extras)
        writer.write_object(self.var_web_uri)

    def read_fields(self, reader):
        super().read_fields(reader)
        self.title = reader.read_object()
        self.visibility = reader.read_object()
        self.var_package_name = reader.read_object()
        self.var_activity_class_name = reader.read_object()
        self.var_intent_action = reader.read_object()
        self.var_intent_categories = reader.read_object()
        self.var_intent_uri = reader.read_object()
        self.var_intent_mime_type = reader.read_object()
        self.var_intent_extras = reader.read_object()
        self.var_web_uri = reader.read_object()

    def describe(self):
        return f"AssistRequest(id={self.stmt_id})"

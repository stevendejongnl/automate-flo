from ..base import Action

TYPE_ID = 1056


class DictionaryRemove(Action):
    """id 1056, UI name "Dictionary remove". Extends DictionarySubscriptAction
    extends Action directly, flattening the base's key/var_dictionary/
    var_old_value fields inline, with no extra fields of its own --
    onComplete only, no continuity. var_dictionary is required
    (RequiredVariableMissingException at runtime if null)."""
    type_id = TYPE_ID

    def __init__(self, stmt_id, var_dictionary, cell_x=0, cell_y=0, on_complete=None,
                 key=None, var_old_value=None):
        super().__init__(stmt_id, cell_x, cell_y, on_complete)
        self.key = key
        self.var_dictionary = var_dictionary
        self.var_old_value = var_old_value

    def write_fields(self, writer):
        super().write_fields(writer)
        writer.write_object(self.key)
        writer.write_object(self.var_dictionary)
        writer.write_object(self.var_old_value)

    def read_fields(self, reader):
        super().read_fields(reader)
        self.key = reader.read_object()
        self.var_dictionary = reader.read_object()
        self.var_old_value = reader.read_object()

    def describe(self):
        return f"DictionaryRemove(id={self.stmt_id})"

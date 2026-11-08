from ..base import Action

TYPE_ID = 1073


class ForEach(Action):
    """id 1073, UI name "For each". Extends Action directly: the
    inherited onComplete slot carries the loop's OK path (taken when
    iteration completes). Own fields in wire order: on_do (the DO path,
    taken per element -- the DO chain must loop back to this block's
    IN dot), container, until, varEntryValue, varEntryIndex,
    varDictionaryKey.

    Container and the entry-value variable are confirmed across six
    For-each instances in two real exports ({PackageName}, {ApkFile},
    {Old}); the until/entry-index/dictionary-key assignment for the
    remaining slots is inferred from the documented inputs-before-
    outputs order (all three were null in every instance observed) and
    is not yet corroborated."""

    type_id = TYPE_ID

    def __init__(self, stmt_id, cell_x=0, cell_y=0, on_ok=None, on_do=None,
                 container=None, until=None, var_entry_value=None,
                 var_entry_index=None, var_dictionary_key=None):
        super().__init__(stmt_id, cell_x, cell_y, on_ok)
        self.on_do = on_do
        self.container = container
        self.until = until
        self.var_entry_value = var_entry_value
        self.var_entry_index = var_entry_index
        self.var_dictionary_key = var_dictionary_key

    def write_fields(self, writer):
        super().write_fields(writer)
        writer.write_object(self.on_do)
        writer.write_object(self.container)
        writer.write_object(self.until)
        writer.write_object(self.var_entry_value)
        writer.write_object(self.var_entry_index)
        writer.write_object(self.var_dictionary_key)

    def read_fields(self, reader):
        super().read_fields(reader)
        self.on_do = reader.read_object()
        self.container = reader.read_object()
        self.until = reader.read_object()
        self.var_entry_value = reader.read_object()
        self.var_entry_index = reader.read_object()
        self.var_dictionary_key = reader.read_object()

    def describe(self):
        return f"ForEach(id={self.stmt_id})"

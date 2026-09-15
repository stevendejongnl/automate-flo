from ..base import Action

TYPE_ID = 1288


class Label(Action):
    """id 1288, UI name "Label". Extends Action -- a jump target for Goto;
    this library doesn't implement Goto (its field layout involves a
    counted array of back-references to Label nodes plus a dynamic
    label-value expression -- meaningfully more complex than the rest of
    this batch, not attempted here). Label itself is just an Action with
    one extra 'value' field (the label's name/id expression) and is useful
    on its own as a connectable no-op anchor."""
    type_id = TYPE_ID

    def __init__(self, stmt_id, value=None, cell_x=0, cell_y=0, on_complete=None):
        super().__init__(stmt_id, cell_x, cell_y, on_complete)
        self.value = value

    def write_fields(self, writer):
        super().write_fields(writer)
        writer.write_object(self.value)

    def read_fields(self, reader):
        super().read_fields(reader)
        self.value = reader.read_object()

    def describe(self):
        return f"Label(id={self.stmt_id})"

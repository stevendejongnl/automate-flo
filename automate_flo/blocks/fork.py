from ..base import Action

TYPE_ID = 1060


class Fork(Action):
    """id 1060, UI name "Fork". Extends Action directly. After
    onComplete (the OK path, taken by the current fiber) comes one more
    connection slot: NEW, taken by the newly spawned child fiber.

    Layout cross-verified between two real exports; the OK/NEW
    assignment is inferred from fiber semantics (the parent parks while
    the child works) and not yet corroborated against the live block
    editor."""

    type_id = TYPE_ID

    def __init__(self, stmt_id, cell_x=0, cell_y=0, on_ok=None, on_new=None):
        super().__init__(stmt_id, cell_x, cell_y, on_ok)
        self.on_new = on_new

    def write_fields(self, writer):
        super().write_fields(writer)
        writer.write_object(self.on_new)

    def read_fields(self, reader):
        super().read_fields(reader)
        self.on_new = reader.read_object()

    def describe(self):
        return f"Fork(id={self.stmt_id})"

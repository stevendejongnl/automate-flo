from ..base import Action

TYPE_ID = 1334


class AccessibilityButton(Action):
    """id 1334, UI name "Accessibility button" -- confirmed via live
    search: opening the real edit screen shows no additional input fields,
    consistent with displayId being valid left null/absent. Extends
    Action."""
    type_id = TYPE_ID

    def __init__(self, stmt_id, display_id=None, cell_x=0, cell_y=0, on_complete=None):
        super().__init__(stmt_id, cell_x, cell_y, on_complete)
        self.display_id = display_id

    def write_fields(self, writer):
        super().write_fields(writer)
        writer.write_object(self.display_id)

    def read_fields(self, reader):
        super().read_fields(reader)
        self.display_id = reader.read_object()

    def describe(self):
        return f"AccessibilityButton(id={self.stmt_id})"

from ..base import Action

TYPE_ID = 1114


class ScreenBrightnessSet(Action):
    """id 1114, UI name "Set screen brightness". Extends Action."""
    type_id = TYPE_ID

    def __init__(self, stmt_id, level=None, cell_x=0, cell_y=0, on_complete=None,
                 scale=None, auto=None, adjustment=None):
        super().__init__(stmt_id, cell_x, cell_y, on_complete)
        self.level = level
        self.scale = scale
        self.auto = auto
        self.adjustment = adjustment

    def write_fields(self, writer):
        super().write_fields(writer)
        writer.write_object(writer.wrap_double(self.level))
        writer.write_object(self.scale)
        writer.write_object(self.auto)
        writer.write_object(self.adjustment)

    def read_fields(self, reader):
        super().read_fields(reader)
        self.level = reader.read_object()
        self.scale = reader.read_object()
        self.auto = reader.read_object()
        self.adjustment = reader.read_object()

    def describe(self):
        return f"ScreenBrightnessSet(id={self.stmt_id})"

from ..base import LevelDecision

TYPE_ID = 1113


class ScreenBrightness(LevelDecision):
    """id 1113, UI name "Screen brightness". Extends LevelDecision (minLevel,
    maxLevel, varLevel) plus scale/auto/varAuto/varAdjustment."""
    type_id = TYPE_ID

    def __init__(self, stmt_id, cell_x=0, cell_y=0, on_positive=None,
                 on_negative=None, continuity=None, min_level=None,
                 max_level=None, var_level=None, scale=None, auto=None,
                 var_auto=None, var_adjustment=None):
        super().__init__(stmt_id, cell_x, cell_y, on_complete=None)
        self.on_positive = on_positive
        self.on_negative = on_negative
        self.continuity = continuity
        self.min_level = min_level
        self.max_level = max_level
        self.var_level = var_level
        self.scale = scale
        self.auto = auto
        self.var_auto = var_auto
        self.var_adjustment = var_adjustment

    def write_fields(self, writer):
        super().write_fields(writer)
        writer.write_object(self.scale)
        writer.write_object(self.auto)
        writer.write_object(self.var_auto)
        writer.write_object(self.var_adjustment)

    def read_fields(self, reader):
        super().read_fields(reader)
        self.scale = reader.read_object()
        self.auto = reader.read_object()
        self.var_auto = reader.read_object()
        self.var_adjustment = reader.read_object()

    def describe(self):
        return f"ScreenBrightness(id={self.stmt_id})"

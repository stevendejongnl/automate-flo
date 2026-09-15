from ..base import LevelDecision

TYPE_ID = 1017


class AudioVolume(LevelDecision):
    """id 1017, UI name "Audio volume". Extends LevelDecision extends IntermittentDecision extends Decision -- onPositive/onNegative/continuity/minLevel/maxLevel/varLevel. Single extra field: stream (generic expression), written after varLevel."""
    type_id = TYPE_ID

    def __init__(self, stmt_id, cell_x=0, cell_y=0, on_positive=None, on_negative=None, continuity=None, min_level=None, max_level=None, var_level=None, stream=None):
        super().__init__(stmt_id, cell_x, cell_y, on_complete=None)
        self.on_positive = on_positive
        self.on_negative = on_negative
        self.continuity = continuity
        self.min_level = min_level
        self.max_level = max_level
        self.var_level = var_level
        self.stream = stream

    def write_fields(self, writer):
        super().write_fields(writer)
        writer.write_object(self.stream)

    def read_fields(self, reader):
        super().read_fields(reader)
        self.stream = reader.read_object()

    def describe(self):
        return f"AudioVolume(id={self.stmt_id})"

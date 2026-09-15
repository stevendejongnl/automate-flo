from ..base import IntermittentDecision

TYPE_ID = 1317


class AudioStreamMuted(IntermittentDecision):
    """id 1317, UI name "Audio stream muted?". Extends IntermittentDecision extends Decision -- onPositive/onNegative/continuity. Single field: stream (generic expression)."""
    type_id = TYPE_ID

    def __init__(self, stmt_id, cell_x=0, cell_y=0, on_positive=None, on_negative=None, continuity=None, stream=None):
        super().__init__(stmt_id, cell_x, cell_y, on_complete=None)
        self.on_positive = on_positive
        self.on_negative = on_negative
        self.continuity = continuity
        self.stream = stream

    def write_fields(self, writer):
        super().write_fields(writer)
        writer.write_object(self.stream)

    def read_fields(self, reader):
        super().read_fields(reader)
        self.stream = reader.read_object()

    def describe(self):
        return f"AudioStreamMuted(id={self.stmt_id})"

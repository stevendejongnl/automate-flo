from ..base import IntermittentDecision

TYPE_ID = 1047


class DeviceDocked(IntermittentDecision):
    """id 1047, UI name "Device docked?". Extends IntermittentDecision
    directly -- onPositive/onNegative/continuity, plus one field of its
    own: modes (a dock-mode bitmask, wrap_double)."""
    type_id = TYPE_ID

    def __init__(self, stmt_id, cell_x=0, cell_y=0, on_positive=None,
                 on_negative=None, continuity=None, modes=None):
        super().__init__(stmt_id, cell_x, cell_y, on_complete=None)
        self.on_positive = on_positive
        self.on_negative = on_negative
        self.continuity = continuity
        self.modes = modes

    def write_fields(self, writer):
        super().write_fields(writer)
        writer.write_object(writer.wrap_double(self.modes))

    def read_fields(self, reader):
        super().read_fields(reader)
        self.modes = reader.read_object()

    def describe(self):
        return f"DeviceDocked(id={self.stmt_id})"

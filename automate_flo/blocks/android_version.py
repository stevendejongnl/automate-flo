from ..base import Decision

TYPE_ID = 1244


class AndroidVersion(Decision):
    """id 1244, UI name "Android version". Extends Decision DIRECTLY (not
    IntermittentDecision, not LevelDecision) -- onPositive/onNegative, then
    its own minLevel/maxLevel/varLevel fields, but NO continuity field.
    Confirmed by source (class declaration is `extends Decision`, not
    `extends LevelDecision` despite having the same-named min/max/var level
    fields as LevelDecision) -- same "Decision used directly, no
    continuity" family as ExpressionDecision/AccountPick/ActivityStartResult
    (see automate_flo/blocks/expression_decision.py)."""
    type_id = TYPE_ID

    def __init__(self, stmt_id, cell_x=0, cell_y=0, on_positive=None,
                 on_negative=None, min_level=None, max_level=None,
                 var_level=None):
        super().__init__(stmt_id, cell_x, cell_y, on_complete=None)
        self.on_positive = on_positive
        self.on_negative = on_negative
        self.min_level = min_level
        self.max_level = max_level
        self.var_level = var_level

    def write_fields(self, writer):
        super().write_fields(writer)
        writer.write_object(self.min_level)
        writer.write_object(self.max_level)
        writer.write_object(self.var_level)

    def read_fields(self, reader):
        super().read_fields(reader)
        self.min_level = reader.read_object()
        self.max_level = reader.read_object()
        self.var_level = reader.read_object()

    def describe(self):
        return f"AndroidVersion(id={self.stmt_id})"

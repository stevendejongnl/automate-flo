from ..base import Decision

TYPE_ID = 1058


class ExpressionDecision(Decision):
    """id 1058, UI name "Expression". Extends Decision DIRECTLY (not
    IntermittentDecision like the rest of this library's Decision-family
    blocks) -- onPositive/onNegative, plus one generic 'expression' field,
    but NO continuity field. Confirmed by source (class declaration is
    `extends Decision`) and empirically: writing a continuity object here
    (matching the other Decision blocks' shape) misaligned every field
    after it and Automate rejected the file outright."""
    type_id = TYPE_ID

    def __init__(self, stmt_id, expression, cell_x=0, cell_y=0,
                 on_positive=None, on_negative=None):
        super().__init__(stmt_id, cell_x, cell_y, on_complete=None)
        self.on_positive = on_positive
        self.on_negative = on_negative
        self.expression = expression

    def write_fields(self, writer):
        super().write_fields(writer)
        writer.write_object(self.expression)

    def read_fields(self, reader):
        super().read_fields(reader)
        self.expression = reader.read_object()

    def describe(self):
        return f"ExpressionDecision(id={self.stmt_id})"

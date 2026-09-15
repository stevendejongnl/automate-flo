from ..base import Decision

TYPE_ID = 1242


class AppNotificationsEnabled(Decision):
    """id 1242, UI name "App notifications enabled?". Extends Decision DIRECTLY (not IntermittentDecision) -- onPositive/onNegative only, no continuity, plus one packageName string-expression field. Same "Decision used directly" family as AndroidVersion/ExpressionDecision/AccountPick/ActivityStartResult."""

    type_id = TYPE_ID

    def __init__(self, stmt_id, cell_x=0, cell_y=0, on_positive=None, on_negative=None, package_name=None):
        super().__init__(stmt_id, cell_x, cell_y, on_complete=None)
        self.on_positive = on_positive
        self.on_negative = on_negative
        self.package_name = package_name

    def write_fields(self, writer):
        super().write_fields(writer)
        writer.write_object(writer.wrap_str(self.package_name))

    def read_fields(self, reader):
        super().read_fields(reader)
        self.package_name = reader.read_object()

    def describe(self):
        return f"AppNotificationsEnabled(id={self.stmt_id})"

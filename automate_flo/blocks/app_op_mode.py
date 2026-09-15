from ..base import Decision

TYPE_ID = 1250


class AppOpMode(Decision):
    """id 1250, UI name "App op mode". Extends Decision DIRECTLY (not IntermittentDecision) -- onPositive/onNegative only, no continuity. Fields: packageName (string expression, wrap_str), opstr (string expression, wrap_str -- the app-op name like "android:fine_location"), mode (numeric expression, wrap_double), varCurrentMode (variable-reference, raw pass-through, no wrapping). Same "Decision used directly" family as AndroidVersion/AppNotificationsEnabled/ExpressionDecision/AccountPick/ActivityStartResult."""

    type_id = TYPE_ID

    def __init__(self, stmt_id, cell_x=0, cell_y=0, on_positive=None, on_negative=None, package_name=None, opstr=None, mode=None, var_current_mode=None):
        super().__init__(stmt_id, cell_x, cell_y, on_complete=None)
        self.on_positive = on_positive
        self.on_negative = on_negative
        self.package_name = package_name
        self.opstr = opstr
        self.mode = mode
        self.var_current_mode = var_current_mode

    def write_fields(self, writer):
        super().write_fields(writer)
        writer.write_object(writer.wrap_str(self.package_name))
        writer.write_object(writer.wrap_str(self.opstr))
        writer.write_object(writer.wrap_double(self.mode))
        writer.write_object(self.var_current_mode)

    def read_fields(self, reader):
        super().read_fields(reader)
        self.package_name = reader.read_object()
        self.opstr = reader.read_object()
        self.mode = reader.read_object()
        self.var_current_mode = reader.read_object()

    def describe(self):
        return f"AppOpMode(id={self.stmt_id})"

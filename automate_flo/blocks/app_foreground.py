from ..base import IntermittentDecision

TYPE_ID = 1006


class AppForeground(IntermittentDecision):
    """id 1006, UI name "App foreground". Extends IntermittentDecision
    directly -- onPositive/onNegative/continuity, plus packageName,
    className (nullable string expressions), varForegroundPackageName,
    varForegroundClassName (nullable VariableExpr, raw pass-through, no
    wrapping)."""
    type_id = TYPE_ID

    def __init__(self, stmt_id, cell_x=0, cell_y=0, on_positive=None,
                 on_negative=None, continuity=None, package_name=None,
                 class_name=None, var_foreground_package_name=None,
                 var_foreground_class_name=None):
        super().__init__(stmt_id, cell_x, cell_y, on_complete=None)
        self.on_positive = on_positive
        self.on_negative = on_negative
        self.continuity = continuity
        self.package_name = package_name
        self.class_name = class_name
        self.var_foreground_package_name = var_foreground_package_name
        self.var_foreground_class_name = var_foreground_class_name

    def write_fields(self, writer):
        super().write_fields(writer)
        writer.write_object(writer.wrap_str(self.package_name))
        writer.write_object(writer.wrap_str(self.class_name))
        writer.write_object(self.var_foreground_package_name)
        writer.write_object(self.var_foreground_class_name)

    def read_fields(self, reader):
        super().read_fields(reader)
        self.package_name = reader.read_object()
        self.class_name = reader.read_object()
        self.var_foreground_package_name = reader.read_object()
        self.var_foreground_class_name = reader.read_object()

    def describe(self):
        return f"AppForeground(id={self.stmt_id})"

from ..base import Action, StringExpr

TYPE_ID = 1235


class AppClearCache(Action):
    """id 1235, UI name "Clear app cache". Extends PackageAction extends Action -- one packageName field."""
    type_id = TYPE_ID

    def __init__(self, stmt_id, package_name, cell_x=0, cell_y=0, on_complete=None):
        super().__init__(stmt_id, cell_x, cell_y, on_complete)
        self.package_name = package_name

    def write_fields(self, writer):
        super().write_fields(writer)
        writer.write_object(StringExpr(self.package_name))

    def read_fields(self, reader):
        super().read_fields(reader)
        pkg = reader.read_object()
        self.package_name = pkg.value if pkg is not None else None

    def describe(self):
        return f"AppClearCache(id={self.stmt_id}, package={self.package_name!r})"

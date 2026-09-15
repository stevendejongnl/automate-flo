from ..base import Action

TYPE_ID = 1251


class AppOpModeSet(Action):
    """id 1251, UI name "Set app op mode". Extends PackageAction extends Action -- packageName, then opstr, mode."""
    type_id = TYPE_ID

    def __init__(self, stmt_id, package_name, opstr, mode, cell_x=0, cell_y=0, on_complete=None):
        super().__init__(stmt_id, cell_x, cell_y, on_complete)
        self.package_name = package_name
        self.opstr = opstr
        self.mode = mode

    def write_fields(self, writer):
        super().write_fields(writer)
        writer.write_object(writer.wrap_str(self.package_name))
        writer.write_object(writer.wrap_str(self.opstr))
        writer.write_object(writer.wrap_double(self.mode))

    def read_fields(self, reader):
        super().read_fields(reader)
        self.package_name = reader.read_object()
        self.opstr = reader.read_object()
        self.mode = reader.read_object()

    def describe(self):
        return f"AppOpModeSet(id={self.stmt_id})"

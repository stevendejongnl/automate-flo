from ..base import Action

TYPE_ID = 1063


class FileCopy(Action):
    """id 1063, UI name "File copy". Extends Action directly. Own
    fields in wire order: sourcePath (final level may be a glob),
    destinationPath, recursive, update. Single observation (deleted from
    the source flow before its second export); the recursive-then-update
    order matches ZipCompress's, which was observed live."""

    type_id = TYPE_ID

    def __init__(self, stmt_id, cell_x=0, cell_y=0, on_complete=None,
                 source_path=None, destination_path=None, recursive=None,
                 update=None):
        super().__init__(stmt_id, cell_x, cell_y, on_complete)
        self.source_path = source_path
        self.destination_path = destination_path
        self.recursive = recursive
        self.update = update

    def write_fields(self, writer):
        super().write_fields(writer)
        writer.write_object(writer.wrap_str(self.source_path))
        writer.write_object(writer.wrap_str(self.destination_path))
        writer.write_object(writer.wrap_double(self.recursive))
        writer.write_object(writer.wrap_double(self.update))

    def read_fields(self, reader):
        super().read_fields(reader)
        self.source_path = reader.read_object()
        self.destination_path = reader.read_object()
        self.recursive = reader.read_object()
        self.update = reader.read_object()

    def describe(self):
        return f"FileCopy(id={self.stmt_id})"

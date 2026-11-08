from ..base import Action

TYPE_ID = 1064


class FileList(Action):
    """id 1064, UI name "File list". Extends Action directly. Own fields
    in wire order: path (the final directory level may be a glob),
    contentType, modifiedSince, recursive, varFilenames.

    ContentType is a picker value carried by the raw-double expression
    type (id 101): 2.0 = "Directories" was observed, and "All content"
    (the default) serializes as null -- a v114/v115 pair of the same
    flow shows exactly this change. Slot mapping confirmed by that
    natural experiment; see format.py's docstring."""

    type_id = TYPE_ID

    def __init__(self, stmt_id, cell_x=0, cell_y=0, on_complete=None,
                 path=None, content_type=None, modified_since=None,
                 recursive=None, var_filenames=None):
        super().__init__(stmt_id, cell_x, cell_y, on_complete)
        self.path = path
        self.content_type = content_type
        self.modified_since = modified_since
        self.recursive = recursive
        self.var_filenames = var_filenames

    def write_fields(self, writer):
        super().write_fields(writer)
        writer.write_object(writer.wrap_str(self.path))
        writer.write_object(self.content_type)
        writer.write_object(writer.wrap_double(self.modified_since))
        writer.write_object(writer.wrap_double(self.recursive))
        writer.write_object(self.var_filenames)

    def read_fields(self, reader):
        super().read_fields(reader)
        self.path = reader.read_object()
        self.content_type = reader.read_object()
        self.modified_since = reader.read_object()
        self.recursive = reader.read_object()
        self.var_filenames = reader.read_object()

    def describe(self):
        return f"FileList(id={self.stmt_id})"

from ..base import Action

TYPE_ID = 1151


class ZipCompress(Action):
    """id 1151, UI name "Zip compress". Extends Action directly. Own
    fields in wire order: destinationZipFile (a new or an existing
    archive), sourcePath (final level may be a glob),
    destinationFolderInZip (null = archive root), recursive, update,
    compressionMethod.

    Update is the load-bearing option when compressing one file per
    call in a loop: with it off, every call recreates the archive and
    only the last entry survives. CompressionMethod is a picker value
    carried by the raw-double expression type (id 101); 0.0 was
    observed, which per the app's docs is the default "Deflated
    normal". Single observation (present in only one of the two source
    exports); slot order recursive-then-update corroborates
    FileCopy's."""

    type_id = TYPE_ID

    def __init__(self, stmt_id, cell_x=0, cell_y=0, on_complete=None,
                 destination_zip_file=None, source_path=None,
                 destination_folder_in_zip=None, recursive=None,
                 update=None, compression_method=None):
        super().__init__(stmt_id, cell_x, cell_y, on_complete)
        self.destination_zip_file = destination_zip_file
        self.source_path = source_path
        self.destination_folder_in_zip = destination_folder_in_zip
        self.recursive = recursive
        self.update = update
        self.compression_method = compression_method

    def write_fields(self, writer):
        super().write_fields(writer)
        writer.write_object(writer.wrap_str(self.destination_zip_file))
        writer.write_object(writer.wrap_str(self.source_path))
        writer.write_object(self.destination_folder_in_zip)
        writer.write_object(writer.wrap_double(self.recursive))
        writer.write_object(writer.wrap_double(self.update))
        writer.write_object(self.compression_method)

    def read_fields(self, reader):
        super().read_fields(reader)
        self.destination_zip_file = reader.read_object()
        self.source_path = reader.read_object()
        self.destination_folder_in_zip = reader.read_object()
        self.recursive = reader.read_object()
        self.update = reader.read_object()
        self.compression_method = reader.read_object()

    def describe(self):
        return f"ZipCompress(id={self.stmt_id})"

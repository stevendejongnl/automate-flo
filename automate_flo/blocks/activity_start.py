from ..base import Action, StringExpr

TYPE_ID = 1001


class ActivityStart(Action):
    """id 1001, UI name "App start" -- confirmed by search + opening the
    real edit screen: field order on screen was exactly Package, Activity
    class, Action, Data URI, MIME type, Category, Extras, Flags, matching
    IntentAction.r()/t() byte-for-byte. Extends IntentAction extends
    Action."""
    type_id = TYPE_ID

    def __init__(self, stmt_id, package_name, cell_x=0, cell_y=0, on_complete=None,
                 class_name=None, action=None, uri=None, mime_type=None,
                 categories=None, extras=None, flags=None,
                 activity_options=None, chooser=None):
        super().__init__(stmt_id, cell_x, cell_y, on_complete)
        self.package_name = package_name
        self.class_name = class_name
        self.action = action
        self.uri = uri
        self.mime_type = mime_type
        self.categories = categories
        self.extras = extras
        self.flags = flags
        self.activity_options = activity_options
        self.chooser = chooser

    def write_fields(self, writer):
        super().write_fields(writer)
        writer.write_object(StringExpr(self.package_name))
        writer.write_object(self.class_name)
        writer.write_object(self.action)
        writer.write_object(self.uri)
        writer.write_object(self.mime_type)
        writer.write_object(self.categories)
        writer.write_object(self.extras)
        writer.write_object(self.flags)             # version 114 >= 45
        writer.write_object(self.activity_options)  # version 114 >= 89
        writer.write_object(self.chooser)            # version 114 >= 38

    def read_fields(self, reader):
        super().read_fields(reader)
        pkg = reader.read_object()
        self.package_name = pkg.value if pkg is not None else None
        self.class_name = reader.read_object()
        self.action = reader.read_object()
        self.uri = reader.read_object()
        self.mime_type = reader.read_object()
        self.categories = reader.read_object()
        self.extras = reader.read_object()
        self.flags = reader.read_object()
        self.activity_options = reader.read_object()
        self.chooser = reader.read_object()

    def describe(self):
        return f"ActivityStart(id={self.stmt_id}, package={self.package_name!r})"

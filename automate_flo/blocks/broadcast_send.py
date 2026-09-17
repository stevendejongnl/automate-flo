from ..base import Action


TYPE_ID = 1023


class BroadcastSend(Action):
    """id 1023, UI name "Broadcast". Extends Action directly, mirroring the
    IntentAction field layout inline (same 8-field shape as ActivityStart:
    package_name, class_name, action, uri, mime_type, categories, extras,
    flags) -- onComplete only, no continuity. Unlike ActivityStart, no field
    is required: the real source has no null-check, it just builds whatever
    Intent it can from whichever fields are set. package_name/class_name/
    action/uri/mime_type are wrap_str; flags is wrap_double; categories
    (array-of-strings) and extras (bundle) are raw pass-through, no wrapper
    exists for those types."""
    type_id = TYPE_ID

    def __init__(self, stmt_id, cell_x=0, cell_y=0, on_complete=None,
                 package_name=None, class_name=None, action=None, uri=None,
                 mime_type=None, categories=None, extras=None, flags=None):
        super().__init__(stmt_id, cell_x, cell_y, on_complete)
        self.package_name = package_name
        self.class_name = class_name
        self.action = action
        self.uri = uri
        self.mime_type = mime_type
        self.categories = categories
        self.extras = extras
        self.flags = flags

    def write_fields(self, writer):
        super().write_fields(writer)
        writer.write_object(writer.wrap_str(self.package_name))
        writer.write_object(writer.wrap_str(self.class_name))
        writer.write_object(writer.wrap_str(self.action))
        writer.write_object(writer.wrap_str(self.uri))
        writer.write_object(writer.wrap_str(self.mime_type))
        writer.write_object(self.categories)
        writer.write_object(self.extras)
        writer.write_object(writer.wrap_double(self.flags))

    def read_fields(self, reader):
        super().read_fields(reader)
        self.package_name = reader.read_object()
        self.class_name = reader.read_object()
        self.action = reader.read_object()
        self.uri = reader.read_object()
        self.mime_type = reader.read_object()
        self.categories = reader.read_object()
        self.extras = reader.read_object()
        self.flags = reader.read_object()

    def describe(self):
        return f"BroadcastSend(id={self.stmt_id})"

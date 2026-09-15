from ..base import IntermittentDecision

TYPE_ID = 1103


class NotificationShow(IntermittentDecision):
    """id 1103, UI name "Show notification". Extends IntermittentDecision
    extends Decision -- onPositive fires on tap, onNegative on dismiss/
    timeout (mirrors the real block's two exec outputs). Source has many
    `if version >= N` gates for older-format migration; all resolve to
    "always write" at version 114, so the field list below is exhaustive
    for files this library produces."""
    type_id = TYPE_ID

    def __init__(self, stmt_id, title, message, cell_x=0, cell_y=0,
                 on_positive=None, on_negative=None, continuity=None,
                 short_critical_text=None, picture_uri=None, person_uri=None,
                 small_icon_uri=None, large_icon_uri=None, primary_layout_xml=None,
                 big_layout_xml=None, heads_up_layout_xml=None, color=None,
                 cancellable=None, ongoing=None, visibility=None, category=None,
                 group_key=None, channel_id=None, progress=None, when=None,
                 var_key=None, var_interface_uri=None):
        super().__init__(stmt_id, cell_x, cell_y, on_complete=None)
        self.on_positive = on_positive
        self.on_negative = on_negative
        self.continuity = continuity
        self.title = title
        self.message = message
        self.short_critical_text = short_critical_text
        self.picture_uri = picture_uri
        self.person_uri = person_uri
        self.small_icon_uri = small_icon_uri
        self.large_icon_uri = large_icon_uri
        self.primary_layout_xml = primary_layout_xml
        self.big_layout_xml = big_layout_xml
        self.heads_up_layout_xml = heads_up_layout_xml
        self.color = color
        self.cancellable = cancellable
        self.ongoing = ongoing
        self.visibility = visibility
        self.category = category
        self.group_key = group_key
        self.channel_id = channel_id
        self.progress = progress
        self.when = when
        self.var_key = var_key
        self.var_interface_uri = var_interface_uri

    def write_fields(self, writer):
        super().write_fields(writer)
        writer.write_object(writer.wrap_str(self.title))
        writer.write_object(writer.wrap_str(self.message))
        writer.write_object(self.short_critical_text)
        writer.write_object(self.picture_uri)
        writer.write_object(self.person_uri)
        writer.write_object(self.small_icon_uri)
        writer.write_object(self.large_icon_uri)
        writer.write_object(self.primary_layout_xml)
        writer.write_object(self.big_layout_xml)
        writer.write_object(self.heads_up_layout_xml)
        writer.write_object(self.color)
        writer.write_object(self.cancellable)
        writer.write_object(self.ongoing)
        writer.write_object(self.visibility)
        writer.write_object(self.category)
        writer.write_object(self.group_key)
        writer.write_object(self.channel_id)
        writer.write_object(self.progress)
        writer.write_object(self.when)
        writer.write_object(self.var_key)
        writer.write_object(self.var_interface_uri)

    def read_fields(self, reader):
        super().read_fields(reader)
        self.title = reader.read_object()
        self.message = reader.read_object()
        self.short_critical_text = reader.read_object()
        self.picture_uri = reader.read_object()
        self.person_uri = reader.read_object()
        self.small_icon_uri = reader.read_object()
        self.large_icon_uri = reader.read_object()
        self.primary_layout_xml = reader.read_object()
        self.big_layout_xml = reader.read_object()
        self.heads_up_layout_xml = reader.read_object()
        self.color = reader.read_object()
        self.cancellable = reader.read_object()
        self.ongoing = reader.read_object()
        self.visibility = reader.read_object()
        self.category = reader.read_object()
        self.group_key = reader.read_object()
        self.channel_id = reader.read_object()
        self.progress = reader.read_object()
        self.when = reader.read_object()
        self.var_key = reader.read_object()
        self.var_interface_uri = reader.read_object()

    def describe(self):
        return f"NotificationShow(id={self.stmt_id})"

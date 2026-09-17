from ..base import Decision

TYPE_ID = 1031


class CaptureImage(Decision):
    """id 1031, UI name "Capture image". Extends ActivityDecision extends
    Decision directly (onPositive/onNegative, no continuity). Flattens
    ActivityDecision's timeout/start_activity/notification_channel_id
    (raw pass-through) inline, then adds its own package_name/target_path
    (wrap_str) and var_image_file (VariableExpr, raw pass-through)."""
    type_id = TYPE_ID

    def __init__(self, stmt_id, cell_x=0, cell_y=0, on_positive=None, on_negative=None,
                 timeout=None, start_activity=None, notification_channel_id=None,
                 package_name=None, target_path=None, var_image_file=None):
        super().__init__(stmt_id, cell_x, cell_y, on_complete=None)
        self.on_positive = on_positive
        self.on_negative = on_negative
        self.timeout = timeout
        self.start_activity = start_activity
        self.notification_channel_id = notification_channel_id
        self.package_name = package_name
        self.target_path = target_path
        self.var_image_file = var_image_file

    def write_fields(self, writer):
        super().write_fields(writer)
        writer.write_object(self.timeout)
        writer.write_object(self.start_activity)
        writer.write_object(self.notification_channel_id)
        writer.write_object(writer.wrap_str(self.package_name))
        writer.write_object(writer.wrap_str(self.target_path))
        writer.write_object(self.var_image_file)

    def read_fields(self, reader):
        super().read_fields(reader)
        self.timeout = reader.read_object()
        self.start_activity = reader.read_object()
        self.notification_channel_id = reader.read_object()
        self.package_name = reader.read_object()
        self.target_path = reader.read_object()
        self.var_image_file = reader.read_object()

    def describe(self):
        return f"CaptureImage(id={self.stmt_id})"

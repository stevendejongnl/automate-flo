from ..base import Decision

TYPE_ID = 1154


class BluetoothDevicePick(Decision):
    """id 1154, UI name "Pick Bluetooth device". Extends ActivityDecision extends Decision -- onPositive/onNegative, not onComplete. ActivityDecision's own fields (timeout, startActivity, notificationChannelId) duplicated inline per this library's convention (see ActivityStartResult), followed by this block's own fields. deviceClass (version>=39) and pairedOnly (version>=108) are version-gated in the app but this library always writes version 114, so both are always present."""
    type_id = TYPE_ID

    def __init__(self, stmt_id, cell_x=0, cell_y=0, on_positive=None, on_negative=None, timeout=None, start_activity=None, notification_channel_id=None, device_class=None, paired_only=None, var_device_name=None, var_device_address=None, var_device_class=None):
        super().__init__(stmt_id, cell_x, cell_y, on_complete=None)
        self.on_positive = on_positive
        self.on_negative = on_negative
        self.timeout = timeout
        self.start_activity = start_activity
        self.notification_channel_id = notification_channel_id
        self.device_class = device_class
        self.paired_only = paired_only
        self.var_device_name = var_device_name
        self.var_device_address = var_device_address
        self.var_device_class = var_device_class

    def write_fields(self, writer):
        super().write_fields(writer)
        writer.write_object(self.timeout)
        writer.write_object(self.start_activity)
        writer.write_object(self.notification_channel_id)
        writer.write_object(self.device_class)
        writer.write_object(self.paired_only)
        writer.write_object(self.var_device_name)
        writer.write_object(self.var_device_address)
        writer.write_object(self.var_device_class)

    def read_fields(self, reader):
        super().read_fields(reader)
        self.timeout = reader.read_object()
        self.start_activity = reader.read_object()
        self.notification_channel_id = reader.read_object()
        self.device_class = reader.read_object()
        self.paired_only = reader.read_object()
        self.var_device_name = reader.read_object()
        self.var_device_address = reader.read_object()
        self.var_device_class = reader.read_object()

    def describe(self):
        return f"BluetoothDevicePick(id={self.stmt_id})"

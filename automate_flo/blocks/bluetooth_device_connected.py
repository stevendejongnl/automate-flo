from ..base import IntermittentDecision

TYPE_ID = 1153


class BluetoothDeviceConnected(IntermittentDecision):
    """id 1153, UI name "Bluetooth device connected?". Extends
    IntermittentDecision extends Decision -- onPositive/onNegative.
    Leaving deviceAddress/deviceName both null matches "any device" in the
    UI -- no device-picker interaction needed to build a valid flow."""
    type_id = TYPE_ID

    def __init__(self, stmt_id, cell_x=0, cell_y=0, on_positive=None,
                 on_negative=None, continuity=None, device_address=None,
                 device_name=None, device_class=None, paired_only=None,
                 var_connected_device_address=None, var_connected_device_name=None,
                 var_connected_device_class=None):
        super().__init__(stmt_id, cell_x, cell_y, on_complete=None)
        self.on_positive = on_positive
        self.on_negative = on_negative
        self.continuity = continuity
        self.device_address = device_address
        self.device_name = device_name
        self.device_class = device_class
        self.paired_only = paired_only
        self.var_connected_device_address = var_connected_device_address
        self.var_connected_device_name = var_connected_device_name
        self.var_connected_device_class = var_connected_device_class

    def write_fields(self, writer):
        super().write_fields(writer)
        writer.write_object(writer.wrap_str(self.device_address))
        writer.write_object(writer.wrap_str(self.device_name))
        writer.write_object(self.device_class)
        writer.write_object(self.paired_only)
        writer.write_object(self.var_connected_device_address)
        writer.write_object(self.var_connected_device_name)
        writer.write_object(self.var_connected_device_class)

    def read_fields(self, reader):
        super().read_fields(reader)
        self.device_address = reader.read_object()
        self.device_name = reader.read_object()
        self.device_class = reader.read_object()
        self.paired_only = reader.read_object()
        self.var_connected_device_address = reader.read_object()
        self.var_connected_device_name = reader.read_object()
        self.var_connected_device_class = reader.read_object()

    def describe(self):
        return f"BluetoothDeviceConnected(id={self.stmt_id})"

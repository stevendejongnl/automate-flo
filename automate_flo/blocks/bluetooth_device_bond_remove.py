from ..base import Decision

TYPE_ID = 1393


class BluetoothDeviceBondRemove(Decision):
    """id 1393, UI name "Remove Bluetooth device bond". Extends Decision directly (no continuity field). Fields, in order: device_address, device_name (both wrap_str, like BluetoothDeviceConnected)."""
    type_id = TYPE_ID

    def __init__(self, stmt_id, cell_x=0, cell_y=0, on_positive=None, on_negative=None, device_address=None, device_name=None):
        super().__init__(stmt_id, cell_x, cell_y, on_complete=None)
        self.on_positive = on_positive
        self.on_negative = on_negative
        self.device_address = device_address
        self.device_name = device_name

    def write_fields(self, writer):
        super().write_fields(writer)
        writer.write_object(writer.wrap_str(self.device_address))
        writer.write_object(writer.wrap_str(self.device_name))

    def read_fields(self, reader):
        super().read_fields(reader)
        self.device_address = reader.read_object()
        self.device_name = reader.read_object()

    def describe(self):
        return f"BluetoothDeviceBondRemove(id={self.stmt_id})"

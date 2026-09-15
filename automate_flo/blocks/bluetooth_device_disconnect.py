from ..base import Action

TYPE_ID = 1270


class BluetoothDeviceDisconnect(Action):
    """id 1270, UI name "Disconnect Bluetooth device". Extends Action directly. Fields, in order: profile (generic expression), device_address, device_name (both wrap_str, like BluetoothDeviceConnected)."""
    type_id = TYPE_ID

    def __init__(self, stmt_id, cell_x=0, cell_y=0, on_complete=None, profile=None, device_address=None, device_name=None):
        super().__init__(stmt_id, cell_x, cell_y, on_complete)
        self.profile = profile
        self.device_address = device_address
        self.device_name = device_name

    def write_fields(self, writer):
        super().write_fields(writer)
        writer.write_object(self.profile)
        writer.write_object(writer.wrap_str(self.device_address))
        writer.write_object(writer.wrap_str(self.device_name))

    def read_fields(self, reader):
        super().read_fields(reader)
        self.profile = reader.read_object()
        self.device_address = reader.read_object()
        self.device_name = reader.read_object()

    def describe(self):
        return f"BluetoothDeviceDisconnect(id={self.stmt_id})"

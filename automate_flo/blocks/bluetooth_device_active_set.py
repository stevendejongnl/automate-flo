from ..base import Decision

TYPE_ID = 1383


class BluetoothDeviceActiveSet(Decision):
    """id 1383, UI name "Set active Bluetooth device". Extends Decision directly (no continuity field, like AndroidVersion/ActivityStartResult). Fields, in order: profile (generic expression), device_address, device_name (both wrapped with writer.wrap_str/reader convention like BluetoothDeviceConnected, so plain Python strings can be passed directly)."""
    type_id = TYPE_ID

    def __init__(self, stmt_id, cell_x=0, cell_y=0, on_positive=None, on_negative=None, profile=None, device_address=None, device_name=None):
        super().__init__(stmt_id, cell_x, cell_y, on_complete=None)
        self.on_positive = on_positive
        self.on_negative = on_negative
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
        return f"BluetoothDeviceActiveSet(id={self.stmt_id})"

from ..base import Action

TYPE_ID = 1277


class BluetoothDeviceScan(Action):
    """id 1277, UI name "Scan Bluetooth devices". Extends Action directly. connectableOnly (version>=97), varDeviceAdvertisements (version>=54), varDeviceRssis (version>=52) are version-gated in the app but this library always writes version 114, so all are always present. Fields, in order: mode, device_class, connectable_only, paired_only (generic expressions), var_device_names, var_device_addresses, var_device_advertisements, var_device_rssis (VariableExpr output vars)."""
    type_id = TYPE_ID

    def __init__(self, stmt_id, cell_x=0, cell_y=0, on_complete=None, mode=None, device_class=None, connectable_only=None, paired_only=None, var_device_names=None, var_device_addresses=None, var_device_advertisements=None, var_device_rssis=None):
        super().__init__(stmt_id, cell_x, cell_y, on_complete)
        self.mode = mode
        self.device_class = device_class
        self.connectable_only = connectable_only
        self.paired_only = paired_only
        self.var_device_names = var_device_names
        self.var_device_addresses = var_device_addresses
        self.var_device_advertisements = var_device_advertisements
        self.var_device_rssis = var_device_rssis

    def write_fields(self, writer):
        super().write_fields(writer)
        writer.write_object(self.mode)
        writer.write_object(self.device_class)
        writer.write_object(self.connectable_only)
        writer.write_object(self.paired_only)
        writer.write_object(self.var_device_names)
        writer.write_object(self.var_device_addresses)
        writer.write_object(self.var_device_advertisements)
        writer.write_object(self.var_device_rssis)

    def read_fields(self, reader):
        super().read_fields(reader)
        self.mode = reader.read_object()
        self.device_class = reader.read_object()
        self.connectable_only = reader.read_object()
        self.paired_only = reader.read_object()
        self.var_device_names = reader.read_object()
        self.var_device_addresses = reader.read_object()
        self.var_device_advertisements = reader.read_object()
        self.var_device_rssis = reader.read_object()

    def describe(self):
        return f"BluetoothDeviceScan(id={self.stmt_id})"

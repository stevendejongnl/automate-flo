from ..base import IntermittentDecision

TYPE_ID = 1329


class AudioDeviceConnected(IntermittentDecision):
    """id 1329, UI name "Audio device connected?". Extends IntermittentDecision extends Decision -- onPositive/onNegative/continuity. All fields below are version-gated in the app (some require version>=110) but this library always writes version 114, so every gate is always satisfied and every field is always present."""
    type_id = TYPE_ID

    def __init__(self, stmt_id, cell_x=0, cell_y=0, on_positive=None, on_negative=None, continuity=None, device_type=None, device_mode=None, device_brand=None, device_address=None, var_connected_device_type=None, var_connected_device_mode=None, var_connected_device_brand=None, var_connected_device_address=None, var_connected_device_id=None):
        super().__init__(stmt_id, cell_x, cell_y, on_complete=None)
        self.on_positive = on_positive
        self.on_negative = on_negative
        self.continuity = continuity
        self.device_type = device_type
        self.device_mode = device_mode
        self.device_brand = device_brand
        self.device_address = device_address
        self.var_connected_device_type = var_connected_device_type
        self.var_connected_device_mode = var_connected_device_mode
        self.var_connected_device_brand = var_connected_device_brand
        self.var_connected_device_address = var_connected_device_address
        self.var_connected_device_id = var_connected_device_id

    def write_fields(self, writer):
        super().write_fields(writer)
        writer.write_object(self.device_type)
        writer.write_object(self.device_mode)
        writer.write_object(self.device_brand)
        writer.write_object(self.device_address)
        writer.write_object(self.var_connected_device_type)
        writer.write_object(self.var_connected_device_mode)
        writer.write_object(self.var_connected_device_brand)
        writer.write_object(self.var_connected_device_address)
        writer.write_object(self.var_connected_device_id)

    def read_fields(self, reader):
        super().read_fields(reader)
        self.device_type = reader.read_object()
        self.device_mode = reader.read_object()
        self.device_brand = reader.read_object()
        self.device_address = reader.read_object()
        self.var_connected_device_type = reader.read_object()
        self.var_connected_device_mode = reader.read_object()
        self.var_connected_device_brand = reader.read_object()
        self.var_connected_device_address = reader.read_object()
        self.var_connected_device_id = reader.read_object()

    def describe(self):
        return f"AudioDeviceConnected(id={self.stmt_id})"

from ..base import IntermittentDecision

TYPE_ID = 1372


class BluetoothGattRead(IntermittentDecision):
    """id 1372, UI name "Read Bluetooth GATT characteristic". Extends IntermittentDecision extends Decision -- onPositive/onNegative/continuity. Fields, in order: device_address, device_name (both wrap_str, like BluetoothDeviceConnected), service_uuid, service_instance_id, characteristic_uuid, characteristic_instance_id, value_format, value_offset (generic expressions), var_result (VariableExpr output var)."""
    type_id = TYPE_ID

    def __init__(self, stmt_id, cell_x=0, cell_y=0, on_positive=None, on_negative=None, continuity=None, device_address=None, device_name=None, service_uuid=None, service_instance_id=None, characteristic_uuid=None, characteristic_instance_id=None, value_format=None, value_offset=None, var_result=None):
        super().__init__(stmt_id, cell_x, cell_y, on_complete=None)
        self.on_positive = on_positive
        self.on_negative = on_negative
        self.continuity = continuity
        self.device_address = device_address
        self.device_name = device_name
        self.service_uuid = service_uuid
        self.service_instance_id = service_instance_id
        self.characteristic_uuid = characteristic_uuid
        self.characteristic_instance_id = characteristic_instance_id
        self.value_format = value_format
        self.value_offset = value_offset
        self.var_result = var_result

    def write_fields(self, writer):
        super().write_fields(writer)
        writer.write_object(writer.wrap_str(self.device_address))
        writer.write_object(writer.wrap_str(self.device_name))
        writer.write_object(self.service_uuid)
        writer.write_object(self.service_instance_id)
        writer.write_object(self.characteristic_uuid)
        writer.write_object(self.characteristic_instance_id)
        writer.write_object(self.value_format)
        writer.write_object(self.value_offset)
        writer.write_object(self.var_result)

    def read_fields(self, reader):
        super().read_fields(reader)
        self.device_address = reader.read_object()
        self.device_name = reader.read_object()
        self.service_uuid = reader.read_object()
        self.service_instance_id = reader.read_object()
        self.characteristic_uuid = reader.read_object()
        self.characteristic_instance_id = reader.read_object()
        self.value_format = reader.read_object()
        self.value_offset = reader.read_object()
        self.var_result = reader.read_object()

    def describe(self):
        return f"BluetoothGattRead(id={self.stmt_id})"

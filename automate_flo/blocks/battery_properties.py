from ..base import Action

TYPE_ID = 1370


class BatteryProperties(Action):
    """id 1370, UI name "Battery properties". Extends Action directly. 9 output-variable fields, in order: var_capacity, var_remaining_percent, var_remaining_charge, var_remaining_energy, var_usage_current_now, var_usage_current_average, var_voltage, var_temperature, var_technology (all VariableExpr)."""
    type_id = TYPE_ID

    def __init__(self, stmt_id, cell_x=0, cell_y=0, on_complete=None, var_capacity=None, var_remaining_percent=None, var_remaining_charge=None, var_remaining_energy=None, var_usage_current_now=None, var_usage_current_average=None, var_voltage=None, var_temperature=None, var_technology=None):
        super().__init__(stmt_id, cell_x, cell_y, on_complete)
        self.var_capacity = var_capacity
        self.var_remaining_percent = var_remaining_percent
        self.var_remaining_charge = var_remaining_charge
        self.var_remaining_energy = var_remaining_energy
        self.var_usage_current_now = var_usage_current_now
        self.var_usage_current_average = var_usage_current_average
        self.var_voltage = var_voltage
        self.var_temperature = var_temperature
        self.var_technology = var_technology

    def write_fields(self, writer):
        super().write_fields(writer)
        writer.write_object(self.var_capacity)
        writer.write_object(self.var_remaining_percent)
        writer.write_object(self.var_remaining_charge)
        writer.write_object(self.var_remaining_energy)
        writer.write_object(self.var_usage_current_now)
        writer.write_object(self.var_usage_current_average)
        writer.write_object(self.var_voltage)
        writer.write_object(self.var_temperature)
        writer.write_object(self.var_technology)

    def read_fields(self, reader):
        super().read_fields(reader)
        self.var_capacity = reader.read_object()
        self.var_remaining_percent = reader.read_object()
        self.var_remaining_charge = reader.read_object()
        self.var_remaining_energy = reader.read_object()
        self.var_usage_current_now = reader.read_object()
        self.var_usage_current_average = reader.read_object()
        self.var_voltage = reader.read_object()
        self.var_temperature = reader.read_object()
        self.var_technology = reader.read_object()

    def describe(self):
        return f"BatteryProperties(id={self.stmt_id})"

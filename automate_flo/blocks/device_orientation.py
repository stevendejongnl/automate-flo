from ..base import IntermittentDecision

TYPE_ID = 1049


class DeviceOrientation(IntermittentDecision):
    """id 1049, UI name "Device orientation". Extends IntermittentDecision
    directly -- onPositive/onNegative/continuity, then target_azimuth/
    target_pitch/target_roll/tolerance (all wrap_double), then 3
    VariableExpr output fields (raw pass-through): var_current_azimuth,
    var_current_pitch, var_current_roll."""
    type_id = TYPE_ID

    def __init__(self, stmt_id, cell_x=0, cell_y=0, on_positive=None, on_negative=None,
                 continuity=None, target_azimuth=None, target_pitch=None,
                 target_roll=None, tolerance=None, var_current_azimuth=None,
                 var_current_pitch=None, var_current_roll=None):
        super().__init__(stmt_id, cell_x, cell_y, on_complete=None)
        self.on_positive = on_positive
        self.on_negative = on_negative
        self.continuity = continuity
        self.target_azimuth = target_azimuth
        self.target_pitch = target_pitch
        self.target_roll = target_roll
        self.tolerance = tolerance
        self.var_current_azimuth = var_current_azimuth
        self.var_current_pitch = var_current_pitch
        self.var_current_roll = var_current_roll

    def write_fields(self, writer):
        super().write_fields(writer)
        writer.write_object(writer.wrap_double(self.target_azimuth))
        writer.write_object(writer.wrap_double(self.target_pitch))
        writer.write_object(writer.wrap_double(self.target_roll))
        writer.write_object(writer.wrap_double(self.tolerance))
        writer.write_object(self.var_current_azimuth)
        writer.write_object(self.var_current_pitch)
        writer.write_object(self.var_current_roll)

    def read_fields(self, reader):
        super().read_fields(reader)
        self.target_azimuth = reader.read_object()
        self.target_pitch = reader.read_object()
        self.target_roll = reader.read_object()
        self.tolerance = reader.read_object()
        self.var_current_azimuth = reader.read_object()
        self.var_current_pitch = reader.read_object()
        self.var_current_roll = reader.read_object()

    def describe(self):
        return f"DeviceOrientation(id={self.stmt_id})"

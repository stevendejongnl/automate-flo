from ..base import IntermittentDecision

TYPE_ID = 1349


class AudioDeviceRecording(IntermittentDecision):
    """id 1349, UI name "Audio device recording?". Extends IntermittentDecision extends Decision -- onPositive/onNegative/continuity."""
    type_id = TYPE_ID

    def __init__(self, stmt_id, cell_x=0, cell_y=0, on_positive=None, on_negative=None, continuity=None, device_type=None, device_brand=None, audio_source=None, var_recording_device_type=None, var_recording_device_brand=None, var_recorded_audio_source=None):
        super().__init__(stmt_id, cell_x, cell_y, on_complete=None)
        self.on_positive = on_positive
        self.on_negative = on_negative
        self.continuity = continuity
        self.device_type = device_type
        self.device_brand = device_brand
        self.audio_source = audio_source
        self.var_recording_device_type = var_recording_device_type
        self.var_recording_device_brand = var_recording_device_brand
        self.var_recorded_audio_source = var_recorded_audio_source

    def write_fields(self, writer):
        super().write_fields(writer)
        writer.write_object(self.device_type)
        writer.write_object(self.device_brand)
        writer.write_object(self.audio_source)
        writer.write_object(self.var_recording_device_type)
        writer.write_object(self.var_recording_device_brand)
        writer.write_object(self.var_recorded_audio_source)

    def read_fields(self, reader):
        super().read_fields(reader)
        self.device_type = reader.read_object()
        self.device_brand = reader.read_object()
        self.audio_source = reader.read_object()
        self.var_recording_device_type = reader.read_object()
        self.var_recording_device_brand = reader.read_object()
        self.var_recorded_audio_source = reader.read_object()

    def describe(self):
        return f"AudioDeviceRecording(id={self.stmt_id})"

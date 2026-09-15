from ..base import IntermittentAction

TYPE_ID = 1015


class AudioRecordStart(IntermittentAction):
    """id 1015, UI name "Start audio recording". Extends IntermittentAction extends Action -- onComplete/continuity. audioDeviceId (version>=110) and focus (version>=80) are version-gated in the app but this library always writes version 114, so both are always present. notificationChannelId has a pre-77 compatibility-wrapping branch in the app's reader that never triggers at version 114, so it is read/written as a plain generic expression here."""

    type_id = TYPE_ID

    def __init__(self, stmt_id, cell_x=0, cell_y=0, on_complete=None, continuity=None, source=None, audio_device_id=None, focus=None, encoding=None, quality=None, max_duration=None, notification_channel_id=None, target_path=None, var_audio_file=None):
        super().__init__(stmt_id, cell_x, cell_y, on_complete)
        self.continuity = continuity
        self.source = source
        self.audio_device_id = audio_device_id
        self.focus = focus
        self.encoding = encoding
        self.quality = quality
        self.max_duration = max_duration
        self.notification_channel_id = notification_channel_id
        self.target_path = target_path
        self.var_audio_file = var_audio_file

    def write_fields(self, writer):
        super().write_fields(writer)
        writer.write_object(self.source)
        writer.write_object(self.audio_device_id)
        writer.write_object(self.focus)
        writer.write_object(self.encoding)
        writer.write_object(self.quality)
        writer.write_object(self.max_duration)
        writer.write_object(self.notification_channel_id)
        writer.write_object(self.target_path)
        writer.write_object(self.var_audio_file)

    def read_fields(self, reader):
        super().read_fields(reader)
        self.source = reader.read_object()
        self.audio_device_id = reader.read_object()
        self.focus = reader.read_object()
        self.encoding = reader.read_object()
        self.quality = reader.read_object()
        self.max_duration = reader.read_object()
        self.notification_channel_id = reader.read_object()
        self.target_path = reader.read_object()
        self.var_audio_file = reader.read_object()

    def describe(self):
        return f"AudioRecordStart(id={self.stmt_id})"

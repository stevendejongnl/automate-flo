from ..base import Action

TYPE_ID = 1115


class DeviceKeepAwake(Action):
    """id 1115, UI name "Keep device awake". Extends Action."""
    type_id = TYPE_ID

    def __init__(self, stmt_id, wake_state=None, cell_x=0, cell_y=0,
                 on_complete=None, wifi_state=None, wakeup=None):
        super().__init__(stmt_id, cell_x, cell_y, on_complete)
        self.wake_state = wake_state
        self.wifi_state = wifi_state
        self.wakeup = wakeup

    def write_fields(self, writer):
        super().write_fields(writer)
        writer.write_object(writer.wrap_str(self.wake_state))
        writer.write_object(self.wifi_state)
        writer.write_object(self.wakeup)

    def read_fields(self, reader):
        super().read_fields(reader)
        self.wake_state = reader.read_object()
        self.wifi_state = reader.read_object()
        self.wakeup = reader.read_object()

    def describe(self):
        return f"DeviceKeepAwake(id={self.stmt_id})"

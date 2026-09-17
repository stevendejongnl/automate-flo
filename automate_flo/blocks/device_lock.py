from ..base import Action

TYPE_ID = 1048


class DeviceLock(Action):
    """id 1048, UI name "Lock device". Extends Action directly -- no
    extra fields at all (locks the device now, no configuration)."""
    type_id = TYPE_ID

    def describe(self):
        return f"DeviceLock(id={self.stmt_id})"

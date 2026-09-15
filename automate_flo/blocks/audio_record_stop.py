from ..base import Action

TYPE_ID = 1016


class AudioRecordStop(Action):
    """id 1016, UI name "Stop audio recording". Extends Action directly --
    no extra fields (stops whatever recording AudioRecordStart started)."""
    type_id = TYPE_ID

    def describe(self):
        return f"AudioRecordStop(id={self.stmt_id})"

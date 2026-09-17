from ..base import Action

TYPE_ID = 1025


class CallEnd(Action):
    """id 1025, UI name "End call". Extends Action directly -- no
    extra fields at all (ends the current call, no configuration)."""
    type_id = TYPE_ID

    def describe(self):
        return f"CallEnd(id={self.stmt_id})"

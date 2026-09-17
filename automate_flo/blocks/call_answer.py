from ..base import Action

TYPE_ID = 1024


class CallAnswer(Action):
    """id 1024, UI name "Answer call". Extends Action directly -- no
    extra fields at all (answers the current ringing call, no
    configuration)."""
    type_id = TYPE_ID

    def describe(self):
        return f"CallAnswer(id={self.stmt_id})"

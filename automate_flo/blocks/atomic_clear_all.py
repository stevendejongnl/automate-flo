from ..base import Action

TYPE_ID = 1254


class AtomicClearAll(Action):
    """id 1254, UI name "Atomic clear all". Extends Action directly -- no
    extra fields at all (clears every atomic-variable register for the
    flow, no configuration)."""
    type_id = TYPE_ID

    def describe(self):
        return f"AtomicClearAll(id={self.stmt_id})"

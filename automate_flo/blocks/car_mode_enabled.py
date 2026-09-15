from ..base import IntermittentDecision

TYPE_ID = 1201


class CarModeEnabled(IntermittentDecision):
    """id 1201, UI name "Car mode enabled?" -- confirmed via live search:
    searching "car"/"auto"/"usb" in the block picker turns up NO dedicated
    Android-Auto/projection/headunit block at all, and no such string
    exists in strings.xml either. CarModeEnabled is Automate's only
    mechanism that reacts to Android Auto connecting, since Android Auto
    puts the phone into standard UiModeManager car mode. This is the block
    ChatGPT's community-flow reference was actually describing. Extends
    IntermittentDecision extends Decision, no extra fields."""
    type_id = TYPE_ID

    def __init__(self, stmt_id, cell_x=0, cell_y=0,
                 on_positive=None, on_negative=None, continuity=None):
        super().__init__(stmt_id, cell_x, cell_y, on_complete=None)
        self.on_positive = on_positive
        self.on_negative = on_negative
        self.continuity = continuity

    def describe(self):
        return f"CarModeEnabled(id={self.stmt_id})"

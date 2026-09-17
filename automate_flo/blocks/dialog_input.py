from ..base import Decision

TYPE_ID = 1054


class DialogInput(Decision):
    """id 1054, UI name "Input dialog". Extends ActivityDecision extends
    Decision directly (onPositive/onNegative, no continuity -- same
    family as DialogConfirm). Flattens ActivityDecision's timeout/
    start_activity/notification_channel_id (raw pass-through) inline,
    then adds title/regex/hint/prepopulate (wrap_str), input_type
    (wrap_double), suggestions (multi-value expression, raw
    pass-through), and var_result_text (VariableExpr, raw
    pass-through)."""
    type_id = TYPE_ID

    def __init__(self, stmt_id, cell_x=0, cell_y=0, on_positive=None, on_negative=None,
                 timeout=None, start_activity=None, notification_channel_id=None,
                 title=None, input_type=None, regex=None, hint=None,
                 prepopulate=None, suggestions=None, var_result_text=None):
        super().__init__(stmt_id, cell_x, cell_y, on_complete=None)
        self.on_positive = on_positive
        self.on_negative = on_negative
        self.timeout = timeout
        self.start_activity = start_activity
        self.notification_channel_id = notification_channel_id
        self.title = title
        self.input_type = input_type
        self.regex = regex
        self.hint = hint
        self.prepopulate = prepopulate
        self.suggestions = suggestions
        self.var_result_text = var_result_text

    def write_fields(self, writer):
        super().write_fields(writer)
        writer.write_object(self.timeout)
        writer.write_object(self.start_activity)
        writer.write_object(self.notification_channel_id)
        writer.write_object(writer.wrap_str(self.title))
        writer.write_object(writer.wrap_double(self.input_type))
        writer.write_object(writer.wrap_str(self.regex))
        writer.write_object(writer.wrap_str(self.hint))
        writer.write_object(writer.wrap_str(self.prepopulate))
        writer.write_object(self.suggestions)
        writer.write_object(self.var_result_text)

    def read_fields(self, reader):
        super().read_fields(reader)
        self.timeout = reader.read_object()
        self.start_activity = reader.read_object()
        self.notification_channel_id = reader.read_object()
        self.title = reader.read_object()
        self.input_type = reader.read_object()
        self.regex = reader.read_object()
        self.hint = reader.read_object()
        self.prepopulate = reader.read_object()
        self.suggestions = reader.read_object()
        self.var_result_text = reader.read_object()

    def describe(self):
        return f"DialogInput(id={self.stmt_id})"

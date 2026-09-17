from ..base import Action

TYPE_ID = 1044


class RingtoneGet(Action):
    """id 1044, UI name "Get ringtone". Extends RingtoneAction extends
    Action directly, flattening RingtoneAction's ringtone_type field
    inline (wrap_double), plus its own var_sound_uri (VariableExpr, raw
    pass-through) -- onComplete only, no continuity."""
    type_id = TYPE_ID

    def __init__(self, stmt_id, cell_x=0, cell_y=0, on_complete=None,
                 ringtone_type=None, var_sound_uri=None):
        super().__init__(stmt_id, cell_x, cell_y, on_complete)
        self.ringtone_type = ringtone_type
        self.var_sound_uri = var_sound_uri

    def write_fields(self, writer):
        super().write_fields(writer)
        writer.write_object(writer.wrap_double(self.ringtone_type))
        writer.write_object(self.var_sound_uri)

    def read_fields(self, reader):
        super().read_fields(reader)
        self.ringtone_type = reader.read_object()
        self.var_sound_uri = reader.read_object()

    def describe(self):
        return f"RingtoneGet(id={self.stmt_id})"

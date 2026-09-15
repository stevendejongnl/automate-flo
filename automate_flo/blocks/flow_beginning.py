from ..base import Action

TYPE_ID = 1072


class FlowBeginning(Action):
    """id 1072. The entry point of every flow; FlowBeginning->AppKill is
    byte-exact-verified against an Automate-exported sample built entirely
    by hand in the app UI, independent of this library."""
    type_id = TYPE_ID

    def __init__(self, stmt_id=1, cell_x=0, cell_y=0, on_complete=None,
                 title="", hidden=False, parallel=False):
        super().__init__(stmt_id, cell_x, cell_y, on_complete)
        self.title = title
        self.hidden = hidden
        self.parallel = parallel

    def write_fields(self, writer):
        super().write_fields(writer)
        writer.w.write_utf(self.title or "")
        writer.w.write_u8(1 if self.hidden else 0)   # version 114 >= 66
        writer.w.write_u8(1 if self.parallel else 0)
        writer.write_object(None)  # varPayload
        writer.write_object(None)  # varFiberUri (version 114 >= 43)

    def read_fields(self, reader):
        super().read_fields(reader)
        self.title = reader.r.read_utf()
        self.hidden = bool(reader.r.read_u8())
        self.parallel = bool(reader.r.read_u8())
        reader.read_object()  # varPayload, discarded
        reader.read_object()  # varFiberUri, discarded

    def describe(self):
        return f"FlowBeginning(id={self.stmt_id}, title={self.title!r})"

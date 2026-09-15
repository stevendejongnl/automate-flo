from ..base import Action

TYPE_ID = 1380


class AdbProtocolSet(Action):
    """id 1380, UI name "ADB protocol set". Extends AdbAction extends Action
    -- host/port/security/alias (same as AdbShellCommand), then this
    class's own protocol/tcpipPort."""
    type_id = TYPE_ID

    def __init__(self, stmt_id, cell_x=0, cell_y=0, on_complete=None,
                 host=None, port=None, security=None, alias=None,
                 protocol=None, tcpip_port=None):
        super().__init__(stmt_id, cell_x, cell_y, on_complete)
        self.host = host
        self.port = port
        self.security = security
        self.alias = alias
        self.protocol = protocol
        self.tcpip_port = tcpip_port

    def write_fields(self, writer):
        super().write_fields(writer)
        # AdbAction's own fields, common to AdbShellCommand and AdbProtocolSet.
        writer.write_object(self.host)
        writer.write_object(self.port)
        writer.write_object(self.security)  # version 114 >= 94
        writer.write_object(self.alias)
        writer.write_object(self.protocol)
        writer.write_object(self.tcpip_port)

    def read_fields(self, reader):
        super().read_fields(reader)
        self.host = reader.read_object()
        self.port = reader.read_object()
        self.security = reader.read_object()  # version 114 >= 94
        self.alias = reader.read_object()
        self.protocol = reader.read_object()
        self.tcpip_port = reader.read_object()

    def describe(self):
        return f"AdbProtocolSet(id={self.stmt_id})"

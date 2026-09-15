from ..base import Action

TYPE_ID = 1342


class AdbShellCommand(Action):
    """id 1342, UI name "ADB shell command". Extends AdbAction extends
    Action -- AdbAction's own S()/y0() write host/port/security(version
    114 >= 94, always written)/alias BEFORE this class's own fields:
    command, varStdout, varStderr, varExitCode."""
    type_id = TYPE_ID

    def __init__(self, stmt_id, command=None, cell_x=0, cell_y=0, on_complete=None,
                 host=None, port=None, security=None, alias=None,
                 var_stdout=None, var_stderr=None, var_exit_code=None):
        super().__init__(stmt_id, cell_x, cell_y, on_complete)
        self.host = host
        self.port = port
        self.security = security
        self.alias = alias
        self.command = command
        self.var_stdout = var_stdout
        self.var_stderr = var_stderr
        self.var_exit_code = var_exit_code

    def write_fields(self, writer):
        super().write_fields(writer)
        # AdbAction's own fields, common to AdbShellCommand and AdbProtocolSet.
        writer.write_object(self.host)
        writer.write_object(self.port)
        writer.write_object(self.security)  # version 114 >= 94
        writer.write_object(self.alias)
        writer.write_object(writer.wrap_str(self.command))
        writer.write_object(self.var_stdout)
        writer.write_object(self.var_stderr)
        writer.write_object(self.var_exit_code)

    def read_fields(self, reader):
        super().read_fields(reader)
        self.host = reader.read_object()
        self.port = reader.read_object()
        self.security = reader.read_object()  # version 114 >= 94
        self.alias = reader.read_object()
        self.command = reader.read_object()
        self.var_stdout = reader.read_object()
        self.var_stderr = reader.read_object()
        self.var_exit_code = reader.read_object()

    def describe(self):
        return f"AdbShellCommand(id={self.stmt_id})"

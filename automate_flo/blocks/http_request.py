from ..base import Action

TYPE_ID = 1087


class HttpRequest(Action):
    """id 1087, UI name "HTTP request". Extends Action."""
    type_id = TYPE_ID

    def __init__(self, stmt_id, url, cell_x=0, cell_y=0, on_complete=None,
                 network_interface=None, method=None, account=None,
                 timeout=None, alias=None, trust=None, dont_redirect=None,
                 content_type=None, body_part=None, body_path=None,
                 headers=None, save_response=None, response_path=None,
                 var_response_code=None, var_response_body=None,
                 var_response_headers=None):
        super().__init__(stmt_id, cell_x, cell_y, on_complete)
        self.network_interface = network_interface
        self.url = url
        self.method = method
        self.account = account
        self.timeout = timeout
        self.alias = alias
        self.trust = trust
        self.dont_redirect = dont_redirect
        self.content_type = content_type
        self.body_part = body_part
        self.body_path = body_path
        self.headers = headers
        self.save_response = save_response
        self.response_path = response_path
        self.var_response_code = var_response_code
        self.var_response_body = var_response_body
        self.var_response_headers = var_response_headers

    def write_fields(self, writer):
        super().write_fields(writer)
        writer.write_object(self.network_interface)   # version 114 >= 74
        writer.write_object(writer.wrap_str(self.url))
        writer.write_object(writer.wrap_str(self.method))
        writer.write_object(self.account)
        writer.write_object(self.timeout)              # version 114 >= 82
        writer.write_object(writer.wrap_str(self.alias))  # version 114 >= 109
        writer.write_object(self.trust)                 # version 114 >= 45
        writer.write_object(self.dont_redirect)          # version 114 >= 47
        writer.write_object(writer.wrap_str(self.content_type))
        writer.write_object(self.body_part)
        writer.write_object(self.body_path)              # version 114 >= 82
        writer.write_object(self.headers)                # version 114 >= 35
        writer.write_object(self.save_response)
        writer.write_object(self.response_path)
        writer.write_object(self.var_response_code)
        writer.write_object(self.var_response_body)
        writer.write_object(self.var_response_headers)   # version 114 >= 35

    def read_fields(self, reader):
        super().read_fields(reader)
        self.network_interface = reader.read_object()
        self.url = reader.read_object()
        self.method = reader.read_object()
        self.account = reader.read_object()
        self.timeout = reader.read_object()
        self.alias = reader.read_object()
        self.trust = reader.read_object()
        self.dont_redirect = reader.read_object()
        self.content_type = reader.read_object()
        self.body_part = reader.read_object()
        self.body_path = reader.read_object()
        self.headers = reader.read_object()
        self.save_response = reader.read_object()
        self.response_path = reader.read_object()
        self.var_response_code = reader.read_object()
        self.var_response_body = reader.read_object()
        self.var_response_headers = reader.read_object()

    def describe(self):
        return f"HttpRequest(id={self.stmt_id})"

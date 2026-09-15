from ..base import IntermittentDecision

TYPE_ID = 1146


class WifiNetworkConnected(IntermittentDecision):
    """id 1146, UI name "Wifi network connected?". Extends
    IntermittentDecision extends Decision -- onPositive/onNegative."""
    type_id = TYPE_ID

    def __init__(self, stmt_id, cell_x=0, cell_y=0, on_positive=None,
                 on_negative=None, continuity=None, ssid=None, bssid=None,
                 var_connected_ssid=None, var_connected_bssid=None,
                 var_connected_capabilities=None, var_connected_link_speed=None,
                 var_connected_frequency=None, var_connected_ip_address=None):
        super().__init__(stmt_id, cell_x, cell_y, on_complete=None)
        self.on_positive = on_positive
        self.on_negative = on_negative
        self.continuity = continuity
        self.ssid = ssid
        self.bssid = bssid
        self.var_connected_ssid = var_connected_ssid
        self.var_connected_bssid = var_connected_bssid
        self.var_connected_capabilities = var_connected_capabilities
        self.var_connected_link_speed = var_connected_link_speed
        self.var_connected_frequency = var_connected_frequency
        self.var_connected_ip_address = var_connected_ip_address

    def write_fields(self, writer):
        super().write_fields(writer)
        writer.write_object(writer.wrap_str(self.ssid))
        writer.write_object(writer.wrap_str(self.bssid))
        writer.write_object(self.var_connected_ssid)
        writer.write_object(self.var_connected_bssid)
        writer.write_object(self.var_connected_capabilities)
        writer.write_object(self.var_connected_link_speed)
        writer.write_object(self.var_connected_frequency)
        writer.write_object(self.var_connected_ip_address)

    def read_fields(self, reader):
        super().read_fields(reader)
        self.ssid = reader.read_object()
        self.bssid = reader.read_object()
        self.var_connected_ssid = reader.read_object()
        self.var_connected_bssid = reader.read_object()
        self.var_connected_capabilities = reader.read_object()
        self.var_connected_link_speed = reader.read_object()
        self.var_connected_frequency = reader.read_object()
        self.var_connected_ip_address = reader.read_object()

    def describe(self):
        return f"WifiNetworkConnected(id={self.stmt_id})"

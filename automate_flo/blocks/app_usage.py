from ..base import Action

TYPE_ID = 1310


class AppUsage(Action):
    """id 1310, UI name "App usage". Extends Action. Fields (all version gates satisfied at version 114): minTimestamp, maxTimestamp, interval (numeric expressions), packageName (string expression), statistic (numeric expression), varUsageDuration, varLastUsedTimestamp, varStatsStartTimestamp, varStatsEndTimestamp (VariableExpr, raw pass-through)."""
    type_id = TYPE_ID

    def __init__(self, stmt_id, cell_x=0, cell_y=0, on_complete=None, min_timestamp=None, max_timestamp=None, interval=None, package_name=None, statistic=None, var_usage_duration=None, var_last_used_timestamp=None, var_stats_start_timestamp=None, var_stats_end_timestamp=None):
        super().__init__(stmt_id, cell_x, cell_y, on_complete)
        self.min_timestamp = min_timestamp
        self.max_timestamp = max_timestamp
        self.interval = interval
        self.package_name = package_name
        self.statistic = statistic
        self.var_usage_duration = var_usage_duration
        self.var_last_used_timestamp = var_last_used_timestamp
        self.var_stats_start_timestamp = var_stats_start_timestamp
        self.var_stats_end_timestamp = var_stats_end_timestamp

    def write_fields(self, writer):
        super().write_fields(writer)
        writer.write_object(writer.wrap_double(self.min_timestamp))
        writer.write_object(writer.wrap_double(self.max_timestamp))
        writer.write_object(writer.wrap_double(self.interval))
        writer.write_object(writer.wrap_str(self.package_name))
        writer.write_object(writer.wrap_double(self.statistic))
        writer.write_object(self.var_usage_duration)
        writer.write_object(self.var_last_used_timestamp)
        writer.write_object(self.var_stats_start_timestamp)
        writer.write_object(self.var_stats_end_timestamp)

    def read_fields(self, reader):
        super().read_fields(reader)
        self.min_timestamp = reader.read_object()
        self.max_timestamp = reader.read_object()
        self.interval = reader.read_object()
        self.package_name = reader.read_object()
        self.statistic = reader.read_object()
        self.var_usage_duration = reader.read_object()
        self.var_last_used_timestamp = reader.read_object()
        self.var_stats_start_timestamp = reader.read_object()
        self.var_stats_end_timestamp = reader.read_object()

    def describe(self):
        return f"AppUsage(id={self.stmt_id})"

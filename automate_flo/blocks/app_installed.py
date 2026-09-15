from ..base import IntermittentDecision

TYPE_ID = 1007


class AppInstalled(IntermittentDecision):
    """id 1007, UI name "App installed?". Extends IntermittentDecision
    directly -- onPositive/onNegative/continuity, plus packageName (nullable
    string expression), then 8 variable-reference fields (I3.l/VariableExpr,
    raw pass-through, no wrapping): varPackageName, varDisplayName,
    varVersionCode, varVersionName, varCacheSize, varDataSize, varCodeSize,
    varSourceDirs. Several are version-gated in source (19/48/48/64/64/64/96)
    but all gates are always satisfied at this library's target version 114,
    so every field is written/read unconditionally."""
    type_id = TYPE_ID

    def __init__(self, stmt_id, cell_x=0, cell_y=0, on_positive=None, on_negative=None, continuity=None, package_name=None, var_package_name=None, var_display_name=None, var_version_code=None, var_version_name=None, var_cache_size=None, var_data_size=None, var_code_size=None, var_source_dirs=None):
        super().__init__(stmt_id, cell_x, cell_y, on_complete=None)
        self.on_positive = on_positive
        self.on_negative = on_negative
        self.continuity = continuity
        self.package_name = package_name
        self.var_package_name = var_package_name
        self.var_display_name = var_display_name  # version 114 >= 19
        self.var_version_code = var_version_code  # version 114 >= 48
        self.var_version_name = var_version_name  # version 114 >= 48
        self.var_cache_size = var_cache_size  # version 114 >= 64
        self.var_data_size = var_data_size  # version 114 >= 64
        self.var_code_size = var_code_size  # version 114 >= 64
        self.var_source_dirs = var_source_dirs  # version 114 >= 96

    def write_fields(self, writer):
        super().write_fields(writer)
        writer.write_object(writer.wrap_str(self.package_name))
        writer.write_object(self.var_package_name)
        writer.write_object(self.var_display_name)  # version 114 >= 19
        writer.write_object(self.var_version_code)  # version 114 >= 48
        writer.write_object(self.var_version_name)  # version 114 >= 48
        writer.write_object(self.var_cache_size)  # version 114 >= 64
        writer.write_object(self.var_data_size)  # version 114 >= 64
        writer.write_object(self.var_code_size)  # version 114 >= 64
        writer.write_object(self.var_source_dirs)  # version 114 >= 96

    def read_fields(self, reader):
        super().read_fields(reader)
        self.package_name = reader.read_object()
        self.var_package_name = reader.read_object()
        self.var_display_name = reader.read_object()  # version 114 >= 19
        self.var_version_code = reader.read_object()  # version 114 >= 48
        self.var_version_name = reader.read_object()  # version 114 >= 48
        self.var_cache_size = reader.read_object()  # version 114 >= 64
        self.var_data_size = reader.read_object()  # version 114 >= 64
        self.var_code_size = reader.read_object()  # version 114 >= 64
        self.var_source_dirs = reader.read_object()  # version 114 >= 96

    def describe(self):
        return f"AppInstalled(id={self.stmt_id})"

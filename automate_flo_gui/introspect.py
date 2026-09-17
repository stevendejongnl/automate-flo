from automate_flo.base import Decision
from automate_flo import blocks
import inspect

def build_block_schemas():
    schemas = []
    for cls in blocks.ALL_BLOCKS:
        doc_summary = cls.__doc__.split('\n')[0] if cls.__doc__ else ""
        category = "decision" if issubclass(cls, Decision) else "action"
        fields = []
        for param_name, param in inspect.signature(cls.__init__).parameters.items():
            if param_name in ["self", "stmt_id", "cell_x", "cell_y", "on_complete", "on_positive", "on_negative"]:
                continue
            field = {
                "name": param_name,
                "required": param.default is inspect.Parameter.empty,
                "default": param.default if param.default is not inspect.Parameter.empty else None,
                "kind": "boolean" if isinstance(param.default, bool) else
                        "number" if isinstance(param.default, (int, float)) else
                        "string"
            }
            fields.append(field)
        schemas.append({
            "type_name": cls.__name__,
            "type_id": cls.type_id,
            "category": category,
            "is_entry_point": cls.__name__ == "FlowBeginning",
            "doc_summary": doc_summary,
            "fields": fields
        })
    return schemas

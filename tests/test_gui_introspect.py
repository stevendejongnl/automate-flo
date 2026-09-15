import unittest
from automate_flo_gui.introspect import build_block_schemas
from automate_flo import blocks

class TestGuiIntrospect(unittest.TestCase):
    def test_build_block_schemas(self):
        schemas = build_block_schemas()
        self.assertEqual(len(schemas), len(blocks.ALL_BLOCKS))

        delay_schema = next(schema for schema in schemas if schema["type_name"] == "Delay")
        self.assertEqual(delay_schema["category"], "action")
        self.assertTrue(delay_schema["fields"][0]["name"] == "seconds")
        self.assertTrue(delay_schema["fields"][0]["required"])
        self.assertEqual(delay_schema["fields"][0]["kind"], "string")

        expression_decision_schema = next(schema for schema in schemas if schema["type_name"] == "ExpressionDecision")
        self.assertEqual(expression_decision_schema["category"], "decision")

        flow_beginning_schema = next(schema for schema in schemas if schema["type_name"] == "FlowBeginning")
        hidden_field = next(f for f in flow_beginning_schema["fields"] if f["name"] == "hidden")
        self.assertFalse(hidden_field["required"])
        self.assertEqual(hidden_field["default"], False)
        self.assertEqual(hidden_field["kind"], "boolean")

if __name__ == '__main__':
    unittest.main()

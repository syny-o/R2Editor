import sys
import unittest
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from text_editor.completion_rules import (
    SPECIAL_COMMAND_TEMPLATES,
    completion_model_name,
)


class CompletionRulesTest(unittest.TestCase):
    def test_pbc_variable_command_uses_pbc_variables(self):
        self.assertEqual(
            completion_model_name("MonitorVariablesCANape"),
            "pbc_variables",
        )

    def test_graph_variables_uses_current_testcase_variables(self):
        self.assertEqual(
            completion_model_name("GraphVariables"),
            "graph_variables",
        )

    def test_monitor_variables_uses_dspace_variables(self):
        self.assertEqual(
            completion_model_name("MonitorVariables"),
            "dspace_variables",
        )

    def test_known_condition_uses_its_values(self):
        self.assertEqual(
            completion_model_name("Condition", {"Condition": object()}),
            "values",
        )

    def test_unknown_text_uses_conditions(self):
        self.assertEqual(completion_model_name("Unknown"), "conditions")

    def test_special_command_template_is_unchanged(self):
        self.assertEqual(
            SPECIAL_COMMAND_TEMPLATES["CANapeCommand"],
            (' = "CANape_GetObjectValue()"', 2),
        )


if __name__ == "__main__":
    unittest.main()

import sys
import unittest
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from text_editor.text_operations import (
    PARAGRAPH_SEPARATOR,
    build_chapter,
    build_command,
    build_testcase,
    completion_context,
    format_first_assignment,
    graph_variables_before_cursor,
    leading_whitespace,
    normalize_variable_command,
    split_indentation,
    transform_indentation,
)


class TextOperationsTest(unittest.TestCase):
    def test_leading_whitespace(self):
        self.assertEqual(leading_whitespace('\t  command'), '\t  ')
        self.assertEqual(leading_whitespace('command'), '')

    def test_split_indentation(self):
        self.assertEqual(split_indentation('\t  Name'), ('\t  ', 'Name'))

    def test_build_command(self):
        self.assertEqual(build_command('  Action'), '  $COM: "Action" $')

    def test_build_testcase(self):
        self.assertEqual(
            build_testcase('\tCase name'),
            '\tTESTCASE "Case name" ID "" REFERENCE "" EXPECTEDRESULT 1',
        )

    def test_build_chapter(self):
        self.assertEqual(
            build_chapter('  Chapter name'),
            '  CHAPTER "Chapter name"\n  \n  END CHAPTER',
        )

    def test_graph_variables_use_only_current_testcase(self):
        text = (
            'TESTCASE "Old"\n'
            'MonitorVariables = "OLD_1 OLD_2, 100, 10"\n'
            'TESTCASE "Current"\n'
            'MonitorVariablesCANape = "NEW_1 NEW_2, 100, 10"\n'
            'GraphVariables = ""'
        )
        self.assertEqual(
            graph_variables_before_cursor(text, len(text)),
            ['NEW_1', 'NEW_2'],
        )

    def test_graph_variables_are_case_insensitive(self):
        text = 'monitorvariables = "Var_1 Var_2, 100, 10"'
        self.assertEqual(
            graph_variables_before_cursor(text, len(text)),
            ['Var_1', 'Var_2'],
        )

    def test_completion_context_uses_text_before_first_equal(self):
        self.assertEqual(completion_context('  Condition = Value', 12), 'Condition')
        self.assertEqual(completion_context('Condition', 9, True), '')

    def test_format_first_assignment_preserves_other_equal_signs(self):
        self.assertEqual(
            format_first_assignment('Condition=Value==Other'),
            'Condition = Value==Other',
        )

    def test_format_first_assignment_honors_exclusions(self):
        line = 'GraphVariables="A B"'
        self.assertEqual(
            format_first_assignment(line, ('GraphVariables',)),
            line,
        )

    def test_normalize_monitor_variables(self):
        self.assertEqual(
            normalize_variable_command(
                'MonitorVariablesCANape  =  " Var_1   Var_2 , 100 , 10 "'
            ),
            'MonitorVariablesCANape = "Var_1 Var_2,100,10"',
        )

    def test_normalize_graph_variables(self):
        self.assertEqual(
            normalize_variable_command('GraphVariables = " Var_1   Var_2 "'),
            'GraphVariables = "Var_1 Var_2"',
        )

    def test_normalize_variable_command_ignores_comments(self):
        line = "'MonitorVariables = \"Var_1,100,10\""
        self.assertEqual(normalize_variable_command(line), line)

    def test_indent_multiple_lines(self):
        source = PARAGRAPH_SEPARATOR.join(('one', '  two'))
        expected = PARAGRAPH_SEPARATOR.join(('\tone', '\t  two'))
        self.assertEqual(transform_indentation(source, 'indent'), expected)

    def test_dedent_tabs_and_two_spaces(self):
        source = PARAGRAPH_SEPARATOR.join(('\tone', '  two', 'three'))
        expected = PARAGRAPH_SEPARATOR.join(('one', 'two', 'three'))
        self.assertEqual(transform_indentation(source, 'dedent'), expected)

    def test_comment_toggles_each_line(self):
        source = PARAGRAPH_SEPARATOR.join(('one', "'two"))
        expected = PARAGRAPH_SEPARATOR.join(("'one", 'two'))
        self.assertEqual(transform_indentation(source, 'comment'), expected)

    def test_unknown_operation_is_rejected(self):
        with self.assertRaises(ValueError):
            transform_indentation('text', 'unknown')


if __name__ == '__main__':
    unittest.main()

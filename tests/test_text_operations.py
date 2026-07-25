import sys
import unittest
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from text_editor.editing.text_operations import (
    PARAGRAPH_SEPARATOR,
    build_chapter,
    build_command,
    build_testcase,
    completion_context,
    cursor_column_after_transform,
    cursor_position_after_format,
    format_first_assignment,
    graph_variables_before_cursor,
    leading_whitespace,
    normalize_variable_command,
    smart_home_column,
    split_indentation,
    transform_indentation,
)
from text_editor.editing.script_formatter import TextFormatter


class TextOperationsTest(unittest.TestCase):
    def test_leading_whitespace(self):
        self.assertEqual(leading_whitespace('\t  command'), '\t  ')
        self.assertEqual(leading_whitespace('command'), '')

    def test_split_indentation(self):
        self.assertEqual(split_indentation('\t  Name'), ('\t  ', 'Name'))

    def test_smart_home_moves_to_first_text_column(self):
        self.assertEqual(smart_home_column('\t  Name', 7), 3)

    def test_smart_home_toggles_from_text_to_line_start(self):
        self.assertEqual(smart_home_column('\t  Name', 3), 0)

    def test_smart_home_stays_at_start_on_unindented_line(self):
        self.assertEqual(smart_home_column('Name', 2), 0)
        self.assertEqual(smart_home_column('Name', 0), 0)

    def test_cursor_stays_at_line_start_when_dedenting(self):
        self.assertEqual(cursor_column_after_transform('\tName', 'Name', 0), 0)

    def test_cursor_tracks_text_when_dedenting(self):
        self.assertEqual(cursor_column_after_transform('\tName', 'Name', 3), 2)

    def test_cursor_tracks_text_when_comment_is_inserted(self):
        self.assertEqual(
            cursor_column_after_transform('\tName', "\t'Name", 1),
            2,
        )

    def test_cursor_inside_indentation_stays_before_inserted_comment(self):
        self.assertEqual(
            cursor_column_after_transform('\t  Name', "\t  'Name", 1),
            1,
        )

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

    def test_formatter_can_be_reused_after_incomplete_blocks(self):
        text = (
            'TESTCASE "Example" EXPECTEDRESULT 1\n'
            'ELSE\n'
            'IF Value == 1'
        )
        formatter = TextFormatter(text)

        self.assertEqual(formatter.run(), formatter.run())

    def test_formatter_chapter_output(self):
        self.assertEqual(
            TextFormatter('CHAPTER "One"\nEND CHAPTER').run(),
            '\nCHAPTER "One"\n\nEND CHAPTER',
        )

    def test_formatter_if_indentation(self):
        result = TextFormatter(
            'TESTCASE "A" EXPECTEDRESULT 1\n'
            'IF Value == 1\n'
            '$COM: "Action" $\n'
            'ENDIF'
        ).run()
        self.assertIn('-TESTCASE-NUMBER- 1', result)
        self.assertTrue(result.endswith(
            '\n\tIF Value == 1\n\n\t\t$COM: "Action" $\n\n\tENDIF'
        ))

    def test_formatter_for_indentation(self):
        result = TextFormatter(
            'TESTCASE "A" EXPECTEDRESULT 1\n'
            'FOR X = A B DO\n'
            '$COM: "Action" $\n'
            'NEXT'
        ).run()
        self.assertTrue(result.endswith(
            '\n\tFOR X = A B DO\n\n\t\t$COM: "Action" $\n\n\tNEXT'
        ))

    def test_formatter_else_if_is_a_nested_if(self):
        source = (
            'TESTCASE "A" EXPECTEDRESULT 1\n'
            'IF A THEN\n'
            'ELSE IF B THEN\n'
            'ELSE\n'
            'ENDIF\n'
            'ENDIF'
        )
        formatted = TextFormatter(source).run()

        self.assertEqual(TextFormatter(formatted).run(), formatted)

    def test_control_keyword_inside_text_does_not_change_indentation(self):
        result = TextFormatter(
            'TESTCASE "A" EXPECTEDRESULT 1\n'
            'Message = "IF is only text"\n'
            '$COM: "Action" $'
        ).run()

        self.assertTrue(result.endswith(
            '\n\tMessage = "IF is only text"\n\n\t$COM: "Action" $'
        ))

    def test_commented_control_commands_do_not_change_indentation(self):
        source = (
            'TESTCASE "A" EXPECTEDRESULT 1\n'
            "'IF A THEN\n"
            "'ELSE\n"
            "'ENDIF\n"
            "'FOR X = A B DO\n"
            "'NEXT\n"
            '\'$COM: "Commented command" $\n'
            "'HIL = Reset\n"
            'Value = 1'
        )
        result = TextFormatter(source).run()

        self.assertTrue(result.endswith(
            "\n\t'IF A THEN"
            "\n\t'ELSE"
            "\n\t'ENDIF"
            "\n\t'FOR X = A B DO"
            "\n\t'NEXT"
            '\n\t\'$COM: "Commented command" $'
            "\n\t'HIL = Reset"
            '\n\tValue = 1'
        ))

    def test_unmatched_block_commands_do_not_crash_formatter(self):
        source = (
            'TESTCASE "A" EXPECTEDRESULT 1\n'
            'ENDIF\n'
            'NEXT\n'
            'ELSE'
        )

        result = TextFormatter(source).run()

        self.assertTrue(result.endswith(
            '\n\tENDIF'
            '\n\n\tNEXT'
            '\n\n\tELSE'
        ))

    def test_cursor_stays_in_word_when_formatting_adds_lines_and_indentation(self):
        source = (
            'TESTCASE "A" EXPECTEDRESULT 1\n'
            '$COM: "Perform the test" $\n'
            'Brake = Apply'
        )
        source_position = source.index('Perform') + 4
        formatted = TextFormatter(source).run()

        formatted_position = cursor_position_after_format(
            source,
            formatted,
            source_position,
        )

        self.assertEqual(
            formatted_position,
            formatted.index('Perform') + 4,
        )

    def test_cursor_uses_same_occurrence_of_duplicate_line(self):
        source = 'Wait = 100\nWait = 100'
        formatted = '\tWait = 100\n\n\tWait = 100'
        source_position = source.rindex('100') + 2

        formatted_position = cursor_position_after_format(
            source,
            formatted,
            source_position,
        )

        self.assertEqual(
            formatted_position,
            formatted.rindex('100') + 2,
        )

    def test_cursor_tracks_word_when_variable_command_spacing_is_normalized(self):
        source = 'MonitorVariables = " Var_1   Var_2 , 100 , 10 "'
        formatted = normalize_variable_command(source)
        source_position = source.index('Var_2') + 3

        formatted_position = cursor_position_after_format(
            source,
            formatted,
            source_position,
        )

        self.assertEqual(
            formatted_position,
            formatted.index('Var_2') + 3,
        )

    def test_indent_multiple_lines(self):
        source = PARAGRAPH_SEPARATOR.join(('one', '  two'))
        expected = PARAGRAPH_SEPARATOR.join(('\tone', '\t  two'))
        self.assertEqual(transform_indentation(source, 'indent'), expected)

    def test_selection_ending_at_next_line_start_does_not_change_next_line(self):
        source = f'one{PARAGRAPH_SEPARATOR}'

        self.assertEqual(
            transform_indentation(source, 'indent'),
            f'\tone{PARAGRAPH_SEPARATOR}',
        )
        self.assertEqual(
            transform_indentation(source, 'comment'),
            f"'one{PARAGRAPH_SEPARATOR}",
        )

    def test_dedent_tabs_and_two_spaces(self):
        source = PARAGRAPH_SEPARATOR.join(('\tone', '  two', 'three'))
        expected = PARAGRAPH_SEPARATOR.join(('one', 'two', 'three'))
        self.assertEqual(transform_indentation(source, 'dedent'), expected)

    def test_comment_comments_entire_mixed_selection(self):
        source = PARAGRAPH_SEPARATOR.join(('one', "'two"))
        expected = PARAGRAPH_SEPARATOR.join(("'one", "'two"))
        self.assertEqual(transform_indentation(source, 'comment'), expected)

    def test_comment_uncomments_selection_when_all_lines_are_commented(self):
        source = PARAGRAPH_SEPARATOR.join(("'one", "\t'two"))
        expected = PARAGRAPH_SEPARATOR.join(('one', '\ttwo'))
        self.assertEqual(transform_indentation(source, 'comment'), expected)

    def test_comment_is_inserted_after_indentation(self):
        self.assertEqual(
            transform_indentation('\t  command', 'comment'),
            "\t  'command",
        )

    def test_comment_keeps_empty_lines_unchanged(self):
        source = PARAGRAPH_SEPARATOR.join(('one', '', 'two'))
        expected = PARAGRAPH_SEPARATOR.join(("'one", '', "'two"))
        self.assertEqual(transform_indentation(source, 'comment'), expected)

    def test_unknown_operation_is_rejected(self):
        with self.assertRaises(ValueError):
            transform_indentation('text', 'unknown')


if __name__ == '__main__':
    unittest.main()

import sys
import unittest
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from text_editor.text_operations import (
    PARAGRAPH_SEPARATOR,
    leading_whitespace,
    transform_indentation,
)


class TextOperationsTest(unittest.TestCase):
    def test_leading_whitespace(self):
        self.assertEqual(leading_whitespace('\t  command'), '\t  ')
        self.assertEqual(leading_whitespace('command'), '')

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

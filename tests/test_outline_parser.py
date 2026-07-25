import sys
import unittest
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from text_editor.outline.parser import (
    OutlineSection,
    line_number_from_position,
    parse_outline_sections,
)


class OutlineParserTest(unittest.TestCase):
    def test_parses_chapters_testcases_and_end_chapters(self):
        text = (
            'CHAPTER "First"\n'
            'TESTCASE "Case A" EXPECTEDRESULT 1\n'
            'END CHAPTER'
        )

        self.assertEqual(
            parse_outline_sections(text),
            (
                OutlineSection('chapter', 'First', 0),
                OutlineSection('testcase', 'Case A', text.index('TESTCASE')),
                OutlineSection('end_chapter', '', text.index('END CHAPTER')),
            ),
        )

    def test_ignores_commented_sections(self):
        text = (
            '\'CHAPTER "Disabled"\n'
            '\t\'TESTCASE "Disabled" EXPECTEDRESULT 1\n'
            'CHAPTER "Active"'
        )

        self.assertEqual(
            parse_outline_sections(text),
            (OutlineSection('chapter', 'Active', text.rindex('CHAPTER')),),
        )

    def test_requires_title_and_expected_result(self):
        text = (
            'CHAPTER\n'
            'TESTCASE "Incomplete"\n'
            'TESTCASE "Complete" EXPECTEDRESULT 1'
        )

        self.assertEqual(
            parse_outline_sections(text),
            (
                OutlineSection(
                    'testcase',
                    'Complete',
                    text.rindex('TESTCASE'),
                ),
            ),
        )

    def test_parsing_is_case_insensitive_and_keeps_indented_position(self):
        text = '\tchapter "Lower"\n\t testcase "Case" expectedresult 1'

        sections = parse_outline_sections(text)

        self.assertEqual(sections[0], OutlineSection('chapter', 'Lower', 0))
        self.assertEqual(
            sections[1],
            OutlineSection('testcase', 'Case', text.index('\t testcase')),
        )

    def test_line_number_from_position_is_one_based(self):
        text = 'first\nsecond\nthird'
        self.assertEqual(line_number_from_position(text, text.index('third')), 3)


if __name__ == '__main__':
    unittest.main()

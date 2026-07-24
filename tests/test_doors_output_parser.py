import unittest

from data_manager.doors_output_parser import (
    extract_attributes,
    extract_baselines,
    parse_requirement,
)


class DoorsOutputParserTests(unittest.TestCase):
    def test_extracts_attributes(self):
        text = (
            '<ATTRIBUTE_START>Object Text<ATTRIBUTE_END>'
            '<ATTRIBUTE_START>Status<ATTRIBUTE_END>'
        )

        self.assertEqual(
            extract_attributes(text),
            ['Object Text', 'Status'],
        )

    def test_extracts_baseline_with_multiline_annotation(self):
        text = (
            '<BASELINE_START>'
            '<VERSION_START>1.2<VERSION_END>'
            '<USER_START>tester<USER_END>'
            '<DATE_START>2026-07-24<DATE_END>'
            '<ANNOTATION_START>line 1\nline 2<ANNOTATION_END>'
            '<BASELINE_END>'
        )

        self.assertEqual(
            extract_baselines(text),
            {'1.2': ['tester', '2026-07-24', 'line 1\nline 2']},
        )

    def test_parses_requirement(self):
        text = (
            '<ID_START>REQ-1<ID_END>'
            '<LEVEL_START>2<LEVEL_END>'
            '<HEADING_START>Heading<HEADING_END>'
            '<COLUMN_START>first<COLUMN_END>'
            '<COLUMN_START>second<COLUMN_END>'
            '<OUTLINK_START>module:2<OUTLINK_END>'
            '<INLINK_START>module:3<INLINK_END>'
        )

        self.assertEqual(
            parse_requirement(text),
            {
                'identifier': 'REQ-1',
                'level': 2,
                'heading': 'Heading',
                'columns': ['first', 'second'],
                'outlinks': ['module:2'],
                'inlinks': ['module:3'],
            },
        )

    def test_can_use_column_as_identifier(self):
        text = (
            '<ID_START>REQ-1<ID_END>'
            '<LEVEL_START>1<LEVEL_END>'
            '<COLUMN_START>COLUMN-ID<COLUMN_END>'
        )

        self.assertEqual(
            parse_requirement(text, column_number_as_identifier=0)[
                'identifier'
            ],
            'COLUMN-ID',
        )


if __name__ == '__main__':
    unittest.main()

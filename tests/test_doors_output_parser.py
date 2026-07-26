import unittest

from data_manager.doors.output_parser import (
    extract_attributes,
    extract_baselines,
    parse_module_output,
    parse_requirement,
    validate_module_output,
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

    def test_rejects_missing_module_path(self):
        result = validate_module_output('connection failed', '/Project/Module')

        self.assertFalse(result['success'])
        self.assertIn('invalid module path', result['message'])
        self.assertIsNone(result['baselines'])

    def test_returns_metadata_when_requirements_are_missing(self):
        output = (
            '<PATH_START>/Project/Module<PATH_END>'
            '<ATTRIBUTE_START>Status<ATTRIBUTE_END>'
            '<BASELINE_START>'
            '<VERSION_START>1.0<VERSION_END>'
            '<USER_START>tester<USER_END>'
            '<DATE_START>2026-07-24<DATE_END>'
            '<BASELINE_END>'
        )

        result = validate_module_output(output, '/Project/Module')

        self.assertFalse(result['success'])
        self.assertIn('Invalid column name', result['message'])
        self.assertEqual(result['attributes'], ['Status'])
        self.assertEqual(
            result['baselines'],
            {'1.0': ['tester', '2026-07-24', '']},
        )

    def test_accepts_module_with_requirements_section(self):
        output = (
            '<PATH_START>/Project/Module<PATH_END>'
            '<REQUIREMENT_START>data<REQUIREMENT_END>'
            '<REQUIREMENTS_END>'
        )

        result = validate_module_output(output, '/Project/Module')

        self.assertTrue(result['success'])
        self.assertEqual(result['message'], 'OK')

    def test_extracts_requested_module_data(self):
        output = (
            '<<<MODULE_START>>>'
            '<PATH_START>/Other<PATH_END>'
            '<REQUIREMENT_START>other<REQUIREMENT_END>'
            '<<<MODULE_END>>>'
            '<<<MODULE_START>>>'
            '<PATH_START>/Target<PATH_END>'
            '<ATTRIBUTE_START>Status<ATTRIBUTE_END>'
            '<REQUIREMENT_START>first\nline<REQUIREMENT_END>'
            '<REQUIREMENT_START>second<REQUIREMENT_END>'
            '<<<MODULE_END>>>'
        )

        result = parse_module_output(output, '/Target')

        self.assertEqual(result['attributes'], ['Status'])
        self.assertEqual(result['baselines'], {})
        self.assertEqual(result['requirements'], ['first\nline', 'second'])

    def test_returns_none_when_requested_module_is_not_present(self):
        self.assertIsNone(parse_module_output('', '/Missing'))


if __name__ == '__main__':
    unittest.main()

import unittest

from data_manager.condition_file_format import (
    parse_condition_file,
    serialize_condition_file,
)


SAMPLE = (
    '<?xml version="1.0"?>\n<Conditions>\n'
    '\t<Condition Name="Ignition" Type="Input">\n'
    '\t\t<Value Name="On" Type="Boolean">\n'
    '\t\t\t<TS Name="Set ignition" A="Set" '
    'Nominal="1" Comment="required" />\n'
    '\t\t</Value>\n'
    '\t</Condition>\n'
    '</Conditions>'
)


class ConditionFileFormatTests(unittest.TestCase):
    def test_parses_condition_value_and_test_step(self):
        header, conditions = parse_condition_file(SAMPLE)

        self.assertEqual(
            header,
            '<?xml version="1.0"?>\n<Conditions>\n\t',
        )
        self.assertEqual(conditions[0]['name'], 'Ignition')
        self.assertEqual(conditions[0]['category'], 'Input')
        self.assertEqual(conditions[0]['values'][0]['name'], 'On')
        self.assertEqual(
            conditions[0]['values'][0]['test_steps'][0],
            {
                'name': 'Set ignition',
                'action': 'Set',
                'nominal': '1',
                'comment': 'required',
            },
        )

    def test_serializes_parsed_data(self):
        header, conditions = parse_condition_file(SAMPLE)

        result = serialize_condition_file(header, conditions)

        self.assertIn(
            '<Condition Name="Ignition" Type="Input">',
            result,
        )
        self.assertIn(
            '<TS Name="Set ignition" A="Set" '
            'Nominal="1" Comment="required" />',
            result,
        )
        self.assertTrue(result.endswith('</Conditions>'))


if __name__ == '__main__':
    unittest.main()

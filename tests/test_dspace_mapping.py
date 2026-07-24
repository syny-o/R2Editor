import unittest

from data_manager.dspace_mapping import (
    parse_dspace_mapping,
    serialize_dspace_mapping,
)


class DspaceMappingTests(unittest.TestCase):
    def test_parses_definitions_and_variables(self):
        text = (
            '# header\n'
            'def Engine():\n'
            '\tEngineVar = []\n'
            '\tEngineVar.append(["Speed", 0, "Model/Speed"])\n'
            '\tEngineVar.append(["Torque", 1, "Model/Torque"])\n'
            '\treturn EngineVar\n\n'
            'def Footer():\n'
            '\tpass\n'
        )

        header, footer, definitions = parse_dspace_mapping(text)

        self.assertEqual(header, '# header\n')
        self.assertTrue(footer.startswith('Footer():'))
        self.assertEqual(
            definitions,
            [
                (
                    'Engine',
                    [
                        ('Speed', '0', 'Model/Speed'),
                        ('Torque', '1', 'Model/Torque'),
                    ],
                )
            ],
        )

    def test_serializes_mapping_in_original_layout(self):
        result = serialize_dspace_mapping(
            '# header\n',
            'Footer():\n\tpass\n',
            [('Engine', [('Speed', '0', 'Model/Speed')])],
        )

        self.assertTrue(result.startswith('# header\ndef Engine():\n'))
        self.assertIn('EngineVar.append(["Speed"', result)
        self.assertIn(',"Model/Speed"])', result)
        self.assertTrue(result.endswith('def Footer():\n\tpass\n'))


if __name__ == '__main__':
    unittest.main()

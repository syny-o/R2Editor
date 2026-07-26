import unittest

from data_manager.requirements.comparison import compare_requirement_data


class RequirementComparisonTests(unittest.TestCase):
    def test_reports_added_and_missing_requirements(self):
        differences = compare_requirement_data(
            ['Status'],
            {'REQ-OLD': ['Approved']},
            {'REQ-NEW': ['Draft']},
        )

        by_identifier = {
            difference['identifier']: difference
            for difference in differences
        }
        self.assertEqual(by_identifier['REQ-OLD']['status'], 'missing')
        self.assertEqual(by_identifier['REQ-NEW']['status'], 'new')

    def test_reports_changed_columns(self):
        differences = compare_requirement_data(
            ['Status', 'Text'],
            {'REQ-1': ['Draft', 'Original']},
            {'REQ-1': ['Approved', 'Updated']},
        )

        self.assertEqual(
            differences,
            [
                {
                    'identifier': 'REQ-1',
                    'status': 'changed',
                    'changes': [
                        ('Status', 'Draft', 'Approved'),
                        ('Text', 'Original', 'Updated'),
                    ],
                }
            ],
        )

    def test_ignores_unchanged_requirements(self):
        self.assertEqual(
            compare_requirement_data(
                ['Status'],
                {'REQ-1': ['Approved']},
                {'REQ-1': ['Approved']},
            ),
            [],
        )


if __name__ == '__main__':
    unittest.main()

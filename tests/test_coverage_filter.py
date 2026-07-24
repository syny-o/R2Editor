import unittest

from data_manager.coverage_filter import translate_coverage_filter


class CoverageFilterTests(unittest.TestCase):
    def test_translates_column_names_to_indexes(self):
        translated = translate_coverage_filter(
            'Status == "Approved" and Priority == "High"',
            ['Status', 'Priority'],
        )

        self.assertEqual(
            translated,
            'column[0] == "Approved" and column[1] == "High"',
        )

    def test_replaces_longest_column_name_first(self):
        translated = translate_coverage_filter(
            'Object Text_DXL != Object Text',
            ['Object Text', 'Object Text_DXL'],
        )

        self.assertEqual(translated, 'column[1] != column[0]')

    def test_trims_filter(self):
        self.assertEqual(
            translate_coverage_filter('  Status  ', ['Status']),
            'column[0]',
        )


if __name__ == '__main__':
    unittest.main()

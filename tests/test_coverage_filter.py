import unittest

from data_manager.coverage_filter import (
    matching_references,
    translate_coverage_filter,
)


class FakeRequirement:
    def __init__(self, reference, columns_data, children=None):
        self.reference = reference
        self.columns_data = columns_data
        self.children = children or []

    def rowCount(self):
        return len(self.children)

    def child(self, row):
        return self.children[row]


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

    def test_collects_matching_references_from_nested_tree(self):
        root = FakeRequirement(
            'root',
            [],
            [
                FakeRequirement(
                    'CHAPTER',
                    ['Chapter', ''],
                    [
                        FakeRequirement('REQ-1', ['Approved', 'High']),
                        FakeRequirement('REQ-2', ['Draft', 'High']),
                    ],
                ),
                FakeRequirement('REQ-3', ['Approved', 'Low']),
            ],
        )

        result = matching_references(
            root,
            'column[0] == "Approved" and column[1] == "High"',
        )

        self.assertEqual(result, ['req-1'])

    def test_propagates_invalid_filter_expression(self):
        root = FakeRequirement(
            'root',
            [],
            [FakeRequirement('REQ-1', ['Approved'])],
        )

        with self.assertRaises(IndexError):
            matching_references(root, 'column[2] == "Approved"')


if __name__ == '__main__':
    unittest.main()

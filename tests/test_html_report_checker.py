import unittest

from data_manager.html_report_checker import classify_references


class HtmlReportCheckerTests(unittest.TestCase):
    def test_classifies_covered_and_missing_references(self):
        missing, covered = classify_references(
            '<p>REQ-1 passed</p><p>REQ-3 passed</p>',
            ['REQ-1', 'REQ-2', 'REQ-3'],
        )

        self.assertEqual(missing, ['REQ-2'])
        self.assertEqual(covered, ['REQ-1', 'REQ-3'])

    def test_matching_is_case_insensitive(self):
        missing, covered = classify_references('req-1', ['REQ-1'])

        self.assertEqual(missing, [])
        self.assertEqual(covered, ['REQ-1'])

    def test_preserves_reference_order(self):
        missing, covered = classify_references(
            '',
            ['REQ-3', 'REQ-1', 'REQ-2'],
        )

        self.assertEqual(missing, ['REQ-3', 'REQ-1', 'REQ-2'])
        self.assertEqual(covered, [])


if __name__ == '__main__':
    unittest.main()

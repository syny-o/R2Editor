import unittest

from data_manager.coverage_data import (
    apply_file_references,
    toggle_script_reference,
)


class CoverageDataTests(unittest.TestCase):
    def test_toggle_adds_and_removes_script_path(self):
        coverage = {'req-1': []}

        self.assertTrue(
            toggle_script_reference(coverage, 'REQ-1', 'script.par')
        )
        self.assertEqual(coverage, {'req-1': ['script.par']})

        toggle_script_reference(coverage, 'REQ-1', 'script.par')
        self.assertEqual(coverage, {'req-1': []})

    def test_toggle_ignores_unknown_requirement(self):
        coverage = {}

        self.assertFalse(
            toggle_script_reference(coverage, 'REQ-1', 'script.par')
        )

    def test_applies_physical_file_references(self):
        coverage = {'req-1': [], 'req-2': []}

        apply_file_references(
            coverage,
            {'req-1': {'first.par', 'second.par'}},
        )

        self.assertEqual(
            set(coverage['req-1']),
            {'first.par', 'second.par'},
        )
        self.assertEqual(coverage['req-2'], [])

    def test_supports_historical_sydesign_typo(self):
        coverage = {'prefix--sydesign_1': []}

        apply_file_references(
            coverage,
            {'prefix-sydesign_1': {'script.par'}},
        )

        self.assertEqual(coverage['prefix--sydesign_1'], ['script.par'])


if __name__ == '__main__':
    unittest.main()

import unittest

from data_manager.coverage.data import (
    add_reference_to_ignore,
    apply_file_references,
    coverage_counts,
    covered_references,
    ignored_references_outside_coverage,
    normalize_ignored_references,
    normalize_requirement_notes,
    remove_reference_from_ignore,
    remove_ignored_references,
    toggle_script_reference,
    uncovered_references,
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

    def test_calculates_coverage_views_and_counts(self):
        coverage = {
            'req-1': ['first.par'],
            'req-2': [],
            'req-3': ['second.par', 'third.par'],
        }

        self.assertEqual(
            covered_references(coverage),
            ['req-1', 'req-3'],
        )
        self.assertEqual(uncovered_references(coverage), ['req-2'])
        self.assertEqual(coverage_counts(coverage), (2, 3))

    def test_calculates_empty_coverage(self):
        self.assertEqual(covered_references({}), [])
        self.assertEqual(uncovered_references({}), [])
        self.assertEqual(coverage_counts({}), (0, 0))

    def test_finds_ignored_references_outside_coverage(self):
        ignored = ['req-1', 'req-2', 'req-3']
        coverage = {'req-1': [], 'req-3': ['script.par']}

        self.assertEqual(
            ignored_references_outside_coverage(ignored, coverage),
            ['req-2'],
        )

    def test_removes_ignored_references_and_their_notes(self):
        ignored = ['req-1', 'req-2']
        notes = {'req-1': 'keep', 'req-2': 'remove', 'other': 'keep'}

        remove_ignored_references(ignored, notes, ['req-2', 'missing'])

        self.assertEqual(ignored, ['req-1'])
        self.assertEqual(notes, {'req-1': 'keep', 'other': 'keep'})

    def test_normalizes_ignored_references(self):
        self.assertEqual(
            normalize_ignored_references(
                ['REQ-2', 'req-1', 'REQ-1'],
            ),
            ['req-1', 'req-2'],
        )
        self.assertEqual(normalize_ignored_references(None), [])

    def test_normalizes_note_reference_keys(self):
        self.assertEqual(
            normalize_requirement_notes(
                {'REQ-1': 'first', 'Req-2': 'second'},
            ),
            {'req-1': 'first', 'req-2': 'second'},
        )
        self.assertEqual(normalize_requirement_notes(None), {})

    def test_moves_reference_from_coverage_to_ignore_list(self):
        coverage = {'req-1': ['script.par']}
        ignored = []

        changed = add_reference_to_ignore(coverage, ignored, 'REQ-1')

        self.assertTrue(changed)
        self.assertEqual(coverage, {})
        self.assertEqual(ignored, ['req-1'])
        self.assertFalse(add_reference_to_ignore(coverage, ignored, 'REQ-1'))

    def test_restores_ignored_reference_to_coverage(self):
        coverage = {}
        ignored = ['req-1']
        notes = {'req-1': 'note'}

        changed = remove_reference_from_ignore(
            coverage,
            ignored,
            notes,
            'REQ-1',
            remove_note=True,
        )

        self.assertTrue(changed)
        self.assertEqual(coverage, {'req-1': []})
        self.assertEqual(ignored, [])
        self.assertEqual(notes, {})

    def test_leaves_data_unchanged_for_reference_not_ignored(self):
        coverage = {}
        ignored = []
        notes = {'req-1': 'note'}

        changed = remove_reference_from_ignore(
            coverage,
            ignored,
            notes,
            'REQ-1',
        )

        self.assertFalse(changed)
        self.assertEqual(coverage, {})
        self.assertEqual(notes, {'req-1': 'note'})


if __name__ == '__main__':
    unittest.main()

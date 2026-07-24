import re
import unittest

from data_manager.a2l_normalizer import (
    contains_number,
    find_missing_signals,
    normalize_a2l_text,
)


class A2lNormalizerTests(unittest.TestCase):
    def test_detects_numbers(self):
        self.assertTrue(contains_number('Signal2'))
        self.assertFalse(contains_number('Signal'))

    def test_finds_missing_non_numbered_signals(self):
        missing = find_missing_signals(
            'PresentSignal',
            ['PresentSignal', 'MissingSignal', 'Generated2'],
        )

        self.assertEqual(missing, ['MissingSignal'])

    def test_normalizes_single_match_and_reports_replacement(self):
        pattern = re.compile(r'(name=)(\w+)')
        statuses = []

        text, replacements, duplicates = normalize_a2l_text(
            'name=wrong',
            {pattern: 'expected'},
            statuses.append,
        )

        self.assertEqual(text, 'name=expected')
        self.assertEqual(replacements, {'wrong': 'expected'})
        self.assertEqual(duplicates, [])
        self.assertEqual(statuses, ['Checking: <expected>'])

    def test_keeps_correct_value_when_duplicate_is_present(self):
        pattern = re.compile(r'(name=)(\w+)')

        text, replacements, duplicates = normalize_a2l_text(
            'name=wrong name=expected',
            {pattern: 'expected'},
        )

        self.assertEqual(text, 'name=wrong name=expected')
        self.assertEqual(replacements, {})
        self.assertEqual(duplicates, ['expected'])

    def test_replaces_shortest_value_when_all_duplicates_are_wrong(self):
        pattern = re.compile(r'(name=)(\w+)')

        text, replacements, duplicates = normalize_a2l_text(
            'name=longwrong name=bad',
            {pattern: 'expected'},
        )

        self.assertEqual(text, 'name=longwrong name=expected')
        self.assertEqual(replacements, {'bad': 'expected'})
        self.assertEqual(duplicates, ['expected'])


if __name__ == '__main__':
    unittest.main()

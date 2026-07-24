import re
import unittest

from file_browser.script_normalizer import normalize_script_text


class ScriptNormalizerTests(unittest.TestCase):
    def test_normalizes_matches_and_reports_replacements(self):
        pattern = re.compile(r'PbcOut[_\.]?Speed')

        text, replacements = normalize_script_text(
            'PbcOut.Speed = PbcOut_Speed',
            {pattern: 'PbcOutSpeed'},
        )

        self.assertEqual(text, 'PbcOutSpeed = PbcOutSpeed')
        self.assertEqual(
            replacements,
            [
                ('PbcOut.Speed', 'PbcOutSpeed'),
                ('PbcOut_Speed', 'PbcOutSpeed'),
            ],
        )

    def test_leaves_expected_value_unchanged(self):
        pattern = re.compile(r'PbcOutSpeed')

        text, replacements = normalize_script_text(
            'PbcOutSpeed',
            {pattern: 'PbcOutSpeed'},
        )

        self.assertEqual(text, 'PbcOutSpeed')
        self.assertEqual(replacements, [])

    def test_returns_original_text_when_nothing_matches(self):
        text, replacements = normalize_script_text(
            'unrelated',
            {re.compile(r'PbcInSpeed'): 'PbcInSpeed'},
        )

        self.assertEqual(text, 'unrelated')
        self.assertEqual(replacements, [])


if __name__ == '__main__':
    unittest.main()

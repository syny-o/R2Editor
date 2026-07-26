import sys
import unittest
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from data_manager.requirements.references import (
    changed_requirement_references,
    extract_requirement_references,
)


class RequirementReferencesTest(unittest.TestCase):
    def test_extracts_ref_and_testcase_reference(self):
        text = (
            '$REF: "REQ-1, REQ-2" $\n'
            'TESTCASE "A" REFERENCE "REQ-3" EXPECTEDRESULT 1'
        )

        self.assertEqual(
            extract_requirement_references(text),
            {'req-1', 'req-2', 'req-3'},
        )

    def test_references_are_trimmed_normalized_and_unique(self):
        text = '$REF: " Req-1,REQ-1, req-2 " $'
        self.assertEqual(
            extract_requirement_references(text),
            {'req-1', 'req-2'},
        )

    def test_changed_references_returns_added_and_removed_items(self):
        original = '$REF: "REQ-1, REQ-2" $'
        updated = '$REF: "REQ-2, REQ-3" $'

        self.assertEqual(
            changed_requirement_references(original, updated),
            {'req-1', 'req-3'},
        )

    def test_unrelated_text_has_no_references(self):
        self.assertEqual(extract_requirement_references('REFERENCE "REQ-1"'), set())


if __name__ == '__main__':
    unittest.main()

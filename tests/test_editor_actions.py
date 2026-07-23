import sys
import unittest
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from text_editor import editor_actions


class ReadOnlyTextEdit:
    def isReadOnly(self):
        return True

    def __getattr__(self, name):
        raise AssertionError(f"Read-only action accessed {name}")


class EditorActionsTest(unittest.TestCase):
    def test_mutating_actions_do_nothing_for_read_only_editor(self):
        editor = ReadOnlyTextEdit()

        editor_actions.add_new_line_indent(editor)
        editor_actions.format_text_edit(editor)
        editor_actions.indent_or_dedent(editor, "indent")
        editor_actions.toggle_comment(editor)
        editor_actions.insert_command(editor)
        editor_actions.insert_testcase(editor)
        editor_actions.insert_chapter(editor)
        editor_actions.format_assignment_at_cursor(editor)
        editor_actions.complete_special_command(editor)


if __name__ == "__main__":
    unittest.main()

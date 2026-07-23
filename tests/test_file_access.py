import stat
import sys
import unittest
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch


PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from text_editor.file_access import is_file_read_only


class FileAccessTest(unittest.TestCase):
    def test_missing_file_path_is_not_read_only(self):
        self.assertFalse(is_file_read_only(None))

    def test_windows_read_only_attribute_is_detected(self):
        file_status = SimpleNamespace(
            st_file_attributes=stat.FILE_ATTRIBUTE_READONLY,
            st_mode=stat.S_IWRITE,
        )
        with patch("text_editor.file_access.os.stat", return_value=file_status):
            self.assertTrue(is_file_read_only("locked.txt"))

    def test_windows_file_without_attribute_is_writable(self):
        file_status = SimpleNamespace(st_file_attributes=0, st_mode=0)
        with patch("text_editor.file_access.os.stat", return_value=file_status):
            self.assertFalse(is_file_read_only("writable.txt"))

    def test_mode_is_used_when_windows_attributes_are_unavailable(self):
        writable = SimpleNamespace(st_mode=stat.S_IWRITE)
        read_only = SimpleNamespace(st_mode=stat.S_IREAD)

        with patch("text_editor.file_access.os.stat", return_value=writable):
            self.assertFalse(is_file_read_only("writable.txt"))
        with patch("text_editor.file_access.os.stat", return_value=read_only):
            self.assertTrue(is_file_read_only("locked.txt"))


if __name__ == "__main__":
    unittest.main()

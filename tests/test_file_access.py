import stat
import sys
import tempfile
import unittest
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch


PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from text_editor.documents.file_access import (
    is_file_read_only,
    is_supported_document,
    read_text_file,
    set_file_read_only,
    write_text_file,
)


class FileAccessTest(unittest.TestCase):
    def test_supported_document_suffix_is_case_insensitive(self):
        self.assertTrue(is_supported_document('script.PAR'))
        self.assertTrue(is_supported_document(Path('script.py')))
        self.assertFalse(is_supported_document('script.json'))
        self.assertFalse(is_supported_document(None))

    def test_text_file_round_trip(self):
        with tempfile.TemporaryDirectory() as directory:
            file_path = Path(directory) / 'script.par'
            write_text_file(file_path, 'CHAPTER "Example"')
            self.assertEqual(read_text_file(file_path), 'CHAPTER "Example"')

    def test_missing_file_path_is_not_read_only(self):
        self.assertFalse(is_file_read_only(None))

    def test_windows_read_only_attribute_is_detected(self):
        file_status = SimpleNamespace(
            st_file_attributes=stat.FILE_ATTRIBUTE_READONLY,
            st_mode=stat.S_IWRITE,
        )
        with patch(
            "text_editor.documents.file_access.os.stat",
            return_value=file_status,
        ):
            self.assertTrue(is_file_read_only("locked.txt"))

    def test_windows_file_without_attribute_is_writable(self):
        file_status = SimpleNamespace(st_file_attributes=0, st_mode=0)
        with patch(
            "text_editor.documents.file_access.os.stat",
            return_value=file_status,
        ):
            self.assertFalse(is_file_read_only("writable.txt"))

    def test_mode_is_used_when_windows_attributes_are_unavailable(self):
        writable = SimpleNamespace(st_mode=stat.S_IWRITE)
        read_only = SimpleNamespace(st_mode=stat.S_IREAD)

        with patch(
            "text_editor.documents.file_access.os.stat",
            return_value=writable,
        ):
            self.assertFalse(is_file_read_only("writable.txt"))
        with patch(
            "text_editor.documents.file_access.os.stat",
            return_value=read_only,
        ):
            self.assertTrue(is_file_read_only("locked.txt"))

    def test_set_file_read_only_uses_expected_mode(self):
        with patch("text_editor.documents.file_access.os.chmod") as chmod:
            set_file_read_only("script.par", True)
            chmod.assert_called_once_with("script.par", stat.S_IREAD)

        with patch("text_editor.documents.file_access.os.chmod") as chmod:
            set_file_read_only("script.par", False)
            chmod.assert_called_once_with("script.par", stat.S_IWRITE)


if __name__ == "__main__":
    unittest.main()

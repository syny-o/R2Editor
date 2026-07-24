import tempfile
import unittest
from pathlib import Path

from file_browser.file_operations import (
    create_document,
    delete_path,
    duplicate_file,
    rename_path,
)


class FileOperationsTests(unittest.TestCase):
    def setUp(self):
        self.temp_directory = tempfile.TemporaryDirectory()
        self.root = Path(self.temp_directory.name)

    def tearDown(self):
        self.temp_directory.cleanup()

    def test_create_document_adds_default_suffix(self):
        path = create_document(self.root, 'script')

        self.assertEqual(path.name, 'script.par')
        self.assertTrue(path.is_file())

    def test_create_document_preserves_supported_suffix(self):
        path = create_document(self.root, 'script.py')

        self.assertEqual(path.name, 'script.py')

    def test_duplicate_file_copies_content(self):
        source = self.root / 'script.par'
        source.write_text('content', encoding='utf8')

        duplicate = duplicate_file(source)

        self.assertEqual(duplicate.name, 'script - Copy.par')
        self.assertEqual(duplicate.read_text(encoding='utf8'), 'content')

    def test_rename_path_returns_new_path(self):
        source = self.root / 'script.par'
        source.touch()

        renamed = rename_path(source, 'renamed')

        self.assertEqual(renamed.name, 'renamed.par')
        self.assertTrue(renamed.exists())
        self.assertFalse(source.exists())

    def test_delete_path_removes_directory_tree(self):
        directory = self.root / 'folder'
        directory.mkdir()
        (directory / 'script.par').touch()

        delete_path(directory)

        self.assertFalse(directory.exists())


if __name__ == '__main__':
    unittest.main()

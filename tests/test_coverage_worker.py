import tempfile
import unittest
from pathlib import Path

from data_manager.coverage.scanner import scan_requirement_references


class CoverageWorkerTests(unittest.TestCase):
    def test_scans_par_and_txt_files_recursively(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            nested = root / 'nested'
            nested.mkdir()
            script = root / 'first.par'
            text_file = nested / 'second.txt'
            script.write_text('$REF: "REQ_1" $', encoding='utf8')
            text_file.write_text(
                '$REF: "REQ_1, REQ_2" $',
                encoding='utf8',
            )

            references = scan_requirement_references(root)

            self.assertEqual(
                references['req_1'],
                {str(script), str(text_file)},
            )
            self.assertEqual(references['req_2'], {str(text_file)})

    def test_ignores_unsupported_files(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / 'ignored.py').write_text(
                "' Satisfies: REQ_1\n",
                encoding='utf8',
            )

            self.assertEqual(scan_requirement_references(root), {})

    def test_reports_scanned_files(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            script = root / 'script.par'
            script.write_text('', encoding='utf8')
            messages = []

            scan_requirement_references(root, progress=messages.append)

            self.assertEqual(messages, [f'Checking: <{script}>'])


if __name__ == '__main__':
    unittest.main()

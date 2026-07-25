import os
import tempfile
import unittest
from datetime import datetime
from pathlib import Path

from dashboard.recent_projects import (
    project_display_text,
    project_last_modified_text,
)


class RecentProjectDisplayTests(unittest.TestCase):
    def test_includes_project_path_and_last_modification_time(self):
        with tempfile.TemporaryDirectory() as directory:
            project_path = Path(directory) / "project.json"
            project_path.touch()
            timestamp = datetime(2026, 7, 25, 14, 32).timestamp()
            os.utime(project_path, (timestamp, timestamp))

            display_text = project_display_text(project_path)

        self.assertEqual(
            display_text,
            f"{project_path} — 25.07.2026 14:32",
        )

    def test_marks_missing_project_file(self):
        project_path = Path("missing-project.json")

        self.assertEqual(
            project_display_text(project_path),
            f"{project_path} — File not found",
        )

    def test_returns_last_modification_as_separate_column_value(self):
        with tempfile.TemporaryDirectory() as directory:
            project_path = Path(directory) / "project.json"
            project_path.touch()
            timestamp = datetime(2026, 7, 25, 14, 32).timestamp()
            os.utime(project_path, (timestamp, timestamp))

            modified_text = project_last_modified_text(project_path)

        self.assertEqual(modified_text, "25.07.2026 14:32")


if __name__ == "__main__":
    unittest.main()

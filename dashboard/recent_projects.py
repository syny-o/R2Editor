from datetime import datetime
from pathlib import Path


def project_last_modified_text(project_path):
    path = Path(project_path)
    try:
        modified = datetime.fromtimestamp(path.stat().st_mtime)
    except OSError:
        return "File not found"

    return modified.strftime("%d.%m.%Y %H:%M")


def project_display_text(project_path):
    return f"{Path(project_path)} — {project_last_modified_text(project_path)}"

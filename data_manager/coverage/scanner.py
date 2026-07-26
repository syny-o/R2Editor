import os
from pathlib import Path

from data_manager.requirements.references import extract_requirement_references


def scan_requirement_references(project_path, progress=None):
    references_by_file = {}
    for root, _, files in os.walk(project_path):
        for filename in files:
            if not filename.endswith(('.par', '.txt')):
                continue

            file_path = Path(root) / filename
            if progress:
                progress(f'Checking: <{file_path}>')

            try:
                text = _read_script(file_path)
            except Exception as exception:
                _write_error_log(file_path, exception)
                continue

            for reference in extract_requirement_references(text):
                references_by_file.setdefault(reference, set()).add(
                    str(file_path)
                )
    return references_by_file


def _read_script(file_path):
    try:
        return file_path.read_text(encoding='utf8')
    except UnicodeDecodeError:
        return file_path.read_text(encoding='latin1')


def _write_error_log(file_path, exception):
    Path('error_log_requirement_coverage.txt').write_text(
        f'{exception}\n{file_path}',
        encoding='utf8',
    )

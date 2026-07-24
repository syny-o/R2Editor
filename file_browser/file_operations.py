import os
import shutil
import stat
from pathlib import Path


DEFAULT_DOCUMENT_SUFFIX = '.par'
SUPPORTED_NEW_DOCUMENT_SUFFIXES = ('.par', '.txt', '.py')


def delete_path(path):
    path = Path(path)
    if path.is_dir():
        shutil.rmtree(path, onerror=_remove_read_only)
    else:
        _make_writable(path)
        path.unlink()


def duplicate_file(path):
    path = Path(path)
    duplicate_path = path.with_name(f'{path.stem} - Copy{path.suffix}')
    shutil.copyfile(path, duplicate_path)
    return duplicate_path


def rename_path(path, new_stem):
    path = Path(path)
    renamed_path = path.with_stem(new_stem)
    path.rename(renamed_path)
    return renamed_path


def create_document(parent, name):
    document_path = Path(parent) / name
    if not str(document_path).endswith(SUPPORTED_NEW_DOCUMENT_SUFFIXES):
        document_path = Path(f'{document_path}{DEFAULT_DOCUMENT_SUFFIX}')
    document_path.touch(exist_ok=False)
    return document_path


def _remove_read_only(function, path, exception_info):
    _make_writable(path)
    os.unlink(path)


def _make_writable(path):
    os.chmod(path, stat.S_IWRITE)

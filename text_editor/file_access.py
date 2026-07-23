import os
import stat


SUPPORTED_DOCUMENT_SUFFIXES = frozenset({
    '.par',
    '.py',
    '.con',
    '.xml',
    '.txt',
    '.map',
})


def is_supported_document(file_path):
    return file_path is not None and (
        os.path.splitext(str(file_path))[1].lower()
        in SUPPORTED_DOCUMENT_SUFFIXES
    )


def read_text_file(file_path):
    with open(file_path, 'r') as input_file:
        return input_file.read()


def write_text_file(file_path, text):
    with open(file_path, 'w') as output_file:
        output_file.write(text)


def is_file_read_only(file_path):
    if file_path is None:
        return False

    file_status = os.stat(file_path)
    windows_attributes = getattr(file_status, "st_file_attributes", None)
    if windows_attributes is not None:
        return bool(windows_attributes & stat.FILE_ATTRIBUTE_READONLY)

    return not bool(file_status.st_mode & stat.S_IWRITE)


def set_file_read_only(file_path, read_only):
    mode = stat.S_IREAD if read_only else stat.S_IWRITE
    os.chmod(file_path, mode)

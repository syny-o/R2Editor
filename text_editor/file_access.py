import os
import stat


def is_file_read_only(file_path):
    if file_path is None:
        return False

    file_status = os.stat(file_path)
    windows_attributes = getattr(file_status, "st_file_attributes", None)
    if windows_attributes is not None:
        return bool(windows_attributes & stat.FILE_ATTRIBUTE_READONLY)

    return not bool(file_status.st_mode & stat.S_IWRITE)

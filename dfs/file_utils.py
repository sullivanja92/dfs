import os


def file_exists(file: str) -> bool:
    """
    This function checks whether a file at a given path currently exists.

    :param file: the path to the file
    :return: a bool indicating whether the file exists
    """
    return os.path.isfile(file)


def get_extension(file_path: str) -> str:
    """
    Returns the lowercase extension of a file at a specified path.

    :param file_path: the path to the file
    :return: the lowercase file extension
    """
    if file_path is None or file_path == '':
        raise ValueError('File path cannot be none or empty')
    return os.path.splitext(file_path)[1].replace('.', '').lower()

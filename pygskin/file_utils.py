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
    Returns the extension of a file at a specified path.

    :param file_path: the path to the file
    :return: the file extension
    """
    return os.path.splitext(file_path)[1].lower()

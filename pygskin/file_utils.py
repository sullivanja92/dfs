import os


def remove_file(file: str) -> None:
    """
    Deletes a file from the file system.

    :param file: the path to the file to delete
    :return: None
    """
    os.remove(file)


def try_remove_file(file: str) -> bool:
    """
    Tries to delete a file from the file system, returning a bool indicating if the file was deleted.

    :param file: the path to the file to delete
    :return: a bool indicating if the file was deleted
    """
    try:
        remove_file(file)
        return True
    except OSError:
        return False


def dir_exists(directory: str) -> bool:
    """
    This function checks whether a directory at a given path currently exists.

    :param directory: the path of the directory
    :return: a bool indicating whether the directory exists
    """
    return os.path.isdir(directory)


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

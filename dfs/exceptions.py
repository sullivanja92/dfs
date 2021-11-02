class InvalidDataFrameException(Exception):
    """
    An exception used to indicate that an optimizer dataframe is invalid.
    """

    def __init__(self, message: str):
        """
        :param message: the exception message.
        """
        self.message = message

    def __str__(self):
        return f"InvalidDataFrameException: {self.message}"


class UnsolvableLineupException(Exception):
    """
    An exception used to indicate that an optimized lineup may not be generated under the current constraints.
    """

    def __init__(self, message: str):
        """
        :param message: the exception message.
        """
        self.message = message

    def __str__(self):
        return f"UnsolvableLineupException: {self.message}"


class InvalidConstraintException(Exception):
    """
    An exception used to indicate that a lineup constraint is invalid.
    """

    def __init__(self, message: str):
        """
        :param message: the exception message.
        """
        self.message = message

    def __str__(self):
        return f"InvalidConstraintException: {self.message}"

class InvalidDataFrameException(Exception):

    def __init__(self, message: str):
        self.message = message

    def __str__(self):
        return f"InvalidDataFrameException: {self.message}"


class UnsolvableLineupException(Exception):

    def __init__(self, message: str):
        self.message = message

    def __str__(self):
        return f"UnsolvableLineupException: {self.message}"


class InvalidConstraintException(Exception):

    def __init__(self, message: str):
        self.message = message

    def __str__(self):
        return f"InvalidConstraintException: {self.message}"

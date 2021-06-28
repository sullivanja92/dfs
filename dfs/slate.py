from enum import Enum
from typing import Callable


class Slate(Enum):
    """
    Enumeration of game slates that may be included in lineup optimization.
    """

    ALL = 0
    SUNDAY = 1
    SUNDAY_AND_MONDAY = 2
    SUNDAY_EARLY = 3
    SUNDAY_EARLY_AND_LATE = 4
    MONDAY = 5

    def filter_function(self) -> Callable:
        """
        Returns a lambda that may be used to filter the player stats dataframe by a particular game slate.

        :return: A lambda that may be used to filter the stats dataframe.
        """
        return {
            0: lambda x, y: True,
            1: lambda x, y: x[y].weekday() == 6,
            2: lambda x, y: x[y].weekday() in [0, 6],
            3: lambda x, y: x[y].weekday() == 6 and x[y].hour == 13,
            4: lambda x, y: x[y].weekday() == 6 and x[y].hour in [13, 16],
            5: lambda x, y: x[y].weekday() == 0
        }.get(self.value)

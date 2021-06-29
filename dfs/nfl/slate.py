from typing import Callable

from dfs.slate import GameSlate


class NflAllGameSlate(GameSlate):
    """
    A game slate used to select all NFL games for a given week.
    """

    def name(self) -> str:
        return 'all'

    def filter_function(self) -> Callable:
        return lambda x, y, *_: True


class NflSundayGameSlate(GameSlate):
    """
    A game slate used to select Sunday NFL games for a given week.
    """

    def name(self) -> str:
        return 'sunday'

    def filter_function(self) -> Callable:
        return lambda x, y, *_: x[y].weekday() == 6


class NflSundayAndMondayGameSlate(GameSlate):
    """
    A game slate used to select Sunday and Monday NFL games for a given week.
    """

    def name(self) -> str:
        return 'sunday_and_monday'

    def filter_function(self) -> Callable:
        return lambda x, y, *_: x[y].weekday() in [0, 6]


class NflSundayEarlyGameSlate(GameSlate):
    """
    A game slate used to select Sunday early (1:00 PM EST) NFL games for a given week.
    """

    def name(self) -> str:
        return 'sunday_early'

    def filter_function(self) -> Callable:
        return lambda x, y, *_: x[y].weekday() == 6 and x[y].hour == 13


class NflSundayEarlyAndLateGameSlate(GameSlate):
    """
    A game slate used to select Sunday early and late (1:00 PM and 4:00 PM) NFL games for a given week.
    """

    def name(self) -> str:
        return 'sunday_early_and_late'

    def filter_function(self) -> Callable:
        return lambda x, y, *_: x[y].weekday() == 6 and x[y].hour in [13, 16]


class NflMondayGameSlate(GameSlate):
    """
    A game slate used to select Monday NFL games for a given week.
    """

    def name(self) -> str:
        return 'monday'

    def filter_function(self) -> Callable:
        return lambda x, y, *_: x[y].weekday() == 0


class NflMondayAndThursdayGameSlate(GameSlate):
    """
    A game slate used to select Monday (week n) and Thursday (week n+1) NFL games for a given week (n).
    """

    def name(self) -> str:
        return 'monday_and_thursday'

    def filter_function(self) -> Callable:
        return lambda x, y, week_col, weeks: (x[week_col] == weeks[0] and x[y].weekday() == 0) or (x[week_col] == weeks[1] and x[y].weekday() == 3)

from datetime import datetime, time
from enum import Enum


class ScheduleType(Enum):  # TODO: add support for custom schedule types
    """
    A class that enumerates various fantasy football site schedules.
    This is provided to the optimizer to control which games and players to include in optimization.

    Enum values are mappings of weekday number (Monday zero-based) to game times.
    """
    ALL = {
        x: [] for x in range(7)
    }
    SUNDAY_ALL = {
        6: []
    }
    SUNDAY_EARLY = {
        6: [time(13, 0, 0, 0)]
    }
    SUNDAY_EARLY_AND_LATE = {
        6: [
            time(13, 0, 0, 0),
            time(16, 5, 0, 0),
            time(16, 25, 0, 0)
        ]
    }
    SUNDAY_LATE = {
        6: [
            time(16, 5, 0, 0),
            time(16, 25, 0, 0)
        ]
    }
    SUNDAY_LATE_AND_NIGHT = {
        6: [
            time(16, 5, 0, 0),
            time(16, 25, 0, 0),
            time(20, 20, 0, 0)
        ]
    }
    SUNDAY_NIGHT = {
        6: [
            time(20, 20, 0, 0)
        ]
    }
    SUNDAY_AND_MONDAY = {
        6: [],
        0: []
    }
    MONDAY = {
        0: []
    }
    THURSDAY = {
        3: []
    }

    def matches(self, dt: datetime) -> bool:
        """
        Determine whether a given datetime matches the schedule type. This is determined using the enum value.

        :param dt: The datetime to check for match
        :return: a bool indicating whether the datetime matches the schedule type.
        """
        if dt is None:
            return False
        if dt.weekday() in self.value:
            times = self.value[dt.weekday()]
            if len(times) == 0 or dt.time() in times:  # zero-length time list will indicate all times included
                return True
        return False

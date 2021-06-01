import re
from typing import Optional


QB = 'QB'
RB = 'RB'
WR = 'WR'
TE = 'TE'
DST = 'DST'


def normalize_position(position: str) -> Optional[str]:
    """
    Normalizes a position string and returns the normalized result.

    :param position: The position string to be normalized.
    :return: The normalized position string.
    """
    if position is None:
        return None
    normalized = position.upper()  # uppercase
    normalized = re.sub(r'\W|_', '', normalized)  # remove non-word characters
    if normalized in ('QB', 'QUARTERBACK'):
        return QB
    elif normalized in ('RB', 'RUNNINGBACK'):
        return RB
    elif normalized in ('WR', 'WIDERECEIVER'):
        return WR
    elif normalized in ('TE', 'TIGHTEND'):
        return TE
    elif normalized in ('DST', 'DEFENSE', 'DEF', 'DEFENSESPECIALTEAMS', 'D'):
        return DST
    else:
        return None

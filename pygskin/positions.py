from enum import Enum
import re


class Position(Enum):
    QB = 'QB'
    RB = 'RB'
    WR = 'WR'
    TE = 'TE'
    DST = 'DST'


def normalize_position(position):
    if position is None:
        return None
    normalized = position.upper()  # uppercase
    normalized = re.sub(r'\W|_', '', normalized)  # remove non-word characters
    if normalized in ('QB', 'QUARTERBACK'):
        return Position.QB
    elif normalized in ('RB', 'RUNNINGBACK'):
        return Position.RB
    elif normalized in ('WR', 'WIDERECEIVER'):
        return Position.WR
    elif normalized in ('TE', 'TIGHTEND'):
        return Position.TE
    elif normalized in ('DST', 'DEFENSE', 'DEF', 'DEFENSESPECIALTEAMS', 'D'):
        return Position.DST
    else:
        return None

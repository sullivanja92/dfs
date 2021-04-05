import re
from enum import Enum
from typing import Optional


class Position(Enum):
    QB = 'QB'
    RB = 'RB'
    WR = 'WR'
    TE = 'TE'
    DST = 'DST'

    def __str__(self):
        return self.value


def normalize_position(position: str) -> Optional[Position]:
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

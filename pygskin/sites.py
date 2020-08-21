from enum import Enum
from typing import Dict, Tuple

from pygskin import positions


class Site(Enum):
    """
    Fantasy football site enumeration. Enums contain site-specific information for lineup generation.
    """
    DRAFTKINGS = {
        'name': 'DraftKings',
        'salary_cap': 50_000,
        'num_players': 9,
        'position_constraints': {  # TODO: add flex
            positions.Position.QB: (1, 1),
            positions.Position.RB: (2, 3),
            positions.Position.WR: (3, 4),
            positions.Position.TE: (1, 2),
            positions.Position.DST: (1, 1)
        }
    }
    FANDUEL = {
        'name': 'FanDuel',
        'salary_cap': 60_000,
        'num_players': 9,
        'position_constraints': {
            positions.Position.QB: (1, 1),
            positions.Position.RB: (2, 3),
            positions.Position.WR: (3, 4),
            positions.Position.TE: (1, 2),
            positions.Position.DST: (1, 1)
        }
    }

    def name(self) -> str:
        """
        Returns the name of the site.

        :return: The site name.
        """
        return self.value['name']

    def salary_cap(self) -> int:
        """
        Returns the site's salary cap.

        :return: The salary cap.
        """
        return self.value['salary_cap']

    def num_players(self) -> int:
        """
        Returns the number of players in a lineup.

        :return: The number of players.
        """
        return self.value['num_players']

    def position_constraints(self) -> Dict[positions.Position, Tuple[int, int]]:
        """
        Returns the constraints (min/max) by position. This is represented by a dict mapping position to tuple.

        :return: The dict mapping position to min/max tuple.
        """
        return self.value['position_constraints']

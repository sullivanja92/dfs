from typing import Dict, Tuple

from pygskin import positions
from pygskin.common import LineupOptimizer
from pygskin.positions import Position


class DraftKingsNflLineupOptimizer(LineupOptimizer):

    def position_constraints(self) -> Dict[positions.Position, Tuple[int, int]]:
        return {  # mapping of min/max-count tuples to position name
            Position.QB: (1, 1),
            Position.RB: (2, 3),
            Position.WR: (3, 4),
            Position.TE: (1, 2),
            Position.DST: (1, 1)
        }

    def num_players(self) -> int:
        return 9

    def salary_cap(self) -> int:
        return 50_000

    def site(self) -> str:
        return 'DraftKings'


class FanDuelNflLineupOptimizer(LineupOptimizer):

    def __init__(self, data):
        super().__init__(data)

    def position_constraints(self) -> Dict[positions.Position, Tuple[int, int]]:
        pass

    def num_players(self) -> int:
        pass

    def salary_cap(self) -> int:
        pass

    def site(self) -> str:
        return 'FanDuel'

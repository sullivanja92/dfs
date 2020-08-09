from pygskin.common import LineupOptimizer
from pygskin.positions import Position


class DraftKingsNflLineupOptimizer(LineupOptimizer):

    def position_constraints(self):
        return {  # mapping of min/max-count tuples to position name
            Position.QB: (1, 1),
            Position.RB: (2, 3),
            Position.WR: (3, 4),
            Position.TE: (1, 2),
            Position.DST: (1, 1)
        }

    def num_players(self):
        return 9

    def salary_cap(self):
        return 50_000

    def site(self):
        return 'DraftKings'


class FanDuelNflLineupOptimizer(LineupOptimizer):

    def __init__(self, data):
        super().__init__(data)

    def position_constraints(self):
        pass

    def num_players(self):
        pass

    def salary_cap(self):
        pass

    def site(self):
        return 'FanDuel'

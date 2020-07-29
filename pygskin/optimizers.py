from pygskin.common import LineupOptimizer


class DraftKingsNflLineupOptimizer(LineupOptimizer):

    def __init__(self, data):
        super().__init__(data)

    def position_constraints(self):
        return {  # mapping of min/max-count tuples to position name
            'QB': (1, 1),
            'RB': (2, 3),
            'WR': (3, 4),
            'TE': (1, 2),
            'DST': (1, 1)
        }

    def num_players(self):
        return 9

    def salary_cap(self):
        return 50_000

    def _problem_name(self):
        return 'DraftKings NFL Optimized Lineup'


class FanDuelNflLineupOptimizer(LineupOptimizer):

    def __init__(self, data):
        super().__init__(data)

    def position_constraints(self):
        pass

    def num_players(self):
        pass

    def salary_cap(self):
        pass

    def _problem_name(self):
        return 'FanDuel NFL Optimized Lineup'

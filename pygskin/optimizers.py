from pygskin.common import LineupOptimizer


class DraftKingsNflLineupOptimizer(LineupOptimizer):

    def __init__(self, data):
        super().__init__(data)

    def lineup_options(self):
        return [  # RB, WR or TE may be used for flex
            {'QB': 1, 'RB': 3, 'WR': 3, 'TE': 1, 'DST': 1},
            {'QB': 1, 'RB': 2, 'WR': 4, 'TE': 1, 'DST': 1},
            {'QB': 1, 'RB': 2, 'WR': 3, 'TE': 2, 'DST': 1}
        ]

    def salary_cap(self):
        return 50_000

    def _problem_name(self):
        return 'DraftKings NFL'


class FanDuelNflLineupOptimizer(LineupOptimizer):

    def __init__(self, data):
        super().__init__(data)

    def lineup_options(self):
        pass

    def salary_cap(self):
        pass

    def _problem_name(self):
        return 'FanDuel NFL'

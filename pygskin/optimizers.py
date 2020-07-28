from pygskin.common import LineupOptimizer


class DraftKingsNflLineupOptimizer(LineupOptimizer):

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

    def lineup_options(self):
        pass

    def salary_cap(self):
        pass

    def _problem_name(self):
        return 'FanDuel NFL'


if __name__ == '__main__':
    import pandas as pd
    df = pd.read_excel('2019_nfl_stats.xlsx')
    for i in range(0, 18):
        week_df = df[df['week'] == i]
        optimizer = DraftKingsNflLineupOptimizer()
        optimizer.set_data(week_df)
        optimizer.optimize_lineup()

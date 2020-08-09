import unittest

import pandas as pd

from pygskin.exceptions import InvalidDataFrameException
from pygskin.optimizers import DraftKingsNflLineupOptimizer


class TestDraftKingsLineupOptimizer(unittest.TestCase):

    def setUp(self):
        self.data = pd.read_excel('../2019_nfl_stats.xlsx')

    def test_draft_kings_optimizer(self):
        optimizer = DraftKingsNflLineupOptimizer(self.data[self.data['week'] == 1],
                                                 points_col='dk_points',
                                                 salary_col='dk_salary')
        lineup = optimizer.optimize_lineup()
        self.assertEqual(329.1, lineup.points)
        self.assertEqual(46000, lineup.salary)

    def test_draft_kings_optimizer_missing_column(self):
        optimizer = DraftKingsNflLineupOptimizer(self.data[self.data['week'] == 1])
        self.assertRaises(InvalidDataFrameException, lambda: optimizer.optimize_lineup())

    def test_draft_kings_optimizer_with_different_format_positions(self):
        df = self.data.copy()
        df = df[df['week'] == 2]

        def change_position(position):
            if position == 'QB':
                return 'Q.B.'
            elif position == 'RB':
                return 'Running back'
            elif position == 'WR':
                return 'Wide_receiver'
            elif position == 'TE':
                return 'TIGHTEND'
            elif position == 'DST':
                return 'D/ST'
        df['position'] = df['position'].apply(lambda x: change_position(x))
        optimizer = DraftKingsNflLineupOptimizer(df, points_col='dk_points', salary_col='dk_salary')
        lineup = optimizer.optimize_lineup()
        self.assertEqual(260.62, lineup.points)
        self.assertEqual(49300, lineup.salary)

    def test_draft_kings_optimizer_missing_positions(self):
        optimizer = DraftKingsNflLineupOptimizer(self.data[self.data['position'] != 'QB'])
        self.assertRaises(InvalidDataFrameException, lambda: optimizer.optimize_lineup())

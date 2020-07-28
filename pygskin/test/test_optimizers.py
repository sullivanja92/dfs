import pandas as pd
import unittest
from pygskin.optimizers import DraftKingsNflLineupOptimizer


class TestDraftKingsLineupOptimizer(unittest.TestCase):

    def setUp(self):
        self.data = pd.read_excel('../2019_nfl_stats.xlsx')

    def test_draft_kings_optimizer(self):
        optimizer = DraftKingsNflLineupOptimizer(self.data[self.data['week'] == 1])
        optimizer.points_col = 'dk_points'
        optimizer.salary_col = 'dk_salary'
        optimizer.optimize_lineup()

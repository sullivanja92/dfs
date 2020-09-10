import unittest

from pygskin import data
from pygskin.exceptions import InvalidDataFrameException
from pygskin.optimize import LineupOptimizer
from pygskin.sites import Site


class TestLineupOptimizer(unittest.TestCase):

    def setUp(self):
        self.data = data.load_2019_data()

    def test_set_column_labels(self):
        optimizer = LineupOptimizer(self.data[self.data['week'] == 1])
        self.assertEqual('points', optimizer.points_col)
        optimizer.points_col = 'dk_points'
        self.assertEqual('dk_points', optimizer.points_col)

    def test_optimizer_setting_missing_column(self):
        optimizer = LineupOptimizer(self.data[self.data['week'] == 1])
        with self.assertRaises(ValueError):
            optimizer.name_col = 'missing'

    def test_optimizer_setting_column_labels(self):
        optimizer = LineupOptimizer(self.data[self.data['week'] == 1])
        optimizer.points_col = 'dk_points'
        optimizer.salary_col = 'dk_salary'
        lineup = optimizer.optimize_lineup('DraftKings')
        self.assertEqual(343.4, lineup.points)
        self.assertEqual(48800, lineup.salary)

    def test_optimizer_with_invalid_site(self):
        self.assertRaises(ValueError,
                          lambda: LineupOptimizer(self.data[self.data['week'] == 1]).optimize_lineup('invalid'))

    def test_draftkings_optimizer_str_site_full(self):
        optimizer = LineupOptimizer(self.data[self.data['week'] == 1],
                                    points_col='dk_points',
                                    salary_col='dk_salary')
        lineup = optimizer.optimize_lineup('DraftKings')
        self.assertEqual(343.4, lineup.points)
        self.assertEqual(48800, lineup.salary)

    def test_draftkings_optimizer_str_site_abbreviation(self):
        optimizer = LineupOptimizer(self.data[self.data['week'] == 1],
                                    points_col='dk_points',
                                    salary_col='dk_salary')
        lineup = optimizer.optimize_lineup('DK')
        self.assertEqual(343.4, lineup.points)
        self.assertEqual(48800, lineup.salary)

    def test_fanduel_optimizer_str_site_full(self):
        optimizer = LineupOptimizer(self.data[self.data['week'] == 1],
                                    points_col='fd_points',
                                    salary_col='fd_salary')
        lineup = optimizer.optimize_lineup('FanDuel')
        self.assertEqual(277.26, lineup.points)
        self.assertEqual(56400, lineup.salary)

    def test_fanduel_optimizer_str_site_abbreviation(self):
        optimizer = LineupOptimizer(self.data[self.data['week'] == 1],
                                    points_col='fd_points',
                                    salary_col='fd_salary')
        lineup = optimizer.optimize_lineup('FD')
        self.assertEqual(277.26, lineup.points)
        self.assertEqual(56400, lineup.salary)

    def test_draft_kings_optimizer(self):
        optimizer = LineupOptimizer(self.data[self.data['week'] == 1],
                                    points_col='dk_points',
                                    salary_col='dk_salary')
        lineup = optimizer.optimize_lineup(site=Site.DRAFTKINGS)
        self.assertEqual(343.4, lineup.points)
        self.assertEqual(48800, lineup.salary)

    def test_draft_kings_optimizer_missing_column(self):
        optimizer = LineupOptimizer(self.data[self.data['week'] == 1])
        self.assertRaises(InvalidDataFrameException, lambda: optimizer.optimize_lineup(site=Site.DRAFTKINGS))

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
        optimizer = LineupOptimizer(df, points_col='dk_points', salary_col='dk_salary')
        lineup = optimizer.optimize_lineup(site=Site.DRAFTKINGS)
        self.assertEqual(290.52, lineup.points)
        self.assertEqual(49900, lineup.salary)

    def test_draft_kings_optimizer_missing_positions(self):
        optimizer = LineupOptimizer(self.data[self.data['position'] != 'QB'])
        self.assertRaises(InvalidDataFrameException, lambda: optimizer.optimize_lineup(site=Site.DRAFTKINGS))

    def test_draft_kings_optimizer_non_int_index(self):
        optimizer = LineupOptimizer(self.data.set_index('name'),
                                    points_col='dk_points',
                                    salary_col='dk_salary')
        self.assertRaises(InvalidDataFrameException, lambda: optimizer.optimize_lineup(site=Site.DRAFTKINGS))

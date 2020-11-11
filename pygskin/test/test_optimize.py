import unittest

from pygskin import data
from pygskin.exceptions import InvalidDataFrameException
from pygskin.optimize import LineupOptimizer
from pygskin.sites import Site


class TestLineupOptimizer(unittest.TestCase):

    def setUp(self):
        self.data = data.load_2019_data()

    def test_optimizer_setting_missing_column(self):
        with self.assertRaises(ValueError):
            LineupOptimizer(self.data[self.data['week'] == 1], name_col='missing')

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
        self.assertRaises(ValueError, lambda: LineupOptimizer(self.data[self.data['week'] == 1]))

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
        optimizer = LineupOptimizer(self.data[self.data['position'] != 'QB'],
                                    points_col='dk_points',
                                    salary_col='dk_salary')
        self.assertRaises(InvalidDataFrameException, lambda: optimizer.optimize_lineup(site=Site.DRAFTKINGS))

    def test_draft_kings_optimizer_non_int_index(self):
        df = self.data.copy()
        df.index = df.index.map(str)
        optimizer = LineupOptimizer(df,
                                    points_col='dk_points',
                                    salary_col='dk_salary')
        self.assertRaises(InvalidDataFrameException, lambda: optimizer.optimize_lineup(site=Site.DRAFTKINGS))

    def test_only_include_teams_constraint(self):
        optimizer = LineupOptimizer(self.data[self.data['week'] == 2],
                                    points_col='dk_points',
                                    salary_col='dk_salary')
        with self.assertRaises(ValueError):
            optimizer.only_include_teams(None)
        with self.assertRaises(ValueError):
            optimizer.only_include_teams([])
        teams = ['ATL', 'CAR', 'NO', 'TB']
        optimizer.only_include_teams(teams)
        lineup = optimizer.optimize_lineup(site='dk')
        self.assertTrue(all([x['team'] in teams for x in lineup.players]))

    def test_exclude_teams_constraint(self):
        optimizer = LineupOptimizer(self.data[self.data['week'] == 1],
                                    points_col='dk_points',
                                    salary_col='dk_salary')
        with self.assertRaises(ValueError):
            optimizer.exclude_teams(None)
        with self.assertRaises(ValueError):
            optimizer.exclude_teams([])
        teams = ['DAL', 'CAR']
        optimizer.exclude_teams(teams)  # should exclude Dak Prescott & Christian McCaffrey
        lineup = optimizer.optimize_lineup(site='dk')
        self.assertTrue(all([x['team'] not in teams for x in lineup.players]))

    def test_clear_constraints(self):
        optimizer = LineupOptimizer(self.data[self.data['week'] == 1],
                                    points_col='dk_points',
                                    salary_col='dk_salary')
        teams = ['DAL', 'CAR']
        optimizer.exclude_teams(teams)  # should exclude Dak Prescott & Christian McCaffrey
        lineup = optimizer.optimize_lineup(site='dk')
        self.assertTrue(all([x['team'] not in teams for x in lineup.players]))
        optimizer.clear_constraints()
        lineup = optimizer.optimize_lineup(site='dk')
        self.assertTrue(all([t in [x['team'] for x in lineup.players] for t in teams]))

    def test_must_include_team_constraint(self):
        optimizer = LineupOptimizer(self.data[self.data['week'] == 1],
                                    points_col='dk_points',
                                    salary_col='dk_salary')
        with self.assertRaises(ValueError):
            optimizer.must_include_team(None)
        with self.assertRaises(ValueError):
            optimizer.must_include_team('missing')
        lineup = optimizer.optimize_lineup(site='dk')
        team = 'GB'
        self.assertTrue(all([p['team'] != team for p in lineup.players]))  # lineup shouldn't include any GB player
        optimizer.must_include_team(team)
        lineup = optimizer.optimize_lineup(site='dk')
        self.assertTrue(any([p['team'] == team for p in lineup.players]))  # lineup should include GB player

    def test_include_player_constraint(self):
        pass

    def test_exclude_player_constraint(self):
        pass

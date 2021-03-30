import unittest

from pygskin import data
from pygskin.exceptions import InvalidDataFrameException, InvalidConstraintException
from pygskin.optimize import LineupOptimizer
from pygskin.sites import Site


class TestLineupOptimizer(unittest.TestCase):

    def setUp(self):
        self.data = data.load_2020_data()

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
        self.assertEqual(288.78, lineup.points)
        self.assertEqual(49100, lineup.salary)

    def test_draftkings_optimizer_str_site_abbreviation(self):
        optimizer = LineupOptimizer(self.data[self.data['week'] == 1],
                                    points_col='dk_points',
                                    salary_col='dk_salary')
        lineup = optimizer.optimize_lineup('DK')
        self.assertEqual(288.78, lineup.points)
        self.assertEqual(49100, lineup.salary)

    def test_fanduel_optimizer_str_site_full(self):
        optimizer = LineupOptimizer(self.data[self.data['week'] == 1],
                                    points_col='fd_points',
                                    salary_col='fd_salary')
        lineup = optimizer.optimize_lineup('FanDuel')
        self.assertEqual(244.68, lineup.points)
        self.assertEqual(59800, lineup.salary)

    def test_fanduel_optimizer_str_site_abbreviation(self):
        optimizer = LineupOptimizer(self.data[self.data['week'] == 1],
                                    points_col='fd_points',
                                    salary_col='fd_salary')
        lineup = optimizer.optimize_lineup('FD')
        self.assertEqual(244.68, lineup.points)
        self.assertEqual(59800, lineup.salary)

    def test_draft_kings_optimizer(self):
        optimizer = LineupOptimizer(self.data[self.data['week'] == 1],
                                    points_col='dk_points',
                                    salary_col='dk_salary')
        lineup = optimizer.optimize_lineup(site=Site.DRAFTKINGS)
        self.assertEqual(288.78, lineup.points)
        self.assertEqual(49100, lineup.salary)

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
        self.assertEqual(293.5, lineup.points)
        self.assertEqual(50000, lineup.salary)

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
        teams = ['GB', 'SEA']
        optimizer.exclude_teams(teams)  # should exclude Davante Adams and Russell Wilson
        lineup = optimizer.optimize_lineup(site='dk')
        self.assertTrue(all([x['team'] not in teams for x in lineup.players]))

    def test_clear_constraints(self):
        optimizer = LineupOptimizer(self.data[self.data['week'] == 1],
                                    points_col='dk_points',
                                    salary_col='dk_salary')
        teams = ['GB', 'SEA']
        optimizer.exclude_teams(teams)  # should exclude Davante Adams and Russell Wilson
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
        team = 'DET'
        self.assertTrue(all([p['team'] != team for p in lineup.players]))  # lineup shouldn't include any DET player
        optimizer.must_include_team(team)
        lineup = optimizer.optimize_lineup(site='dk')
        self.assertTrue(any([p['team'] == team for p in lineup.players]))  # lineup should include DET player

    def test_include_player_constraint(self):
        optimizer = LineupOptimizer(self.data[self.data['week'] == 4],
                                    points_col='dk_points',
                                    salary_col='dk_salary')
        lineup = optimizer.optimize_lineup(site='dk')
        self.assertEqual(lineup.points, 316.98)
        self.assertEqual(lineup.salary, 49700)
        # test include by name
        with self.assertRaises(InvalidConstraintException):
            optimizer.include_player(name=None)
        with self.assertRaises(InvalidConstraintException):
            optimizer.include_player(name='Missing Player')
        optimizer.include_player(name='Aaron Rodgers')
        lineup = optimizer.optimize_lineup(site='dk')
        self.assertTrue('Aaron Rodgers' in [p.name for p in lineup.players])
        self.assertEqual(lineup.points, 307.28)
        self.assertEqual(lineup.salary, 49600)
        # test include by id
        optimizer.clear_constraints()
        with self.assertRaises(InvalidConstraintException):
            optimizer.include_player(id=None)
        with self.assertRaises(InvalidConstraintException):
            optimizer.include_player(id='Missing ID')
        optimizer.include_player(id=1416)
        lineup = optimizer.optimize_lineup(site='dk')
        self.assertTrue('Aaron Rodgers' in [p.name for p in lineup.players])
        self.assertEqual(lineup.points, 307.28)
        self.assertEqual(lineup.salary, 49600)

    def test_exclude_player_constraint(self):
        optimizer = LineupOptimizer(self.data[self.data['week'] == 4],
                                    points_col='dk_points',
                                    salary_col='dk_salary')
        lineup = optimizer.optimize_lineup(site='dk')
        self.assertEqual(lineup.points, 316.98)
        self.assertEqual(lineup.salary, 49700)
        optimizer.exclude_player('Missing Player')
        lineup = optimizer.optimize_lineup(site='dk')
        self.assertEqual(lineup.points, 316.98)
        self.assertEqual(lineup.salary, 49700)
        self.assertTrue('Joe Mixon' in [p.name for p in lineup.players])
        optimizer.exclude_player('Joe Mixon')
        lineup = optimizer.optimize_lineup(site='dk')
        self.assertEqual(lineup.points, 295.08)
        self.assertEqual(lineup.salary, 50000)
        self.assertFalse('Joe Mixon' in [p.name for p in lineup.players])
        with self.assertRaises(ValueError):
            optimizer.exclude_player(None)

import tempfile
import unittest

from dfs import data
from dfs.exceptions import InvalidDataFrameException, InvalidConstraintException
from dfs.optimize import LineupOptimizer
from dfs.sites import Site


class TestLineupOptimizer(unittest.TestCase):

    def setUp(self):
        self.data = data.load_2020_data()

    # the following tests test the optimizer initializer

    def test_initialize_with_wrong_type(self):
        with self.assertRaises(ValueError):
            LineupOptimizer(data_source=56)
        with self.assertRaises(ValueError):
            LineupOptimizer(data_source=[])

    def test_initialize_with_wrong_file_ext(self):
        with self.assertRaises(ValueError):
            LineupOptimizer(data_source='./myFile.txt')

    def test_initialize_with_missing_file(self):
        with self.assertRaises(ValueError):
            LineupOptimizer(data_source='./missing_file.csv')

    def test_optimize_with_csv_file(self):
        temp = tempfile.NamedTemporaryFile(mode='w', suffix='.csv')
        data.load_2020_data(weeks=[1]).to_csv(temp.name)
        optimizer = LineupOptimizer(data_source=temp.name,
                                    points_col='dk_points',
                                    salary_col='dk_salary')
        lineup = optimizer.optimize_lineup(site='dk')
        self.assertEqual(288.78, lineup.points)
        self.assertEqual(49100, lineup.salary)
        temp.close()

    def test_optimize_with_excel_file(self):
        temp = tempfile.NamedTemporaryFile(mode='w', suffix='.xlsx')
        data.load_2020_data(weeks=[1]).to_excel(temp.name)
        optimizer = LineupOptimizer(data_source=temp.name,
                                    points_col='dk_points',
                                    salary_col='dk_salary')
        lineup = optimizer.optimize_lineup(site='dk')
        self.assertEqual(288.78, lineup.points)
        self.assertEqual(49100, lineup.salary)
        temp.close()

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

    def test_only_include_teams_constraint(self):
        optimizer = LineupOptimizer(self.data[self.data['week'] == 2],
                                    points_col='dk_points',
                                    salary_col='dk_salary')
        with self.assertRaises(ValueError):
            optimizer.set_only_include_teams(None)
        with self.assertRaises(ValueError):
            optimizer.set_only_include_teams([])
        teams = ['ATL', 'CAR', 'NO', 'TB']
        for team in teams:
            optimizer.set_max_players_from_team(0, team)
        with self.assertRaises(InvalidConstraintException):  # all teams already excluded
            optimizer.set_only_include_teams(teams)
        optimizer.clear_constraints()
        optimizer.set_only_include_teams(teams)
        lineup = optimizer.optimize_lineup(site='dk')
        self.assertTrue(all([x.team in teams for x in lineup.players]))

    def test_exclude_teams_constraint(self):
        optimizer = LineupOptimizer(self.data[self.data['week'] == 1],
                                    points_col='dk_points',
                                    salary_col='dk_salary')
        with self.assertRaises(ValueError):
            optimizer.set_exclude_teams(None)
        with self.assertRaises(ValueError):
            optimizer.set_exclude_teams([])
        teams = ['GB', 'SEA']
        optimizer.set_exclude_teams(teams)  # should exclude Davante Adams and Russell Wilson
        lineup = optimizer.optimize_lineup(site='dk')
        self.assertTrue(all([x.team not in teams for x in lineup.players]))

    def test_clear_constraints(self):
        optimizer = LineupOptimizer(self.data[self.data['week'] == 1],
                                    points_col='dk_points',
                                    salary_col='dk_salary')
        teams = ['GB', 'SEA']
        optimizer.set_exclude_teams(teams)  # should exclude Davante Adams and Russell Wilson
        lineup = optimizer.optimize_lineup(site='dk')
        self.assertTrue(all([x.team not in teams for x in lineup.players]))
        optimizer.clear_constraints()
        lineup = optimizer.optimize_lineup(site='dk')
        self.assertTrue(all([t in [x.team for x in lineup.players] for t in teams]))

    def test_must_include_team_constraint(self):
        optimizer = LineupOptimizer(self.data[self.data['week'] == 1],
                                    points_col='dk_points',
                                    salary_col='dk_salary')
        with self.assertRaises(ValueError):
            optimizer.set_must_include_team(None)
        with self.assertRaises(ValueError):
            optimizer.set_must_include_team('missing')
        lineup = optimizer.optimize_lineup(site='dk')
        team = 'DET'
        self.assertTrue(all([p.team != team for p in lineup.players]))  # lineup shouldn't include any DET player
        optimizer.set_must_include_team(team)
        lineup = optimizer.optimize_lineup(site='dk')
        self.assertTrue(any([p.team == team for p in lineup.players]))  # lineup should include DET player

    def test_include_player_constraint(self):
        optimizer = LineupOptimizer(self.data[self.data['week'] == 4],
                                    points_col='dk_points',
                                    salary_col='dk_salary')
        lineup = optimizer.optimize_lineup(site='dk')
        self.assertEqual(lineup.points, 316.98)
        self.assertEqual(lineup.salary, 49700)
        # test include by name
        with self.assertRaises(ValueError):
            optimizer.set_must_include_player(name=None)
        with self.assertRaises(ValueError):
            optimizer.set_must_include_player(name='Missing Player')
        optimizer.set_must_include_player(name='Aaron Rodgers')
        lineup = optimizer.optimize_lineup(site='dk')
        self.assertTrue('Aaron Rodgers' in [p.name for p in lineup.players])
        self.assertEqual(lineup.points, 307.28)
        self.assertEqual(lineup.salary, 49600)
        # test include by id
        optimizer.clear_constraints()
        with self.assertRaises(ValueError):
            optimizer.set_must_include_player(id=None)
        with self.assertRaises(ValueError):
            optimizer.set_must_include_player(id='Missing ID')
        optimizer.set_must_include_player(id=1416)
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
        # test include by name
        with self.assertRaises(ValueError):
            optimizer.set_exclude_player(name='Missing Player')
        self.assertTrue('Joe Mixon' in [p.name for p in lineup.players])
        optimizer.set_exclude_player(name='Joe Mixon')
        lineup = optimizer.optimize_lineup(site='dk')
        self.assertEqual(lineup.points, 295.08)
        self.assertEqual(lineup.salary, 50000)
        self.assertFalse('Joe Mixon' in [p.name for p in lineup.players])
        with self.assertRaises(ValueError):
            optimizer.set_exclude_player(name=None)
        # test include by id
        optimizer.clear_constraints()
        with self.assertRaises(ValueError):
            optimizer.set_exclude_player(id=None)
        with self.assertRaises(ValueError):
            optimizer.set_exclude_player(id='Missing ID')
        optimizer.set_exclude_player(id=1453)
        lineup = optimizer.optimize_lineup(site='dk')
        self.assertFalse('Joe Mixon' in [p.name for p in lineup.players])
        self.assertEqual(lineup.points, 295.08)
        self.assertEqual(lineup.salary, 50000)

    def test_max_from_team(self):
        optimizer = LineupOptimizer(self.data[self.data['week'] == 3],
                                    points_col='dk_points',
                                    salary_col='dk_salary')
        lineup = optimizer.optimize_lineup(site='dk')  # lineup includes two bears
        self.assertEqual(lineup.points, 314.5)
        self.assertEqual(lineup.salary, 49700)
        self.assertTrue(all(p in [player.name for player in lineup.players] for p in ['Allen Robinson', 'Jimmy Graham']))
        optimizer.set_max_players_from_team(1, 'CHI')
        lineup = optimizer.optimize_lineup(site='dk')
        self.assertEqual(lineup.points, 314.1)
        self.assertEqual(lineup.salary, 48900)
        self.assertTrue('Jimmy Graham' in [player.name for player in lineup.players])
        optimizer.clear_constraints()
        optimizer.set_max_players_from_team(0, 'CHI')
        lineup = optimizer.optimize_lineup(site='dk')
        self.assertEqual(lineup.points, 308.9)
        self.assertEqual(lineup.salary, 49800)
        self.assertFalse(any(p in [player.name for player in lineup.players] for p in ['Allen Robinson', 'Jimmy Graham']))
        optimizer.clear_constraints()
        with self.assertRaises(InvalidConstraintException):
            optimizer.set_max_players_from_team(0, 'CHI')
            optimizer.set_max_players_from_team(1, 'CHI')
        optimizer.clear_constraints()
        optimizer.set_min_players_from_team(3, 'CHI')
        with self.assertRaises(InvalidConstraintException):  # min from this team already set to greater value
            optimizer.set_max_players_from_team(2, 'CHI')
        optimizer.clear_constraints()
        with self.assertRaises(ValueError):
            optimizer.set_max_players_from_team(None, 'CHI')
        with self.assertRaises(ValueError):
            optimizer.set_max_players_from_team(-3, 'CHI')
        with self.assertRaises(ValueError):
            optimizer.set_max_players_from_team(3, None)
        with self.assertRaises(ValueError):
            optimizer.set_max_players_from_team(3, 'MISSING')

    def test_min_from_team(self):
        optimizer = LineupOptimizer(self.data[self.data['week'] == 2],
                                    points_col='dk_points',
                                    salary_col='dk_salary')
        lineup = optimizer.optimize_lineup(site='dk')
        self.assertEqual(lineup.points, 293.5)
        self.assertEqual(lineup.salary, 50_000)
        with self.assertRaises(ValueError):  # min is none
            optimizer.set_min_players_from_team(None, 'CIN')
        with self.assertRaises(ValueError):  # min is too large
            optimizer.set_min_players_from_team(100, 'CIN')
        with self.assertRaises(ValueError):  # team is none
            optimizer.set_min_players_from_team(3, None)
        with self.assertRaises(ValueError):  # team is missing
            optimizer.set_min_players_from_team(3, 'MISSING')
        optimizer.set_max_players_from_team(3, 'CIN')
        with self.assertRaises(InvalidConstraintException):  # constraints already include max that's less than min
            optimizer.set_min_players_from_team(4, 'CIN')
        optimizer.clear_constraints()
        optimizer.set_min_players_from_team(2, 'CIN')
        with self.assertRaises(InvalidConstraintException):  # min constraint for this team already included
            optimizer.set_min_players_from_team(3, 'CIN')
        optimizer.clear_constraints()
        optimizer.set_min_players_from_team(2, 'CIN')  # include at least two bengals
        lineup = optimizer.optimize_lineup(site='dk')
        self.assertEqual(sum([1 for p in lineup.players if p.team == 'CIN']), 2)

    def test_max_salary(self):
        optimizer = LineupOptimizer(self.data[self.data['week'] == 3],
                                    points_col='dk_points',
                                    salary_col='dk_salary')
        lineup = optimizer.optimize_lineup(site='dk')
        self.assertEqual(lineup.points, 314.5)
        self.assertEqual(lineup.salary, 49700)
        with self.assertRaises(ValueError):
            optimizer.set_max_salary(None)
        with self.assertRaises(ValueError):
            optimizer.set_max_salary(0)
        optimizer.set_min_salary(45_000)
        with self.assertRaises(InvalidConstraintException):  # set max that's below min
            optimizer.set_max_salary(40_000)
        optimizer.clear_constraints()
        optimizer.set_max_salary(40_000)
        lineup = optimizer.optimize_lineup(site='dk')
        self.assertLessEqual(lineup.salary, 40_000)
        self.assertEqual(lineup.points, 279.6)

    def test_min_salary(self):
        optimizer = LineupOptimizer(self.data[self.data['week'] == 4],
                                    points_col='dk_points',
                                    salary_col='dk_salary')
        lineup = optimizer.optimize_lineup(site='dk')
        self.assertEqual(lineup.points, 316.98)
        self.assertEqual(lineup.salary, 49700)
        with self.assertRaises(ValueError):
            optimizer.set_min_salary(None)
        with self.assertRaises(ValueError):
            optimizer.set_min_salary(100_000)
        optimizer.set_max_salary(45_000)
        with self.assertRaises(InvalidConstraintException):
            optimizer.set_min_salary(46_000)
        optimizer.clear_constraints()
        optimizer.set_min_salary(50_000)
        lineup = optimizer.optimize_lineup(site='dk')
        self.assertEqual(lineup.salary, 50_000)
        self.assertEqual(lineup.points, 308.26)

    def test_num_players_from_team(self):
        optimizer = LineupOptimizer(self.data[self.data['week'] == 4],
                                    points_col='dk_points',
                                    salary_col='dk_salary')
        lineup = optimizer.optimize_lineup(site='dk')
        self.assertEqual(lineup.points, 316.98)
        self.assertEqual(lineup.salary, 49700)
        with self.assertRaises(ValueError):
            optimizer.set_num_players_from_team(None, 'GB')
        with self.assertRaises(ValueError):
            optimizer.set_num_players_from_team(15, 'GB')
        with self.assertRaises(ValueError):
            optimizer.set_num_players_from_team(3, None)
        with self.assertRaises(ValueError):
            optimizer.set_num_players_from_team(3, 'MISSING')
        optimizer.set_min_players_from_team(4, 'GB')
        with self.assertRaises(InvalidConstraintException):
            optimizer.set_num_players_from_team(3, 'GB')
        optimizer.clear_constraints()
        optimizer.set_num_players_from_team(4, 'GB')
        optimizer.set_num_players_from_team(2, 'DET')
        lineup = optimizer.optimize_lineup(site='dk')
        self.assertEqual(sum([1 for p in lineup.players if p.team == 'GB']), 4)
        self.assertEqual(sum([1 for p in lineup.players if p.team == 'DET']), 2)

    def test_include_qb_receiver_stack(self):
        optimizer = LineupOptimizer(self.data[self.data['week'] == 1],
                                    points_col='dk_points',
                                    salary_col='dk_salary')
        lineup = optimizer.optimize_lineup(site='dk')
        self.assertEqual(lineup.points, 288.78)
        self.assertEqual(lineup.salary, 49100)
        with self.assertRaises(ValueError):
            optimizer.set_qb_receiver_stack(team='MISSING')
        optimizer.set_qb_receiver_stack(team='GB')
        with self.assertRaises(InvalidConstraintException):
            optimizer.set_qb_receiver_stack(team='NE')  # can't add two qb/receiver stacks
        optimizer.clear_constraints()
        optimizer.set_max_players_from_team(n=0, team='NE')
        with self.assertRaises(InvalidConstraintException):
            optimizer.set_qb_receiver_stack(team='NE')  # already excluding this team
        optimizer.clear_constraints()
        optimizer.set_qb_receiver_stack(team='NE')  # lineup should include a qb/receiver stack from patriots
        lineup = optimizer.optimize_lineup(site='dk')
        self.assertEqual(lineup.points, 261.5)
        self.assertEqual(lineup.salary, 49500)

    def test_qb_receiver_stack_specifying_position(self):
        optimizer = LineupOptimizer(self.data[self.data['week'] == 1],
                                    points_col='dk_points',
                                    salary_col='dk_salary')
        self.assertRaises(ValueError, lambda: optimizer.set_qb_receiver_stack(team='TB', position='RB'))
        optimizer.set_qb_receiver_stack(team='TB')
        lineup = optimizer.optimize_lineup(site='dk')  # lineup will include TB QB/TE stack
        self.assertEqual(262.96, lineup.points)
        self.assertEqual(48200, lineup.salary)
        tb_players = list(filter(lambda p: p.team == 'TB', lineup.players))
        self.assertTrue(tb_players[0].position == 'QB')
        self.assertTrue(tb_players[1].position == 'TE')
        optimizer.clear_constraints()
        optimizer.set_qb_receiver_stack(team='TB', position='WR')
        lineup = optimizer.optimize_lineup(site='dk')  # lineup will include TB QB/WR stack
        tb_players = list(filter(lambda p: p.team == 'TB', lineup.players))
        self.assertTrue(tb_players[0].position == 'QB')
        self.assertTrue(tb_players[1].position == 'WR')
        optimizer.clear_constraints()
        optimizer.set_qb_receiver_stack(team='BUF', position='TE')
        lineup = optimizer.optimize_lineup(site='dk')
        buf_players = list(filter(lambda p: p.team == 'BUF', lineup.players))
        self.assertTrue(buf_players[0].position == 'QB')
        self.assertTrue(buf_players[1].position == 'TE')

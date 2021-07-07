import tempfile
import unittest
from abc import ABC, abstractmethod

from dfs.nfl import data
from dfs.exceptions import InvalidConstraintException, InvalidDataFrameException
from dfs.nfl.optimize import DraftKingsNflLineupOptimizer, FanDuelNflLineupOptimizer, YahooNflLineupOptimizer


class TestNflLineupOptimizer(ABC):

    @abstractmethod
    def test_initialize_with_wrong_dataframe_type(self):
        pass

    @abstractmethod
    def test_initialize_with_wrong_file_ext(self):
        pass

    @abstractmethod
    def test_initialize_with_missing_file(self):
        pass

    @abstractmethod
    def test_optimize_with_csv_file(self):
        pass

    @abstractmethod
    def test_optimize_with_excel_file(self):
        pass

    @abstractmethod
    def test_optimizer_setting_missing_column(self):
        pass

    @abstractmethod
    def test_optimizer_missing_column(self):
        pass

    @abstractmethod
    def test_optimizer_with_different_format_positions(self):
        pass

    @abstractmethod
    def test_optimizer_missing_positions(self):
        pass

    @abstractmethod
    def test_only_include_teams_constraint(self):
        pass

    @abstractmethod
    def test_only_include_teams_none_teams(self):
        pass

    @abstractmethod
    def test_only_include_teams_empty_teams(self):
        pass

    @abstractmethod
    def test_only_include_teams_already_excluded(self):
        pass

    @abstractmethod
    def test_exclude_teams(self):
        pass

    @abstractmethod
    def test_exclude_teams_none(self):
        pass

    @abstractmethod
    def test_exclude_teams_empty(self):
        pass

    @abstractmethod
    def test_clear_constraints(self):
        pass

    @abstractmethod
    def test_must_include_team(self):
        pass

    @abstractmethod
    def test_must_include_team_none(self):
        pass

    @abstractmethod
    def test_must_include_team_missing(self):
        pass

    @abstractmethod
    def test_include_player_name(self):
        pass

    @abstractmethod
    def test_include_player_none_name(self):
        pass

    @abstractmethod
    def test_include_player_missing_name(self):
        pass

    @abstractmethod
    def test_include_player_id(self):
        pass

    @abstractmethod
    def test_include_player_none_id(self):
        pass

    @abstractmethod
    def test_include_player_missing_id(self):
        pass

    @abstractmethod
    def test_exclude_player_name(self):
        pass

    @abstractmethod
    def test_exclude_player_name_none(self):
        pass

    @abstractmethod
    def test_exclude_player_name_already_included(self):
        pass

    @abstractmethod
    def test_exclude_player_name_missing(self):
        pass

    @abstractmethod
    def test_exclude_player_id(self):
        pass

    @abstractmethod
    def test_exclude_player_id_already_included(self):
        pass

    @abstractmethod
    def test_exclude_player_id_none(self):
        pass

    @abstractmethod
    def test_exclude_player_id_missing(self):
        pass

    @abstractmethod
    def test_max_from_team(self):
        pass

    @abstractmethod
    def test_max_from_team_twice(self):
        pass

    @abstractmethod
    def test_max_from_team_less_than_min(self):
        pass

    @abstractmethod
    def test_max_from_team_none_value(self):
        pass

    @abstractmethod
    def test_max_from_team_negative_value(self):
        pass

    @abstractmethod
    def test_max_from_team_none_team(self):
        pass

    @abstractmethod
    def test_max_from_team_missing_team(self):
        pass

    @abstractmethod
    def test_min_from_team(self):
        pass

    @abstractmethod
    def test_min_from_team_none_value(self):
        pass

    @abstractmethod
    def test_min_from_team_too_large(self):
        pass

    @abstractmethod
    def test_min_from_team_none_team(self):
        pass

    @abstractmethod
    def test_min_from_team_missing_team(self):
        pass

    @abstractmethod
    def test_min_from_team_already_having_max_less_than(self):
        pass

    @abstractmethod
    def test_min_from_team_twice(self):
        pass

    @abstractmethod
    def test_max_salary(self):
        pass

    @abstractmethod
    def test_max_salary_none(self):
        pass

    @abstractmethod
    def test_max_salary_zero(self):
        pass

    @abstractmethod
    def test_max_salary_already_having_min_greater_than(self):
        pass

    @abstractmethod
    def test_min_salary(self):
        pass

    @abstractmethod
    def test_min_salary_none(self):
        pass

    @abstractmethod
    def test_min_salary_too_high(self):
        pass

    @abstractmethod
    def test_min_salary_already_having_max_lower(self):
        pass

    @abstractmethod
    def test_num_players_from_team(self):
        pass

    @abstractmethod
    def test_num_players_from_team_none_value(self):
        pass

    @abstractmethod
    def test_num_players_from_team_value_too_high(self):
        pass

    @abstractmethod
    def test_num_players_from_team_none_team(self):
        pass

    @abstractmethod
    def test_num_players_from_team_missing_team(self):
        pass

    @abstractmethod
    def test_num_players_from_team_already_specified(self):
        pass

    @abstractmethod
    def test_qb_receiver_stack(self):
        pass

    @abstractmethod
    def test_qb_receiver_stack_none_team(self):
        pass

    @abstractmethod
    def test_qb_receiver_stack_missing_team(self):
        pass

    @abstractmethod
    def test_qb_receiver_stack_twice(self):
        pass

    @abstractmethod
    def test_qb_receiver_stack_team_already_excluded(self):
        pass

    @abstractmethod
    def test_qb_receiver_stack_with_position(self):
        pass

    @abstractmethod
    def test_qb_receiver_stack_non_receiver_position(self):
        pass

    @abstractmethod
    def test_qb_receiver_stack_with_num(self):
        pass

    @abstractmethod
    def test_qb_receiver_stack_num_receivers_and_position(self):
        pass

    @abstractmethod
    def test_rb_dst_stack(self):
        pass

    @abstractmethod
    def test_rb_dst_stack_none_team(self):
        pass

    @abstractmethod
    def test_rb_dst_stack_missing_team(self):
        pass

    @abstractmethod
    def test_rb_dst_stack_already_set(self):
        pass

    @abstractmethod
    def test_optimizer_without_id_col(self):
        pass

    @abstractmethod
    def test_game_slate_sunday(self):
        pass

    @abstractmethod
    def test_game_slate_sunday_early(self):
        pass

    @abstractmethod
    def test_game_slate_sunday_early_and_late(self):
        pass

    @abstractmethod
    def test_missing_datetime_col(self):
        pass

    @abstractmethod
    def test_game_slate_sunday_and_monday(self):
        pass

    @abstractmethod
    def test_game_slate_already_included(self):
        pass

    @abstractmethod
    def test_flex_position(self):
        pass

    @abstractmethod
    def test_slate_monday(self):
        pass

    @abstractmethod
    def test_slate_monday_and_thursday(self):
        pass

    @abstractmethod
    def test_slate_monday_and_thursday_not_two_weeks(self):
        pass

    @staticmethod
    def change_position(position: str) -> str:
        """
        Changes the position to a different format. Used to test normalization of different format positions.

        :param position: The position string.
        :return: The position with different format.
        """
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


class TestDraftKingsNflLineupOptimizer(unittest.TestCase, TestNflLineupOptimizer):

    def setUp(self):
        self.data = data.load_2020_data()

    def test_initialize_with_wrong_dataframe_type(self):
        self.assertRaises(ValueError, lambda: DraftKingsNflLineupOptimizer(data_source=56))
        self.assertRaises(ValueError, lambda: DraftKingsNflLineupOptimizer(data_source=[]))

    def test_initialize_with_wrong_file_ext(self):
        self.assertRaises(ValueError, lambda: DraftKingsNflLineupOptimizer(data_source='./myFile.txt'))

    def test_initialize_with_missing_file(self):
        self.assertRaises(ValueError, lambda: DraftKingsNflLineupOptimizer(data_source='./missing_file.csv'))

    def test_optimize_with_csv_file(self):
        temp = tempfile.NamedTemporaryFile(mode='w', suffix='.csv')
        data.load_2020_data(weeks=[1]).to_csv(temp.name)
        optimizer = DraftKingsNflLineupOptimizer(data_source=temp.name,
                                                 points_col='dk_points',
                                                 salary_col='dk_salary')
        lineup = optimizer.optimize_lineup()
        self.assertEqual(288.78, lineup.points)
        self.assertEqual(49100, lineup.salary)
        temp.close()

    def test_optimize_with_excel_file(self):
        temp = tempfile.NamedTemporaryFile(mode='w', suffix='.xlsx')
        data.load_2020_data(weeks=[1]).to_excel(temp.name)
        optimizer = DraftKingsNflLineupOptimizer(data_source=temp.name,
                                                 points_col='dk_points',
                                                 salary_col='dk_salary')
        lineup = optimizer.optimize_lineup()
        self.assertEqual(288.78, lineup.points)
        self.assertEqual(49100, lineup.salary)
        temp.close()

    def test_optimizer_setting_missing_column(self):
        self.assertRaises(InvalidDataFrameException,
                          lambda: DraftKingsNflLineupOptimizer(self.data[self.data['week'] == 1], name_col='missing'))

    def test_optimizer_missing_column(self):
        self.assertRaises(InvalidDataFrameException, lambda: DraftKingsNflLineupOptimizer(self.data[self.data['week'] == 1]))

    def test_optimizer_with_different_format_positions(self):
        df = self.data.copy()
        df = df[df['week'] == 2]
        df['position'] = df['position'].apply(lambda x: self.change_position(x))
        optimizer = DraftKingsNflLineupOptimizer(df, points_col='dk_points', salary_col='dk_salary')
        lineup = optimizer.optimize_lineup()
        self.assertEqual(293.5, lineup.points)
        self.assertEqual(50000, lineup.salary)

    def test_optimizer_missing_positions(self):
        optimizer = DraftKingsNflLineupOptimizer(self.data[self.data['position'] != 'QB'],
                                                 points_col='dk_points',
                                                 salary_col='dk_salary')
        self.assertRaises(InvalidDataFrameException, lambda: optimizer.optimize_lineup())

    def test_only_include_teams_constraint(self):
        optimizer = DraftKingsNflLineupOptimizer(self.data[self.data['week'] == 2],
                                                 points_col='dk_points',
                                                 salary_col='dk_salary')
        teams = ['ATL', 'CAR', 'NO', 'TB']
        optimizer.set_only_include_teams(teams=teams)
        lineup = optimizer.optimize_lineup()
        self.assertTrue(all([x.team in teams for x in lineup.players]))

    def test_only_include_teams_none_teams(self):
        optimizer = DraftKingsNflLineupOptimizer(self.data[self.data['week'] == 2],
                                                 points_col='dk_points',
                                                 salary_col='dk_salary')
        self.assertRaises(ValueError, lambda: optimizer.set_only_include_teams(teams=None))

    def test_only_include_teams_empty_teams(self):
        optimizer = DraftKingsNflLineupOptimizer(self.data[self.data['week'] == 2],
                                                 points_col='dk_points',
                                                 salary_col='dk_salary')
        self.assertRaises(ValueError, lambda: optimizer.set_only_include_teams(teams=[]))

    def test_only_include_teams_already_excluded(self):
        optimizer = DraftKingsNflLineupOptimizer(self.data[self.data['week'] == 2],
                                                 points_col='dk_points',
                                                 salary_col='dk_salary')
        teams = ['ATL', 'CAR', 'NO', 'TB']
        for team in teams:
            optimizer.set_max_players_from_team(0, team)
        self.assertRaises(InvalidConstraintException, lambda: optimizer.set_only_include_teams(teams=teams))

    def test_exclude_teams(self):
        optimizer = DraftKingsNflLineupOptimizer(self.data[self.data['week'] == 1],
                                                 points_col='dk_points',
                                                 salary_col='dk_salary')
        teams = ['GB', 'SEA']
        optimizer.set_exclude_teams(teams)  # should exclude Davante Adams and Russell Wilson
        lineup = optimizer.optimize_lineup()
        self.assertTrue(all([x.team not in teams for x in lineup.players]))

    def test_exclude_teams_none(self):
        optimizer = DraftKingsNflLineupOptimizer(self.data[self.data['week'] == 1],
                                                 points_col='dk_points',
                                                 salary_col='dk_salary')
        self.assertRaises(ValueError, lambda: optimizer.set_exclude_teams(teams=None))

    def test_exclude_teams_empty(self):
        optimizer = DraftKingsNflLineupOptimizer(self.data[self.data['week'] == 1],
                                                 points_col='dk_points',
                                                 salary_col='dk_salary')
        self.assertRaises(ValueError, lambda: optimizer.set_exclude_teams(teams=[]))

    def test_clear_constraints(self):
        optimizer = DraftKingsNflLineupOptimizer(self.data[self.data['week'] == 1],
                                                 points_col='dk_points',
                                                 salary_col='dk_salary')
        teams = ['GB', 'SEA']
        optimizer.set_exclude_teams(teams)
        lineup = optimizer.optimize_lineup()
        self.assertTrue(all([x.team not in teams for x in lineup.players]))
        optimizer.clear_constraints()
        lineup = optimizer.optimize_lineup()
        self.assertTrue(all([t in [x.team for x in lineup.players] for t in teams]))

    def test_must_include_team(self):
        optimizer = DraftKingsNflLineupOptimizer(self.data[self.data['week'] == 1],
                                                 points_col='dk_points',
                                                 salary_col='dk_salary')
        lineup = optimizer.optimize_lineup()
        team = 'DET'
        self.assertTrue(all([p.team != team for p in lineup.players]))  # lineup shouldn't include any DET player
        optimizer.set_must_include_team(team)
        lineup = optimizer.optimize_lineup()
        self.assertTrue(any([p.team == team for p in lineup.players]))  # lineup should include DET player

    def test_must_include_team_none(self):
        optimizer = DraftKingsNflLineupOptimizer(self.data[self.data['week'] == 1],
                                                 points_col='dk_points',
                                                 salary_col='dk_salary')
        self.assertRaises(ValueError, lambda: optimizer.set_must_include_team(None))

    def test_must_include_team_missing(self):
        optimizer = DraftKingsNflLineupOptimizer(self.data[self.data['week'] == 1],
                                                 points_col='dk_points',
                                                 salary_col='dk_salary')
        self.assertRaises(ValueError, lambda: optimizer.set_must_include_team('MISSING'))

    def test_include_player_name(self):
        optimizer = DraftKingsNflLineupOptimizer(self.data[self.data['week'] == 4],
                                                 points_col='dk_points',
                                                 salary_col='dk_salary',
                                                 id_col='id')
        optimizer.set_must_include_player(name='Aaron Rodgers')
        lineup = optimizer.optimize_lineup()
        self.assertTrue('Aaron Rodgers' in [p.name for p in lineup.players])
        self.assertEqual(lineup.points, 307.28)
        self.assertEqual(lineup.salary, 49600)

    def test_include_player_none_name(self):
        optimizer = DraftKingsNflLineupOptimizer(self.data[self.data['week'] == 4],
                                                 points_col='dk_points',
                                                 salary_col='dk_salary',
                                                 id_col='id')
        self.assertRaises(ValueError, lambda: optimizer.set_must_include_player(name=None))

    def test_include_player_missing_name(self):
        optimizer = DraftKingsNflLineupOptimizer(self.data[self.data['week'] == 4],
                                                 points_col='dk_points',
                                                 salary_col='dk_salary',
                                                 id_col='id')
        self.assertRaises(ValueError, lambda: optimizer.set_must_include_player(name='MISSING'))

    def test_include_player_id(self):
        optimizer = DraftKingsNflLineupOptimizer(self.data[self.data['week'] == 4],
                                                 points_col='dk_points',
                                                 salary_col='dk_salary',
                                                 id_col='id')
        optimizer.set_must_include_player(id=1419)
        lineup = optimizer.optimize_lineup()
        self.assertTrue('Aaron Rodgers' in [p.name for p in lineup.players])
        self.assertEqual(lineup.points, 307.28)
        self.assertEqual(lineup.salary, 49600)

    def test_include_player_none_id(self):
        optimizer = DraftKingsNflLineupOptimizer(self.data[self.data['week'] == 4],
                                                 points_col='dk_points',
                                                 salary_col='dk_salary',
                                                 id_col='id')
        self.assertRaises(ValueError, lambda: optimizer.set_must_include_player(id=None))

    def test_include_player_missing_id(self):
        optimizer = DraftKingsNflLineupOptimizer(self.data[self.data['week'] == 4],
                                                 points_col='dk_points',
                                                 salary_col='dk_salary',
                                                 id_col='id')
        self.assertRaises(ValueError, lambda: optimizer.set_must_include_player(id=9999))

    def test_exclude_player_name(self):
        optimizer = DraftKingsNflLineupOptimizer(self.data[self.data['week'] == 4],
                                                 points_col='dk_points',
                                                 salary_col='dk_salary',
                                                 id_col='id')
        optimizer.set_exclude_player(name='Joe Mixon')
        lineup = optimizer.optimize_lineup()
        self.assertEqual(lineup.points, 295.08)
        self.assertEqual(lineup.salary, 50000)
        self.assertFalse('Joe Mixon' in [p.name for p in lineup.players])

    def test_exclude_player_name_already_included(self):
        optimizer = DraftKingsNflLineupOptimizer(self.data[self.data['week'] == 4],
                                                 points_col='dk_points',
                                                 salary_col='dk_salary',
                                                 id_col='id')
        optimizer.set_must_include_player(name='Joe Mixon')
        self.assertRaises(InvalidConstraintException, lambda: optimizer.set_exclude_player(name='Joe Mixon'))

    def test_exclude_player_name_none(self):
        optimizer = DraftKingsNflLineupOptimizer(self.data[self.data['week'] == 4],
                                                 points_col='dk_points',
                                                 salary_col='dk_salary',
                                                 id_col='id')
        self.assertRaises(ValueError, lambda: optimizer.set_exclude_player(name=None))

    def test_exclude_player_name_missing(self):
        optimizer = DraftKingsNflLineupOptimizer(self.data[self.data['week'] == 4],
                                                 points_col='dk_points',
                                                 salary_col='dk_salary',
                                                 id_col='id')
        self.assertRaises(ValueError, lambda: optimizer.set_exclude_player(name='MISSING PLAYER'))

    def test_exclude_player_id(self):
        optimizer = DraftKingsNflLineupOptimizer(self.data[self.data['week'] == 4],
                                                 points_col='dk_points',
                                                 salary_col='dk_salary',
                                                 id_col='id')
        optimizer.set_exclude_player(id=1456)
        lineup = optimizer.optimize_lineup()
        self.assertEqual(lineup.points, 295.08)
        self.assertEqual(lineup.salary, 50000)
        self.assertFalse('Joe Mixon' in [p.name for p in lineup.players])

    def test_exclude_player_id_already_included(self):
        optimizer = DraftKingsNflLineupOptimizer(self.data[self.data['week'] == 4],
                                                 points_col='dk_points',
                                                 salary_col='dk_salary',
                                                 id_col='id')
        optimizer.set_must_include_player(id=1453)
        self.assertRaises(InvalidConstraintException, lambda: optimizer.set_exclude_player(id=1453))

    def test_exclude_player_id_none(self):
        optimizer = DraftKingsNflLineupOptimizer(self.data[self.data['week'] == 4],
                                                 points_col='dk_points',
                                                 salary_col='dk_salary',
                                                 id_col='id')
        self.assertRaises(ValueError, lambda: optimizer.set_exclude_player(id=None))

    def test_exclude_player_id_missing(self):
        optimizer = DraftKingsNflLineupOptimizer(self.data[self.data['week'] == 4],
                                                 points_col='dk_points',
                                                 salary_col='dk_salary',
                                                 id_col='id')
        self.assertRaises(ValueError, lambda: optimizer.set_exclude_player(id=9999))

    def test_max_from_team(self):
        optimizer = DraftKingsNflLineupOptimizer(self.data[self.data['week'] == 3],
                                                 points_col='dk_points',
                                                 salary_col='dk_salary')
        lineup = optimizer.optimize_lineup()
        self.assertEqual(lineup.points, 314.5)
        self.assertEqual(lineup.salary, 49700)
        self.assertTrue(len([filter(lambda p: p.team == 'CHI', lineup.players)]), 2)
        optimizer.set_max_players_from_team(1, 'CHI')
        lineup = optimizer.optimize_lineup()
        self.assertEqual(lineup.points, 314.1)
        self.assertEqual(lineup.salary, 48900)
        self.assertTrue(len([filter(lambda p: p.team == 'CHI', lineup.players)]), 1)
        optimizer.clear_constraints()
        optimizer.set_max_players_from_team(0, 'CHI')
        lineup = optimizer.optimize_lineup()
        self.assertEqual(lineup.points, 308.9)
        self.assertEqual(lineup.salary, 49800)
        self.assertTrue(len([filter(lambda p: p.team == 'CHI', lineup.players)]), 0)

    def test_max_from_team_twice(self):
        optimizer = DraftKingsNflLineupOptimizer(self.data[self.data['week'] == 3],
                                                 points_col='dk_points',
                                                 salary_col='dk_salary')
        with self.assertRaises(InvalidConstraintException):
            optimizer.set_max_players_from_team(0, 'CHI')
            optimizer.set_max_players_from_team(1, 'CHI')

    def test_max_from_team_less_than_min(self):
        optimizer = DraftKingsNflLineupOptimizer(self.data[self.data['week'] == 3],
                                                 points_col='dk_points',
                                                 salary_col='dk_salary')
        optimizer.set_min_players_from_team(3, 'CHI')
        self.assertRaises(InvalidConstraintException, lambda: optimizer.set_max_players_from_team(2, 'CHI'))

    def test_max_from_team_none_value(self):
        optimizer = DraftKingsNflLineupOptimizer(self.data[self.data['week'] == 3],
                                                 points_col='dk_points',
                                                 salary_col='dk_salary')
        self.assertRaises(ValueError, lambda: optimizer.set_max_players_from_team(None, 'CHI'))

    def test_max_from_team_negative_value(self):
        optimizer = DraftKingsNflLineupOptimizer(self.data[self.data['week'] == 3],
                                                 points_col='dk_points',
                                                 salary_col='dk_salary')
        self.assertRaises(ValueError, lambda: optimizer.set_max_players_from_team(-1, 'CHI'))

    def test_max_from_team_none_team(self):
        optimizer = DraftKingsNflLineupOptimizer(self.data[self.data['week'] == 3],
                                                 points_col='dk_points',
                                                 salary_col='dk_salary')
        self.assertRaises(ValueError, lambda: optimizer.set_max_players_from_team(3, None))

    def test_max_from_team_missing_team(self):
        optimizer = DraftKingsNflLineupOptimizer(self.data[self.data['week'] == 3],
                                                 points_col='dk_points',
                                                 salary_col='dk_salary')
        self.assertRaises(ValueError, lambda: optimizer.set_max_players_from_team(3, None))

    def test_min_from_team(self):
        optimizer = DraftKingsNflLineupOptimizer(self.data[self.data['week'] == 2],
                                                 points_col='dk_points',
                                                 salary_col='dk_salary')
        optimizer.set_min_players_from_team(2, 'CIN')
        lineup = optimizer.optimize_lineup()
        self.assertEqual(len(list(filter(lambda p: p.team == 'CIN', lineup.players))), 2)

    def test_min_from_team_none_value(self):
        optimizer = DraftKingsNflLineupOptimizer(self.data[self.data['week'] == 2],
                                                 points_col='dk_points',
                                                 salary_col='dk_salary')
        self.assertRaises(ValueError, lambda: optimizer.set_min_players_from_team(None, 'CIN'))

    def test_min_from_team_too_large(self):
        optimizer = DraftKingsNflLineupOptimizer(self.data[self.data['week'] == 2],
                                                 points_col='dk_points',
                                                 salary_col='dk_salary')
        self.assertRaises(ValueError, lambda: optimizer.set_min_players_from_team(100, 'CIN'))

    def test_min_from_team_none_team(self):
        optimizer = DraftKingsNflLineupOptimizer(self.data[self.data['week'] == 2],
                                                 points_col='dk_points',
                                                 salary_col='dk_salary')
        self.assertRaises(ValueError, lambda: optimizer.set_min_players_from_team(2, None))

    def test_min_from_team_missing_team(self):
        optimizer = DraftKingsNflLineupOptimizer(self.data[self.data['week'] == 2],
                                                 points_col='dk_points',
                                                 salary_col='dk_salary')
        self.assertRaises(ValueError, lambda: optimizer.set_min_players_from_team(2, 'MISSING'))

    def test_min_from_team_already_having_max_less_than(self):
        optimizer = DraftKingsNflLineupOptimizer(self.data[self.data['week'] == 2],
                                                 points_col='dk_points',
                                                 salary_col='dk_salary')
        optimizer.set_max_players_from_team(1, 'CIN')
        self.assertRaises(InvalidConstraintException, lambda: optimizer.set_min_players_from_team(2, 'CIN'))

    def test_min_from_team_twice(self):
        optimizer = DraftKingsNflLineupOptimizer(self.data[self.data['week'] == 2],
                                                 points_col='dk_points',
                                                 salary_col='dk_salary')
        with self.assertRaises(InvalidConstraintException):
            optimizer.set_min_players_from_team(2, 'CIN')
            optimizer.set_min_players_from_team(3, 'CIN')

    def test_max_salary(self):
        optimizer = DraftKingsNflLineupOptimizer(self.data[self.data['week'] == 3],
                                                 points_col='dk_points',
                                                 salary_col='dk_salary')
        optimizer.set_max_salary(40_000)
        lineup = optimizer.optimize_lineup()
        self.assertLessEqual(lineup.salary, 40_000)
        self.assertEqual(lineup.points, 276.9)

    def test_max_salary_none(self):
        optimizer = DraftKingsNflLineupOptimizer(self.data[self.data['week'] == 3],
                                                 points_col='dk_points',
                                                 salary_col='dk_salary')
        self.assertRaises(ValueError, lambda: optimizer.set_max_salary(None))

    def test_max_salary_zero(self):
        optimizer = DraftKingsNflLineupOptimizer(self.data[self.data['week'] == 3],
                                                 points_col='dk_points',
                                                 salary_col='dk_salary')
        self.assertRaises(ValueError, lambda: optimizer.set_max_salary(0))

    def test_max_salary_already_having_min_greater_than(self):
        optimizer = DraftKingsNflLineupOptimizer(self.data[self.data['week'] == 3],
                                                 points_col='dk_points',
                                                 salary_col='dk_salary')
        with self.assertRaises(InvalidConstraintException):
            optimizer.set_min_salary(45_000)
            optimizer.set_max_salary(40_000)

    def test_min_salary(self):
        optimizer = DraftKingsNflLineupOptimizer(self.data[self.data['week'] == 4],
                                                 points_col='dk_points',
                                                 salary_col='dk_salary')
        lineup = optimizer.optimize_lineup()
        self.assertLess(lineup.salary, 50_000)
        optimizer.set_min_salary(50_000)
        lineup = optimizer.optimize_lineup()
        self.assertEqual(lineup.salary, 50_000)
        self.assertEqual(lineup.points, 308.26)

    def test_min_salary_none(self):
        optimizer = DraftKingsNflLineupOptimizer(self.data[self.data['week'] == 4],
                                                 points_col='dk_points',
                                                 salary_col='dk_salary')
        self.assertRaises(ValueError, lambda: optimizer.set_min_salary(None))

    def test_min_salary_too_high(self):
        optimizer = DraftKingsNflLineupOptimizer(self.data[self.data['week'] == 4],
                                                 points_col='dk_points',
                                                 salary_col='dk_salary')
        self.assertRaises(ValueError, lambda: optimizer.set_min_salary(55_000))

    def test_min_salary_already_having_max_lower(self):
        optimizer = DraftKingsNflLineupOptimizer(self.data[self.data['week'] == 4],
                                                 points_col='dk_points',
                                                 salary_col='dk_salary')
        with self.assertRaises(InvalidConstraintException):
            optimizer.set_max_salary(45_000)
            optimizer.set_min_salary(46_000)

    def test_num_players_from_team(self):
        optimizer = DraftKingsNflLineupOptimizer(self.data[self.data['week'] == 4],
                                                 points_col='dk_points',
                                                 salary_col='dk_salary')
        optimizer.set_num_players_from_team(4, 'GB')
        optimizer.set_num_players_from_team(2, 'DET')
        lineup = optimizer.optimize_lineup()
        self.assertEqual(4, len(list(filter(lambda p: p.team == 'GB', lineup.players))))
        self.assertEqual(2, len(list(filter(lambda p: p.team == 'DET', lineup.players))))

    def test_num_players_from_team_none_value(self):
        optimizer = DraftKingsNflLineupOptimizer(self.data[self.data['week'] == 4],
                                                 points_col='dk_points',
                                                 salary_col='dk_salary')
        self.assertRaises(ValueError, lambda: optimizer.set_num_players_from_team(None, 'GB'))

    def test_num_players_from_team_value_too_high(self):
        optimizer = DraftKingsNflLineupOptimizer(self.data[self.data['week'] == 4],
                                                 points_col='dk_points',
                                                 salary_col='dk_salary')
        self.assertRaises(ValueError, lambda: optimizer.set_num_players_from_team(15, 'GB'))

    def test_num_players_from_team_none_team(self):
        optimizer = DraftKingsNflLineupOptimizer(self.data[self.data['week'] == 4],
                                                 points_col='dk_points',
                                                 salary_col='dk_salary')
        self.assertRaises(ValueError, lambda: optimizer.set_num_players_from_team(2, None))

    def test_num_players_from_team_missing_team(self):
        optimizer = DraftKingsNflLineupOptimizer(self.data[self.data['week'] == 4],
                                                 points_col='dk_points',
                                                 salary_col='dk_salary')
        self.assertRaises(ValueError, lambda: optimizer.set_num_players_from_team(2, 'MISSING'))

    def test_num_players_from_team_already_specified(self):
        optimizer = DraftKingsNflLineupOptimizer(self.data[self.data['week'] == 4],
                                                 points_col='dk_points',
                                                 salary_col='dk_salary')
        optimizer.set_min_players_from_team(4, 'GB')
        with self.assertRaises(InvalidConstraintException):
            optimizer.set_num_players_from_team(3, 'GB')

    def test_qb_receiver_stack(self):
        optimizer = DraftKingsNflLineupOptimizer(self.data[self.data['week'] == 1],
                                                 points_col='dk_points',
                                                 salary_col='dk_salary')
        optimizer.set_qb_receiver_stack(team='NE')
        lineup = optimizer.optimize_lineup()
        self.assertEqual(lineup.points, 261.5)
        self.assertEqual(lineup.salary, 49500)
        self.assertEqual(2, len(list(filter(lambda p: p.team == 'NE', lineup.players))))

    def test_qb_receiver_stack_none_team(self):
        optimizer = DraftKingsNflLineupOptimizer(self.data[self.data['week'] == 1],
                                                 points_col='dk_points',
                                                 salary_col='dk_salary')
        self.assertRaises(ValueError, lambda: optimizer.set_qb_receiver_stack(team=None))

    def test_qb_receiver_stack_missing_team(self):
        optimizer = DraftKingsNflLineupOptimizer(self.data[self.data['week'] == 1],
                                                 points_col='dk_points',
                                                 salary_col='dk_salary')
        self.assertRaises(ValueError, lambda: optimizer.set_qb_receiver_stack(team='MISSING'))

    def test_qb_receiver_stack_twice(self):
        optimizer = DraftKingsNflLineupOptimizer(self.data[self.data['week'] == 1],
                                                 points_col='dk_points',
                                                 salary_col='dk_salary')
        with self.assertRaises(InvalidConstraintException):
            optimizer.set_qb_receiver_stack(team='BAL')
            optimizer.set_qb_receiver_stack(team='PIT')

    def test_qb_receiver_stack_team_already_excluded(self):
        optimizer = DraftKingsNflLineupOptimizer(self.data[self.data['week'] == 1],
                                                 points_col='dk_points',
                                                 salary_col='dk_salary')
        with self.assertRaises(InvalidConstraintException):
            optimizer.set_exclude_teams(teams=['MIA'])
            optimizer.set_qb_receiver_stack(team='MIA')

    def test_qb_receiver_stack_with_position(self):
        optimizer = DraftKingsNflLineupOptimizer(self.data[self.data['week'] == 1],
                                                 points_col='dk_points',
                                                 salary_col='dk_salary')
        optimizer.set_qb_receiver_stack(team='TB')
        lineup = optimizer.optimize_lineup()  # lineup will include TB QB/TE stack
        self.assertEqual(262.96, lineup.points)
        self.assertEqual(48200, lineup.salary)
        tb_players = list(filter(lambda p: p.team == 'TB', lineup.players))
        self.assertTrue(tb_players[0].position == 'QB')
        self.assertTrue(tb_players[1].position == 'TE')
        optimizer.clear_constraints()
        optimizer.set_qb_receiver_stack(team='TB', position='WR')
        lineup = optimizer.optimize_lineup()  # lineup will include TB QB/WR stack
        tb_players = list(filter(lambda p: p.team == 'TB', lineup.players))
        self.assertTrue(tb_players[0].position == 'QB')
        self.assertTrue(tb_players[1].position == 'WR')
        optimizer.clear_constraints()
        optimizer.set_qb_receiver_stack(team='BUF', position='TE')
        lineup = optimizer.optimize_lineup()
        buf_players = list(filter(lambda p: p.team == 'BUF', lineup.players))
        self.assertTrue(buf_players[0].position == 'QB')
        self.assertTrue(buf_players[1].position == 'TE')

    def test_qb_receiver_stack_non_receiver_position(self):
        optimizer = DraftKingsNflLineupOptimizer(self.data[self.data['week'] == 1],
                                                 points_col='dk_points',
                                                 salary_col='dk_salary')
        self.assertRaises(ValueError, lambda: optimizer.set_qb_receiver_stack(team='TB', position='RB'))

    def test_qb_receiver_stack_with_num(self):
        optimizer = DraftKingsNflLineupOptimizer(self.data[self.data['week'] == 3],
                                                 points_col='dk_points',
                                                 salary_col='dk_salary')
        optimizer.set_qb_receiver_stack(team='DEN')
        lineup = optimizer.optimize_lineup()
        den_players = list(filter(lambda p: p.team == 'DEN', lineup.players))
        self.assertTrue(len(den_players) == 2)
        self.assertTrue(den_players[0].position == 'QB')
        self.assertTrue(den_players[1].position == 'TE')
        optimizer.clear_constraints()
        optimizer.set_qb_receiver_stack(team='DEN', num_receivers=2)
        lineup = optimizer.optimize_lineup()
        den_players = list(filter(lambda p: p.team == 'DEN', lineup.players))
        self.assertTrue(len(den_players) == 3)
        self.assertTrue(den_players[0].position == 'QB')
        self.assertTrue(den_players[1].position == 'TE')
        self.assertTrue(den_players[2].position == 'WR')

    def test_qb_receiver_stack_num_receivers_and_position(self):
        optimizer = DraftKingsNflLineupOptimizer(self.data[self.data['week'] == 3],
                                                 points_col='dk_points',
                                                 salary_col='dk_salary')
        self.assertRaises(ValueError,
                          lambda: optimizer.set_qb_receiver_stack(team='DEN', position='WR', num_receivers=2))

    def test_rb_dst_stack(self):
        optimizer = DraftKingsNflLineupOptimizer(self.data[self.data['week'] == 4],
                                                 points_col='dk_points',
                                                 salary_col='dk_salary')
        optimizer.set_rb_dst_stack(team='CLE')
        lineup = optimizer.optimize_lineup()
        self.assertEqual(1, len(list(filter(lambda p: p.team == 'CLE' and p.position == 'RB', lineup.players))))
        self.assertEqual(1, len(list(filter(lambda p: p.team == 'CLE' and p.position == 'DST', lineup.players))))

    def test_rb_dst_stack_none_team(self):
        optimizer = DraftKingsNflLineupOptimizer(self.data[self.data['week'] == 4],
                                                 points_col='dk_points',
                                                 salary_col='dk_salary')
        self.assertRaises(ValueError, lambda: optimizer.set_rb_dst_stack(team=None))

    def test_rb_dst_stack_missing_team(self):
        optimizer = DraftKingsNflLineupOptimizer(self.data[self.data['week'] == 4],
                                                 points_col='dk_points',
                                                 salary_col='dk_salary')
        self.assertRaises(ValueError, lambda: optimizer.set_rb_dst_stack(team='MISSING'))

    def test_rb_dst_stack_already_set(self):
        optimizer = DraftKingsNflLineupOptimizer(self.data[self.data['week'] == 4],
                                                 points_col='dk_points',
                                                 salary_col='dk_salary')
        optimizer.set_rb_dst_stack(team='BAL')
        self.assertRaises(InvalidConstraintException, lambda: optimizer.set_rb_dst_stack(team='CLE'))

    def test_optimizer_without_id_col(self):
        optimizer = DraftKingsNflLineupOptimizer(self.data[self.data['week'] == 1],
                                                 points_col='dk_points',
                                                 salary_col='dk_salary')
        self.assertRaises(ValueError, lambda: optimizer.set_must_include_player(id=1))
        self.assertRaises(ValueError, lambda: optimizer.set_exclude_player(id=1))
        lineup = optimizer.optimize_lineup()
        self.assertEqual(288.78, lineup.points)
        self.assertEqual(49100, lineup.salary)

    def test_game_slate_sunday(self):
        optimizer = DraftKingsNflLineupOptimizer(self.data[self.data['week'] == 1],
                                                 points_col='dk_points',
                                                 salary_col='dk_salary')
        lineup = optimizer.optimize_lineup()
        self.assertNotEqual(0, len(list(filter(lambda p: p.datetime.weekday() != 6, lineup.players))))
        optimizer.set_game_slate_sunday()
        lineup = optimizer.optimize_lineup()
        self.assertEqual(0, len(list(filter(lambda p: p.datetime.weekday() != 6, lineup.players))))

    def test_game_slate_sunday_early(self):
        optimizer = DraftKingsNflLineupOptimizer(self.data[self.data['week'] == 1],
                                                 points_col='dk_points',
                                                 salary_col='dk_salary')
        lineup = optimizer.optimize_lineup()
        self.assertNotEqual(0, len(list(filter(lambda p: p.datetime.hour != 13, lineup.players))))
        optimizer.set_game_slate_sunday_early()
        lineup = optimizer.optimize_lineup()
        self.assertEqual(0, len(list(filter(lambda p: p.datetime.hour != 13, lineup.players))))

    def test_game_slate_sunday_early_and_late(self):
        optimizer = DraftKingsNflLineupOptimizer(self.data[self.data['week'] == 1],
                                                 points_col='dk_points',
                                                 salary_col='dk_salary')
        lineup = optimizer.optimize_lineup()
        self.assertNotEqual(0, len(list(filter(lambda p: p.datetime.hour not in [13, 16], lineup.players))))
        optimizer.set_game_slate_sunday_early()
        lineup = optimizer.optimize_lineup()
        self.assertEqual(0, len(list(filter(lambda p: p.datetime.hour not in [13, 16], lineup.players))))

    def test_game_slate_sunday_and_monday(self):
        optimizer = DraftKingsNflLineupOptimizer(self.data[self.data['week'] == 4],
                                                 points_col='dk_points',
                                                 salary_col='dk_salary')
        lineup = optimizer.optimize_lineup()
        self.assertNotEqual(0, len(list(filter(lambda p: p.datetime.weekday() not in [0, 6], lineup.players))))
        optimizer.set_game_slate_sunday_and_monday()
        lineup = optimizer.optimize_lineup()
        self.assertEqual(0, len(list(filter(lambda p: p.datetime.weekday() not in [0, 6], lineup.players))))

    def test_missing_datetime_col(self):
        with self.assertRaises(InvalidDataFrameException):
            DraftKingsNflLineupOptimizer(self.data[self.data['week'] == 1],
                                         points_col='dk_points',
                                         salary_col='dk_salary',
                                         datetime_col='datetime_missing')

    def test_game_slate_already_included(self):
        optimizer = DraftKingsNflLineupOptimizer(self.data[self.data['week'] == 1],
                                                 points_col='dk_points',
                                                 salary_col='dk_salary')
        with self.assertRaises(InvalidConstraintException):
            optimizer.set_game_slate_sunday_early()
            optimizer.set_game_slate_sunday_early()

    def test_flex_position(self):
        optimizer = DraftKingsNflLineupOptimizer(self.data[self.data['week'] == 1],
                                                 points_col='dk_points',
                                                 salary_col='dk_salary')
        lineup = optimizer.optimize_lineup()
        self.assertEqual(4, len(list(filter(lambda x: x.position == 'WR', lineup.players))))
        self.assertEqual(1, len(list(filter(lambda x: x.lineup_position == 'FLEX', lineup.players))))
        self.assertTrue(sorted(list(filter(lambda x: x.position == 'WR', lineup.players)),
                               key=lambda x: x.datetime)[-1].lineup_position == 'FLEX')

    def test_slate_monday(self):
        optimizer = DraftKingsNflLineupOptimizer(self.data[self.data['week'] == 1],
                                                 points_col='dk_points',
                                                 salary_col='dk_salary')
        lineup = optimizer.optimize_lineup()
        self.assertNotEqual(0, len(list(filter(lambda p: p.datetime.weekday() != 0, lineup.players))))
        optimizer.set_game_slate_monday()
        lineup = optimizer.optimize_lineup()
        self.assertEqual(0, len(list(filter(lambda p: p.datetime.weekday() != 0, lineup.players))))

    def test_slate_monday_and_thursday(self):
        optimizer = DraftKingsNflLineupOptimizer(self.data[self.data['week'].isin([2, 3])],
                                                 points_col='dk_points',
                                                 salary_col='dk_salary')
        optimizer.set_game_slate_monday_and_thursday()
        lineup = optimizer.optimize_lineup()
        self.assertEqual(9, len(list(filter(lambda x: x.team in ('JAC', 'MIA', 'NO', 'LV'), lineup.players))))

    def test_slate_monday_and_thursday_not_two_weeks(self):
        optimizer = DraftKingsNflLineupOptimizer(self.data[self.data['week'] == 2],
                                                 points_col='dk_points',
                                                 salary_col='dk_salary')
        self.assertRaises(ValueError, lambda: optimizer.set_game_slate_monday_and_thursday())
        optimizer = DraftKingsNflLineupOptimizer(self.data[self.data['week'].isin([2, 3, 4])],
                                                 points_col='dk_points',
                                                 salary_col='dk_salary')
        self.assertRaises(ValueError, lambda: optimizer.set_game_slate_monday_and_thursday())


class TestFanDuelNflLineupOptimizer(unittest.TestCase, TestNflLineupOptimizer):

    def setUp(self):
        self.data = data.load_2020_data()

    def test_initialize_with_wrong_dataframe_type(self):
        self.assertRaises(ValueError, lambda: FanDuelNflLineupOptimizer(data_source=56))
        self.assertRaises(ValueError, lambda: FanDuelNflLineupOptimizer(data_source=[]))

    def test_initialize_with_wrong_file_ext(self):
        self.assertRaises(ValueError, lambda: FanDuelNflLineupOptimizer(data_source='./myFile.txt'))

    def test_initialize_with_missing_file(self):
        self.assertRaises(ValueError, lambda: FanDuelNflLineupOptimizer(data_source='./missing_file.csv'))

    def test_optimize_with_csv_file(self):
        temp = tempfile.NamedTemporaryFile(mode='w', suffix='.csv')
        data.load_2020_data(weeks=[1]).to_csv(temp.name)
        optimizer = FanDuelNflLineupOptimizer(data_source=temp.name,
                                              points_col='fd_points',
                                              salary_col='fd_salary')
        lineup = optimizer.optimize_lineup()
        self.assertEqual(244.68, lineup.points)
        self.assertEqual(59800, lineup.salary)
        temp.close()

    def test_optimize_with_excel_file(self):
        temp = tempfile.NamedTemporaryFile(mode='w', suffix='.xlsx')
        data.load_2020_data(weeks=[1]).to_excel(temp.name)
        optimizer = FanDuelNflLineupOptimizer(data_source=temp.name,
                                              points_col='fd_points',
                                              salary_col='fd_salary')
        lineup = optimizer.optimize_lineup()
        self.assertEqual(244.68, lineup.points)
        self.assertEqual(59800, lineup.salary)
        temp.close()

    def test_optimizer_setting_missing_column(self):
        self.assertRaises(InvalidDataFrameException,
                          lambda: FanDuelNflLineupOptimizer(self.data[self.data['week'] == 1], name_col='missing'))

    def test_optimizer_missing_column(self):
        self.assertRaises(InvalidDataFrameException, lambda: FanDuelNflLineupOptimizer(self.data[self.data['week'] == 1]))

    def test_optimizer_with_different_format_positions(self):
        df = self.data.copy()
        df = df[df['week'] == 2]
        df['position'] = df['position'].apply(lambda x: self.change_position(x))
        optimizer = FanDuelNflLineupOptimizer(df, points_col='fd_points', salary_col='fd_salary')
        lineup = optimizer.optimize_lineup()
        self.assertEqual(254.9, lineup.points)
        self.assertEqual(59500, lineup.salary)

    def test_optimizer_missing_positions(self):
        optimizer = FanDuelNflLineupOptimizer(self.data[self.data['position'] != 'QB'],
                                              points_col='fd_points',
                                              salary_col='fd_salary')
        self.assertRaises(InvalidDataFrameException, lambda: optimizer.optimize_lineup())

    def test_only_include_teams_constraint(self):
        optimizer = FanDuelNflLineupOptimizer(self.data[self.data['week'] == 2],
                                              points_col='fd_points',
                                              salary_col='fd_salary')
        teams = ['ATL', 'CAR', 'NO', 'TB']
        optimizer.set_only_include_teams(teams=teams)
        lineup = optimizer.optimize_lineup()
        self.assertTrue(all([x.team in teams for x in lineup.players]))

    def test_only_include_teams_none_teams(self):
        optimizer = FanDuelNflLineupOptimizer(self.data[self.data['week'] == 2],
                                              points_col='fd_points',
                                              salary_col='fd_salary')
        self.assertRaises(ValueError, lambda: optimizer.set_only_include_teams(teams=None))

    def test_only_include_teams_empty_teams(self):
        optimizer = FanDuelNflLineupOptimizer(self.data[self.data['week'] == 2],
                                              points_col='fd_points',
                                              salary_col='fd_salary')
        self.assertRaises(ValueError, lambda: optimizer.set_only_include_teams(teams=[]))

    def test_only_include_teams_already_excluded(self):
        optimizer = FanDuelNflLineupOptimizer(self.data[self.data['week'] == 2],
                                              points_col='fd_points',
                                              salary_col='fd_salary')
        teams = ['ATL', 'CAR', 'NO', 'TB']
        for team in teams:
            optimizer.set_max_players_from_team(0, team)
        self.assertRaises(InvalidConstraintException, lambda: optimizer.set_only_include_teams(teams=teams))

    def test_exclude_teams(self):
        optimizer = FanDuelNflLineupOptimizer(self.data[self.data['week'] == 1],
                                              points_col='fd_points',
                                              salary_col='fd_salary')
        teams = ['GB', 'SEA']
        optimizer.set_exclude_teams(teams)  # should exclude Davante Adams and Russell Wilson
        lineup = optimizer.optimize_lineup()
        self.assertTrue(all([x.team not in teams for x in lineup.players]))

    def test_exclude_teams_none(self):
        optimizer = FanDuelNflLineupOptimizer(self.data[self.data['week'] == 1],
                                              points_col='fd_points',
                                              salary_col='fd_salary')
        self.assertRaises(ValueError, lambda: optimizer.set_exclude_teams(teams=None))

    def test_exclude_teams_empty(self):
        optimizer = FanDuelNflLineupOptimizer(self.data[self.data['week'] == 1],
                                              points_col='fd_points',
                                              salary_col='fd_salary')
        self.assertRaises(ValueError, lambda: optimizer.set_exclude_teams(teams=[]))

    def test_clear_constraints(self):
        optimizer = FanDuelNflLineupOptimizer(self.data[self.data['week'] == 1],
                                              points_col='fd_points',
                                              salary_col='fd_salary')
        teams = ['GB', 'SEA']
        optimizer.set_exclude_teams(teams)
        lineup = optimizer.optimize_lineup()
        self.assertTrue(all([x.team not in teams for x in lineup.players]))
        optimizer.clear_constraints()
        lineup = optimizer.optimize_lineup()
        self.assertTrue(all([t in [x.team for x in lineup.players] for t in teams]))

    def test_must_include_team(self):
        optimizer = FanDuelNflLineupOptimizer(self.data[self.data['week'] == 1],
                                              points_col='fd_points',
                                              salary_col='fd_salary')
        lineup = optimizer.optimize_lineup()
        team = 'DET'
        self.assertTrue(all([p.team != team for p in lineup.players]))  # lineup shouldn't include any DET player
        optimizer.set_must_include_team(team)
        lineup = optimizer.optimize_lineup()
        self.assertTrue(any([p.team == team for p in lineup.players]))  # lineup should include DET player

    def test_must_include_team_none(self):
        optimizer = FanDuelNflLineupOptimizer(self.data[self.data['week'] == 1],
                                              points_col='fd_points',
                                              salary_col='fd_salary')
        self.assertRaises(ValueError, lambda: optimizer.set_must_include_team(None))

    def test_must_include_team_missing(self):
        optimizer = FanDuelNflLineupOptimizer(self.data[self.data['week'] == 1],
                                              points_col='fd_points',
                                              salary_col='fd_salary')
        self.assertRaises(ValueError, lambda: optimizer.set_must_include_team('MISSING'))

    def test_include_player_name(self):
        optimizer = FanDuelNflLineupOptimizer(self.data[self.data['week'] == 4],
                                              points_col='fd_points',
                                              salary_col='fd_salary',
                                              id_col='id')
        optimizer.set_must_include_player(name='Aaron Rodgers')
        lineup = optimizer.optimize_lineup()
        self.assertTrue('Aaron Rodgers' in [p.name for p in lineup.players])
        self.assertEqual(lineup.points, 265.68)
        self.assertEqual(lineup.salary, 58800)

    def test_include_player_none_name(self):
        optimizer = FanDuelNflLineupOptimizer(self.data[self.data['week'] == 4],
                                              points_col='fd_points',
                                              salary_col='fd_salary',
                                              id_col='id')
        self.assertRaises(ValueError, lambda: optimizer.set_must_include_player(name=None))

    def test_include_player_missing_name(self):
        optimizer = FanDuelNflLineupOptimizer(self.data[self.data['week'] == 4],
                                              points_col='fd_points',
                                              salary_col='fd_salary',
                                              id_col='id')
        self.assertRaises(ValueError, lambda: optimizer.set_must_include_player(name=None))

    def test_include_player_id(self):
        optimizer = FanDuelNflLineupOptimizer(self.data[self.data['week'] == 4],
                                              points_col='fd_points',
                                              salary_col='fd_salary',
                                              id_col='id')
        optimizer.set_must_include_player(id=1419)
        lineup = optimizer.optimize_lineup()
        self.assertTrue('Aaron Rodgers' in [p.name for p in lineup.players])
        self.assertEqual(lineup.points, 265.68)
        self.assertEqual(lineup.salary, 58800)

    def test_include_player_none_id(self):
        optimizer = FanDuelNflLineupOptimizer(self.data[self.data['week'] == 4],
                                              points_col='fd_points',
                                              salary_col='fd_salary',
                                              id_col='id')
        self.assertRaises(ValueError, lambda: optimizer.set_must_include_player(id=None))

    def test_include_player_missing_id(self):
        optimizer = FanDuelNflLineupOptimizer(self.data[self.data['week'] == 4],
                                              points_col='fd_points',
                                              salary_col='fd_salary',
                                              id_col='id')
        self.assertRaises(ValueError, lambda: optimizer.set_must_include_player(id=9999))

    def test_exclude_player_name(self):
        optimizer = FanDuelNflLineupOptimizer(self.data[self.data['week'] == 4],
                                              points_col='fd_points',
                                              salary_col='fd_salary',
                                              id_col='id')
        optimizer.set_exclude_player(name='Joe Mixon')
        lineup = optimizer.optimize_lineup()
        self.assertEqual(lineup.points, 260.08)
        self.assertEqual(lineup.salary, 59700)
        self.assertFalse('Joe Mixon' in [p.name for p in lineup.players])

    def test_exclude_player_name_already_included(self):
        optimizer = FanDuelNflLineupOptimizer(self.data[self.data['week'] == 4],
                                              points_col='fd_points',
                                              salary_col='fd_salary',
                                              id_col='id')
        optimizer.set_must_include_player(name='Joe Mixon')
        self.assertRaises(InvalidConstraintException, lambda: optimizer.set_exclude_player(name='Joe Mixon'))

    def test_exclude_player_name_none(self):
        optimizer = FanDuelNflLineupOptimizer(self.data[self.data['week'] == 4],
                                              points_col='fd_points',
                                              salary_col='fd_salary',
                                              id_col='id')
        self.assertRaises(ValueError, lambda: optimizer.set_exclude_player(name=None))

    def test_exclude_player_name_missing(self):
        optimizer = FanDuelNflLineupOptimizer(self.data[self.data['week'] == 4],
                                              points_col='fd_points',
                                              salary_col='fd_salary',
                                              id_col='id')
        self.assertRaises(ValueError, lambda: optimizer.set_exclude_player(name='MISSING PLAYER'))

    def test_exclude_player_id(self):
        optimizer = FanDuelNflLineupOptimizer(self.data[self.data['week'] == 4],
                                              points_col='fd_points',
                                              salary_col='fd_salary',
                                              id_col='id')
        optimizer.set_exclude_player(id=1456)
        lineup = optimizer.optimize_lineup()
        self.assertEqual(lineup.points, 260.08)
        self.assertEqual(lineup.salary, 59700)
        self.assertFalse('Joe Mixon' in [p.name for p in lineup.players])

    def test_exclude_player_id_already_included(self):
        optimizer = FanDuelNflLineupOptimizer(self.data[self.data['week'] == 4],
                                              points_col='fd_points',
                                              salary_col='fd_salary',
                                              id_col='id')
        optimizer.set_must_include_player(id=1453)
        self.assertRaises(InvalidConstraintException, lambda: optimizer.set_exclude_player(id=1453))

    def test_exclude_player_id_none(self):
        optimizer = FanDuelNflLineupOptimizer(self.data[self.data['week'] == 4],
                                              points_col='fd_points',
                                              salary_col='fd_salary',
                                              id_col='id')
        self.assertRaises(ValueError, lambda: optimizer.set_exclude_player(id=None))

    def test_exclude_player_id_missing(self):
        optimizer = FanDuelNflLineupOptimizer(self.data[self.data['week'] == 4],
                                              points_col='fd_points',
                                              salary_col='fd_salary',
                                              id_col='id')
        self.assertRaises(ValueError, lambda: optimizer.set_exclude_player(id=9999))

    def test_max_from_team(self):
        optimizer = FanDuelNflLineupOptimizer(self.data[self.data['week'] == 4],
                                              points_col='fd_points',
                                              salary_col='fd_salary')
        lineup = optimizer.optimize_lineup()
        self.assertEqual(lineup.points, 274.38)
        self.assertEqual(lineup.salary, 59000)
        self.assertTrue(len([filter(lambda p: p.team == 'DAL', lineup.players)]), 2)
        optimizer.set_max_players_from_team(1, 'DAL')
        lineup = optimizer.optimize_lineup()
        self.assertEqual(lineup.points, 272.36)
        self.assertEqual(lineup.salary, 59700)
        self.assertTrue(len([filter(lambda p: p.team == 'DAL', lineup.players)]), 1)
        optimizer.clear_constraints()
        optimizer.set_max_players_from_team(0, 'DAL')
        lineup = optimizer.optimize_lineup()
        self.assertEqual(lineup.points, 267.16)
        self.assertEqual(lineup.salary, 59700)
        self.assertTrue(len([filter(lambda p: p.team == 'DAL', lineup.players)]), 0)

    def test_max_from_team_twice(self):
        optimizer = FanDuelNflLineupOptimizer(self.data[self.data['week'] == 3],
                                              points_col='fd_points',
                                              salary_col='fd_salary')
        with self.assertRaises(InvalidConstraintException):
            optimizer.set_max_players_from_team(0, 'CHI')
            optimizer.set_max_players_from_team(1, 'CHI')

    def test_max_from_team_less_than_min(self):
        optimizer = FanDuelNflLineupOptimizer(self.data[self.data['week'] == 3],
                                              points_col='fd_points',
                                              salary_col='fd_salary')
        optimizer.set_min_players_from_team(3, 'CHI')
        self.assertRaises(InvalidConstraintException, lambda: optimizer.set_max_players_from_team(2, 'CHI'))

    def test_max_from_team_none_value(self):
        optimizer = FanDuelNflLineupOptimizer(self.data[self.data['week'] == 3],
                                              points_col='fd_points',
                                              salary_col='fd_salary')
        self.assertRaises(ValueError, lambda: optimizer.set_max_players_from_team(None, 'CHI'))

    def test_max_from_team_negative_value(self):
        optimizer = FanDuelNflLineupOptimizer(self.data[self.data['week'] == 3],
                                              points_col='fd_points',
                                              salary_col='fd_salary')
        self.assertRaises(ValueError, lambda: optimizer.set_max_players_from_team(-1, 'CHI'))

    def test_max_from_team_none_team(self):
        optimizer = FanDuelNflLineupOptimizer(self.data[self.data['week'] == 3],
                                              points_col='fd_points',
                                              salary_col='fd_salary')
        self.assertRaises(ValueError, lambda: optimizer.set_max_players_from_team(3, None))

    def test_max_from_team_missing_team(self):
        optimizer = FanDuelNflLineupOptimizer(self.data[self.data['week'] == 3],
                                              points_col='fd_points',
                                              salary_col='fd_salary')
        self.assertRaises(ValueError, lambda: optimizer.set_max_players_from_team(3, None))

    def test_min_from_team(self):
        optimizer = FanDuelNflLineupOptimizer(self.data[self.data['week'] == 2],
                                              points_col='fd_points',
                                              salary_col='fd_salary')
        optimizer.set_min_players_from_team(2, 'CIN')
        lineup = optimizer.optimize_lineup()
        self.assertEqual(len(list(filter(lambda p: p.team == 'CIN', lineup.players))), 2)

    def test_min_from_team_none_value(self):
        optimizer = FanDuelNflLineupOptimizer(self.data[self.data['week'] == 2],
                                              points_col='fd_points',
                                              salary_col='fd_salary')
        self.assertRaises(ValueError, lambda: optimizer.set_min_players_from_team(None, 'CIN'))

    def test_min_from_team_too_large(self):
        optimizer = FanDuelNflLineupOptimizer(self.data[self.data['week'] == 2],
                                              points_col='fd_points',
                                              salary_col='fd_salary')
        self.assertRaises(ValueError, lambda: optimizer.set_min_players_from_team(100, 'CIN'))

    def test_min_from_team_none_team(self):
        optimizer = FanDuelNflLineupOptimizer(self.data[self.data['week'] == 2],
                                              points_col='fd_points',
                                              salary_col='fd_salary')
        self.assertRaises(ValueError, lambda: optimizer.set_min_players_from_team(2, None))

    def test_min_from_team_missing_team(self):
        optimizer = FanDuelNflLineupOptimizer(self.data[self.data['week'] == 2],
                                              points_col='fd_points',
                                              salary_col='fd_salary')
        self.assertRaises(ValueError, lambda: optimizer.set_min_players_from_team(2, 'MISSING'))

    def test_min_from_team_already_having_max_less_than(self):
        optimizer = FanDuelNflLineupOptimizer(self.data[self.data['week'] == 2],
                                              points_col='fd_points',
                                              salary_col='fd_salary')
        optimizer.set_max_players_from_team(1, 'CIN')
        self.assertRaises(InvalidConstraintException, lambda: optimizer.set_min_players_from_team(2, 'CIN'))

    def test_min_from_team_twice(self):
        optimizer = FanDuelNflLineupOptimizer(self.data[self.data['week'] == 2],
                                              points_col='fd_points',
                                              salary_col='fd_salary')
        with self.assertRaises(InvalidConstraintException):
            optimizer.set_min_players_from_team(2, 'CIN')
            optimizer.set_min_players_from_team(3, 'CIN')

    def test_max_salary(self):
        optimizer = FanDuelNflLineupOptimizer(self.data[self.data['week'] == 3],
                                                 points_col='fd_points',
                                                 salary_col='fd_salary')
        optimizer.set_max_salary(40_000)
        lineup = optimizer.optimize_lineup()
        self.assertLessEqual(lineup.salary, 40_000)
        self.assertEqual(lineup.points, 157.2)

    def test_max_salary_none(self):
        optimizer = FanDuelNflLineupOptimizer(self.data[self.data['week'] == 3],
                                              points_col='fd_points',
                                              salary_col='fd_salary')
        self.assertRaises(ValueError, lambda: optimizer.set_max_salary(None))

    def test_max_salary_zero(self):
        optimizer = FanDuelNflLineupOptimizer(self.data[self.data['week'] == 3],
                                              points_col='fd_points',
                                              salary_col='fd_salary')
        self.assertRaises(ValueError, lambda: optimizer.set_max_salary(0))

    def test_max_salary_already_having_min_greater_than(self):
        optimizer = FanDuelNflLineupOptimizer(self.data[self.data['week'] == 3],
                                              points_col='fd_points',
                                              salary_col='fd_salary')
        with self.assertRaises(InvalidConstraintException):
            optimizer.set_min_salary(45_000)
            optimizer.set_max_salary(40_000)

    def test_min_salary(self):
        optimizer = FanDuelNflLineupOptimizer(self.data[self.data['week'] == 4],
                                              points_col='fd_points',
                                              salary_col='fd_salary')
        lineup = optimizer.optimize_lineup()
        self.assertLess(lineup.salary, 60_000)
        optimizer.set_min_salary(60_000)
        lineup = optimizer.optimize_lineup()
        self.assertEqual(lineup.salary, 60_000)

    def test_min_salary_none(self):
        optimizer = FanDuelNflLineupOptimizer(self.data[self.data['week'] == 4],
                                              points_col='fd_points',
                                              salary_col='fd_salary')
        self.assertRaises(ValueError, lambda: optimizer.set_min_salary(None))

    def test_min_salary_too_high(self):
        optimizer = FanDuelNflLineupOptimizer(self.data[self.data['week'] == 4],
                                              points_col='fd_points',
                                              salary_col='fd_salary')
        self.assertRaises(ValueError, lambda: optimizer.set_min_salary(65_000))

    def test_min_salary_already_having_max_lower(self):
        optimizer = FanDuelNflLineupOptimizer(self.data[self.data['week'] == 4],
                                              points_col='fd_points',
                                              salary_col='fd_salary')
        with self.assertRaises(InvalidConstraintException):
            optimizer.set_max_salary(55_000)
            optimizer.set_min_salary(56_000)

    def test_num_players_from_team(self):
        optimizer = FanDuelNflLineupOptimizer(self.data[self.data['week'] == 4],
                                              points_col='fd_points',
                                              salary_col='fd_salary')
        optimizer.set_num_players_from_team(4, 'GB')
        optimizer.set_num_players_from_team(2, 'DET')
        lineup = optimizer.optimize_lineup()
        self.assertEqual(4, len(list(filter(lambda p: p.team == 'GB', lineup.players))))
        self.assertEqual(2, len(list(filter(lambda p: p.team == 'DET', lineup.players))))

    def test_num_players_from_team_none_value(self):
        optimizer = FanDuelNflLineupOptimizer(self.data[self.data['week'] == 4],
                                              points_col='fd_points',
                                              salary_col='fd_salary')
        self.assertRaises(ValueError, lambda: optimizer.set_num_players_from_team(None, 'GB'))

    def test_num_players_from_team_value_too_high(self):
        optimizer = FanDuelNflLineupOptimizer(self.data[self.data['week'] == 4],
                                              points_col='fd_points',
                                              salary_col='fd_salary')
        self.assertRaises(ValueError, lambda: optimizer.set_num_players_from_team(15, 'GB'))

    def test_num_players_from_team_none_team(self):
        optimizer = FanDuelNflLineupOptimizer(self.data[self.data['week'] == 4],
                                              points_col='fd_points',
                                              salary_col='fd_salary')
        self.assertRaises(ValueError, lambda: optimizer.set_num_players_from_team(2, None))

    def test_num_players_from_team_missing_team(self):
        optimizer = FanDuelNflLineupOptimizer(self.data[self.data['week'] == 4],
                                              points_col='fd_points',
                                              salary_col='fd_salary')
        self.assertRaises(ValueError, lambda: optimizer.set_num_players_from_team(2, 'MISSING'))

    def test_num_players_from_team_already_specified(self):
        optimizer = FanDuelNflLineupOptimizer(self.data[self.data['week'] == 4],
                                              points_col='fd_points',
                                              salary_col='fd_salary')
        optimizer.set_min_players_from_team(4, 'GB')
        with self.assertRaises(InvalidConstraintException):
            optimizer.set_num_players_from_team(3, 'GB')

    def test_qb_receiver_stack(self):
        optimizer = FanDuelNflLineupOptimizer(self.data[self.data['week'] == 1],
                                              points_col='fd_points',
                                              salary_col='fd_salary')
        optimizer.set_qb_receiver_stack(team='NE')
        lineup = optimizer.optimize_lineup()
        self.assertEqual(lineup.points, 223.7)
        self.assertEqual(lineup.salary, 58000)
        self.assertEqual(2, len(list(filter(lambda p: p.team == 'NE', lineup.players))))

    def test_qb_receiver_stack_none_team(self):
        optimizer = FanDuelNflLineupOptimizer(self.data[self.data['week'] == 1],
                                              points_col='fd_points',
                                              salary_col='fd_salary')
        self.assertRaises(ValueError, lambda: optimizer.set_qb_receiver_stack(team=None))

    def test_qb_receiver_stack_missing_team(self):
        optimizer = FanDuelNflLineupOptimizer(self.data[self.data['week'] == 1],
                                              points_col='fd_points',
                                              salary_col='fd_salary')
        self.assertRaises(ValueError, lambda: optimizer.set_qb_receiver_stack(team='MISSING'))

    def test_qb_receiver_stack_twice(self):
        optimizer = FanDuelNflLineupOptimizer(self.data[self.data['week'] == 1],
                                              points_col='fd_points',
                                              salary_col='fd_salary')
        with self.assertRaises(InvalidConstraintException):
            optimizer.set_qb_receiver_stack(team='BAL')
            optimizer.set_qb_receiver_stack(team='PIT')

    def test_qb_receiver_stack_team_already_excluded(self):
        optimizer = FanDuelNflLineupOptimizer(self.data[self.data['week'] == 1],
                                              points_col='fd_points',
                                              salary_col='fd_salary')
        with self.assertRaises(InvalidConstraintException):
            optimizer.set_exclude_teams(teams=['MIA'])
            optimizer.set_qb_receiver_stack(team='MIA')

    def test_qb_receiver_stack_with_position(self):
        optimizer = FanDuelNflLineupOptimizer(self.data[self.data['week'] == 1],
                                              points_col='fd_points',
                                              salary_col='fd_salary')
        optimizer.set_qb_receiver_stack(team='TB')
        lineup = optimizer.optimize_lineup()  # lineup will include TB QB/TE stack
        self.assertEqual(228.36, lineup.points)
        self.assertEqual(59900, lineup.salary)
        tb_players = list(filter(lambda p: p.team == 'TB', lineup.players))
        self.assertTrue(tb_players[0].position == 'QB')
        self.assertTrue(tb_players[1].position == 'TE')
        optimizer.clear_constraints()
        optimizer.set_qb_receiver_stack(team='TB', position='WR')
        lineup = optimizer.optimize_lineup()  # lineup will include TB QB/WR stack
        tb_players = list(filter(lambda p: p.team == 'TB', lineup.players))
        self.assertTrue(tb_players[0].position == 'QB')
        self.assertTrue(tb_players[1].position == 'WR')
        optimizer.clear_constraints()
        optimizer.set_qb_receiver_stack(team='BUF', position='TE')
        lineup = optimizer.optimize_lineup()
        buf_players = list(filter(lambda p: p.team == 'BUF', lineup.players))
        self.assertTrue(buf_players[0].position == 'QB')
        self.assertTrue(buf_players[1].position == 'TE')

    def test_qb_receiver_stack_non_receiver_position(self):
        optimizer = FanDuelNflLineupOptimizer(self.data[self.data['week'] == 1],
                                              points_col='fd_points',
                                              salary_col='fd_salary')
        self.assertRaises(ValueError, lambda: optimizer.set_qb_receiver_stack(team='TB', position='RB'))

    def test_qb_receiver_stack_with_num(self):
        optimizer = FanDuelNflLineupOptimizer(self.data[self.data['week'] == 3],
                                              points_col='fd_points',
                                              salary_col='fd_salary')
        optimizer.set_qb_receiver_stack(team='DEN')
        lineup = optimizer.optimize_lineup()
        den_players = list(filter(lambda p: p.team == 'DEN', lineup.players))
        self.assertTrue(len(den_players) == 2)
        self.assertTrue(den_players[0].position == 'QB')
        self.assertTrue(den_players[1].position == 'WR')
        optimizer.clear_constraints()
        optimizer.set_qb_receiver_stack(team='DEN', num_receivers=2)
        lineup = optimizer.optimize_lineup()
        den_players = list(filter(lambda p: p.team == 'DEN', lineup.players))
        self.assertTrue(len(den_players) == 3)
        self.assertTrue(den_players[0].position == 'QB')
        self.assertTrue(den_players[1].position == 'WR')
        self.assertTrue(den_players[2].position == 'TE')

    def test_qb_receiver_stack_num_receivers_and_position(self):
        optimizer = FanDuelNflLineupOptimizer(self.data[self.data['week'] == 3],
                                              points_col='fd_points',
                                              salary_col='fd_salary')
        self.assertRaises(ValueError,
                          lambda: optimizer.set_qb_receiver_stack(team='DEN', position='WR', num_receivers=2))

    def test_rb_dst_stack(self):
        optimizer = FanDuelNflLineupOptimizer(self.data[self.data['week'] == 4],
                                              points_col='fd_points',
                                              salary_col='fd_salary')
        optimizer.set_rb_dst_stack(team='CLE')
        lineup = optimizer.optimize_lineup()
        self.assertEqual(1, len(list(filter(lambda p: p.team == 'CLE' and p.position == 'RB', lineup.players))))
        self.assertEqual(1, len(list(filter(lambda p: p.team == 'CLE' and p.position == 'DST', lineup.players))))

    def test_rb_dst_stack_none_team(self):
        optimizer = FanDuelNflLineupOptimizer(self.data[self.data['week'] == 4],
                                              points_col='fd_points',
                                              salary_col='fd_salary')
        self.assertRaises(ValueError, lambda: optimizer.set_rb_dst_stack(team=None))

    def test_rb_dst_stack_missing_team(self):
        optimizer = FanDuelNflLineupOptimizer(self.data[self.data['week'] == 4],
                                              points_col='fd_points',
                                              salary_col='fd_salary')
        self.assertRaises(ValueError, lambda: optimizer.set_rb_dst_stack(team='MISSING'))

    def test_rb_dst_stack_already_set(self):
        optimizer = FanDuelNflLineupOptimizer(self.data[self.data['week'] == 4],
                                              points_col='fd_points',
                                              salary_col='fd_salary')
        optimizer.set_rb_dst_stack(team='BAL')
        self.assertRaises(InvalidConstraintException, lambda: optimizer.set_rb_dst_stack(team='CLE'))

    def test_optimizer_without_id_col(self):
        optimizer = FanDuelNflLineupOptimizer(self.data[self.data['week'] == 1],
                                              points_col='fd_points',
                                              salary_col='fd_salary')
        self.assertRaises(ValueError, lambda: optimizer.set_must_include_player(id=1))
        self.assertRaises(ValueError, lambda: optimizer.set_exclude_player(id=1))
        lineup = optimizer.optimize_lineup()
        self.assertEqual(244.68, lineup.points)
        self.assertEqual(59800, lineup.salary)

    def test_game_slate_sunday(self):
        optimizer = FanDuelNflLineupOptimizer(self.data[self.data['week'] == 1],
                                              points_col='fd_points',
                                              salary_col='fd_salary')
        lineup = optimizer.optimize_lineup()
        self.assertNotEqual(0, len(list(filter(lambda p: p.datetime.weekday() != 6, lineup.players))))
        optimizer.set_game_slate_sunday()
        lineup = optimizer.optimize_lineup()
        self.assertEqual(0, len(list(filter(lambda p: p.datetime.weekday() != 6, lineup.players))))

    def test_game_slate_sunday_early(self):
        optimizer = FanDuelNflLineupOptimizer(self.data[self.data['week'] == 1],
                                              points_col='fd_points',
                                              salary_col='fd_salary')
        lineup = optimizer.optimize_lineup()
        self.assertNotEqual(0, len(list(filter(lambda p: p.datetime.hour != 13, lineup.players))))
        optimizer.set_game_slate_sunday_early()
        lineup = optimizer.optimize_lineup()
        self.assertEqual(0, len(list(filter(lambda p: p.datetime.hour != 13, lineup.players))))

    def test_game_slate_sunday_early_and_late(self):
        optimizer = FanDuelNflLineupOptimizer(self.data[self.data['week'] == 1],
                                              points_col='fd_points',
                                              salary_col='fd_salary')
        lineup = optimizer.optimize_lineup()
        self.assertNotEqual(0, len(list(filter(lambda p: p.datetime.hour not in [13, 16], lineup.players))))
        optimizer.set_game_slate_sunday_early()
        lineup = optimizer.optimize_lineup()
        self.assertEqual(0, len(list(filter(lambda p: p.datetime.hour not in [13, 16], lineup.players))))

    def test_game_slate_sunday_and_monday(self):
        optimizer = FanDuelNflLineupOptimizer(self.data[self.data['week'] == 4],
                                              points_col='fd_points',
                                              salary_col='fd_salary')
        lineup = optimizer.optimize_lineup()
        self.assertNotEqual(0, len(list(filter(lambda p: p.datetime.weekday() not in [0, 6], lineup.players))))
        optimizer.set_game_slate_sunday_and_monday()
        lineup = optimizer.optimize_lineup()
        self.assertEqual(0, len(list(filter(lambda p: p.datetime.weekday() not in [0, 6], lineup.players))))

    def test_missing_datetime_col(self):
        with self.assertRaises(InvalidDataFrameException):
            FanDuelNflLineupOptimizer(self.data[self.data['week'] == 1],
                                      points_col='fd_points',
                                      salary_col='fd_salary',
                                      datetime_col='datetime_missing')

    def test_game_slate_already_included(self):
        optimizer = FanDuelNflLineupOptimizer(self.data[self.data['week'] == 1],
                                              points_col='fd_points',
                                              salary_col='fd_salary')
        with self.assertRaises(InvalidConstraintException):
            optimizer.set_game_slate_sunday_early()
            optimizer.set_game_slate_sunday_early()

    def test_flex_position(self):
        optimizer = FanDuelNflLineupOptimizer(self.data[self.data['week'] == 1],
                                              points_col='fd_points',
                                              salary_col='fd_salary')
        lineup = optimizer.optimize_lineup()
        self.assertEqual(4, len(list(filter(lambda x: x.position == 'WR', lineup.players))))
        self.assertEqual(1, len(list(filter(lambda x: x.lineup_position == 'FLEX', lineup.players))))
        self.assertTrue(sorted(list(filter(lambda x: x.position == 'WR', lineup.players)),
                               key=lambda x: x.datetime)[-1].lineup_position == 'FLEX')

    def test_slate_monday(self):
        optimizer = FanDuelNflLineupOptimizer(self.data[self.data['week'] == 1],
                                              points_col='fd_points',
                                              salary_col='fd_salary')
        lineup = optimizer.optimize_lineup()
        self.assertNotEqual(0, len(list(filter(lambda p: p.datetime.weekday() != 0, lineup.players))))
        optimizer.set_game_slate_monday()
        lineup = optimizer.optimize_lineup()
        self.assertEqual(0, len(list(filter(lambda p: p.datetime.weekday() != 0, lineup.players))))

    def test_slate_monday_and_thursday(self):
        optimizer = FanDuelNflLineupOptimizer(self.data[self.data['week'].isin([2, 3])],
                                              points_col='fd_points',
                                              salary_col='fd_salary')
        optimizer.set_game_slate_monday_and_thursday()
        lineup = optimizer.optimize_lineup()
        self.assertEqual(9, len(list(filter(lambda x: x.team in ('JAC', 'MIA', 'NO', 'LV'), lineup.players))))

    def test_slate_monday_and_thursday_not_two_weeks(self):
        optimizer = FanDuelNflLineupOptimizer(self.data[self.data['week'] == 2],
                                              points_col='fd_points',
                                              salary_col='fd_salary')
        self.assertRaises(ValueError, lambda: optimizer.set_game_slate_monday_and_thursday())
        optimizer = FanDuelNflLineupOptimizer(self.data[self.data['week'].isin([2, 3, 4])],
                                              points_col='fd_points',
                                              salary_col='fd_salary')
        self.assertRaises(ValueError, lambda: optimizer.set_game_slate_monday_and_thursday())


class TestYahooNflLineupOptimizer(unittest.TestCase, TestNflLineupOptimizer):

    def setUp(self):
        self.data = data.load_2020_data()

    def test_initialize_with_wrong_dataframe_type(self):
        self.assertRaises(ValueError, lambda: YahooNflLineupOptimizer(data_source=56))
        self.assertRaises(ValueError, lambda: YahooNflLineupOptimizer(data_source=[]))

    def test_initialize_with_wrong_file_ext(self):
        self.assertRaises(ValueError, lambda: YahooNflLineupOptimizer(data_source='./file.docx'))

    def test_initialize_with_missing_file(self):
        self.assertRaises(ValueError, lambda: YahooNflLineupOptimizer(data_source='./missing.csv'))

    def test_optimize_with_csv_file(self):
        temp = tempfile.NamedTemporaryFile(mode='w', suffix='.csv')
        data.load_2020_data(weeks=[1]).to_csv(temp.name)
        optimizer = YahooNflLineupOptimizer(data_source=temp.name,
                                            points_col='yh_points',
                                            salary_col='yh_salary')
        lineup = optimizer.optimize_lineup()
        self.assertEqual(244.68, lineup.points)
        self.assertEqual(195, lineup.salary)
        temp.close()

    def test_optimize_with_excel_file(self):
        temp = tempfile.NamedTemporaryFile(mode='w', suffix='.xlsx')
        data.load_2020_data(weeks=[1]).to_excel(temp.name)
        optimizer = YahooNflLineupOptimizer(data_source=temp.name,
                                            points_col='yh_points',
                                            salary_col='yh_salary')
        lineup = optimizer.optimize_lineup()
        self.assertEqual(244.68, lineup.points)
        self.assertEqual(195, lineup.salary)
        temp.close()

    def test_optimizer_setting_missing_column(self):
        self.assertRaises(InvalidDataFrameException,
                          lambda: YahooNflLineupOptimizer(self.data[self.data['week'] == 1], name_col='missing'))

    def test_optimizer_missing_column(self):
        self.assertRaises(InvalidDataFrameException, lambda: YahooNflLineupOptimizer(self.data[self.data['week'] == 1]))

    def test_optimizer_with_different_format_positions(self):
        df = self.data.copy()
        df = df[df['week'] == 2]
        df['position'] = df['position'].apply(lambda x: self.change_position(x))
        optimizer = YahooNflLineupOptimizer(df, points_col='yh_points', salary_col='yh_salary')
        lineup = optimizer.optimize_lineup()
        self.assertEqual(253.18, lineup.points)
        self.assertEqual(199, lineup.salary)

    def test_optimizer_missing_positions(self):
        optimizer = YahooNflLineupOptimizer(self.data[self.data['position'] != 'QB'],
                                                 points_col='yh_points',
                                                 salary_col='yh_salary')
        self.assertRaises(InvalidDataFrameException, lambda: optimizer.optimize_lineup())

    def test_only_include_teams_constraint(self):
        optimizer = YahooNflLineupOptimizer(self.data[self.data['week'] == 2],
                                            points_col='yh_points',
                                            salary_col='yh_salary')
        teams = ['ATL', 'CAR', 'NO', 'TB']
        optimizer.set_only_include_teams(teams=teams)
        lineup = optimizer.optimize_lineup()
        self.assertTrue(all([x.team in teams for x in lineup.players]))

    def test_only_include_teams_none_teams(self):
        optimizer = YahooNflLineupOptimizer(self.data[self.data['week'] == 2],
                                            points_col='yh_points',
                                            salary_col='yh_salary')
        self.assertRaises(ValueError, lambda: optimizer.set_only_include_teams(teams=None))

    def test_only_include_teams_empty_teams(self):
        optimizer = YahooNflLineupOptimizer(self.data[self.data['week'] == 2],
                                            points_col='yh_points',
                                            salary_col='yh_salary')
        self.assertRaises(ValueError, lambda: optimizer.set_only_include_teams(teams=[]))

    def test_only_include_teams_already_excluded(self):
        optimizer = YahooNflLineupOptimizer(self.data[self.data['week'] == 2],
                                            points_col='yh_points',
                                            salary_col='yh_salary')
        optimizer.set_exclude_teams(teams=['CHI', 'DET', 'GB', 'MIN'])
        self.assertRaises(InvalidConstraintException, lambda: optimizer.set_only_include_teams(teams=['DET', 'MIN']))

    def test_exclude_teams(self):
        optimizer = YahooNflLineupOptimizer(self.data[self.data['week'] == 3],
                                            points_col='yh_points',
                                            salary_col='yh_salary')
        lineup = optimizer.optimize_lineup()
        self.assertTrue(all([p in [n.name for n in lineup.players] for p in ['Alvin Kamara', 'Rex Burkhead']]))
        optimizer.set_exclude_teams(teams=['NO', 'NE'])
        lineup = optimizer.optimize_lineup()
        self.assertTrue(all([p not in [n.name for n in lineup.players] for p in ['Alvin Kamara', 'Rex Burkhead']]))

    def test_exclude_teams_none(self):
        optimizer = YahooNflLineupOptimizer(self.data[self.data['week'] == 3],
                                            points_col='yh_points',
                                            salary_col='yh_salary')
        self.assertRaises(ValueError, lambda: optimizer.set_exclude_teams(teams=None))

    def test_exclude_teams_empty(self):
        optimizer = YahooNflLineupOptimizer(self.data[self.data['week'] == 3],
                                            points_col='yh_points',
                                            salary_col='yh_salary')
        self.assertRaises(ValueError, lambda: optimizer.set_exclude_teams(teams=[]))

    def test_clear_constraints(self):
        optimizer = YahooNflLineupOptimizer(self.data[self.data['week'] == 1],
                                            points_col='yh_points',
                                            salary_col='yh_salary')
        teams = ['GB', 'SEA']
        optimizer.set_exclude_teams(teams)
        lineup = optimizer.optimize_lineup()
        self.assertTrue(all([x.team not in teams for x in lineup.players]))
        optimizer.clear_constraints()
        lineup = optimizer.optimize_lineup()
        self.assertTrue(all([t in [x.team for x in lineup.players] for t in teams]))

    def test_must_include_team(self):
        optimizer = YahooNflLineupOptimizer(self.data[self.data['week'] == 1],
                                            points_col='yh_points',
                                            salary_col='yh_salary')
        lineup = optimizer.optimize_lineup()
        team = 'DET'
        self.assertTrue(all([p.team != team for p in lineup.players]))  # lineup shouldn't include any DET player
        optimizer.set_must_include_team(team)
        lineup = optimizer.optimize_lineup()
        self.assertTrue(any([p.team == team for p in lineup.players]))  # lineup should include DET player

    def test_must_include_team_none(self):
        optimizer = YahooNflLineupOptimizer(self.data[self.data['week'] == 1],
                                            points_col='yh_points',
                                            salary_col='yh_salary')
        self.assertRaises(ValueError, lambda: optimizer.set_must_include_team(team=None))

    def test_must_include_team_missing(self):
        optimizer = YahooNflLineupOptimizer(self.data[self.data['week'] == 1],
                                            points_col='yh_points',
                                            salary_col='yh_salary')
        self.assertRaises(ValueError, lambda: optimizer.set_must_include_team(team='MISSING'))

    def test_include_player_name(self):
        optimizer = YahooNflLineupOptimizer(self.data[self.data['week'] == 4],
                                            points_col='yh_points',
                                            salary_col='yh_salary',
                                            id_col='id')
        optimizer.set_must_include_player(name='Aaron Rodgers')
        lineup = optimizer.optimize_lineup()
        self.assertTrue('Aaron Rodgers' in [p.name for p in lineup.players])
        self.assertEqual(lineup.points, 265.68)
        self.assertEqual(lineup.salary, 200)

    def test_include_player_none_name(self):
        optimizer = YahooNflLineupOptimizer(self.data[self.data['week'] == 4],
                                            points_col='yh_points',
                                            salary_col='yh_salary',
                                            id_col='id')
        self.assertRaises(ValueError, lambda: optimizer.set_must_include_player(name=None))

    def test_include_player_missing_name(self):
        optimizer = YahooNflLineupOptimizer(self.data[self.data['week'] == 4],
                                            points_col='yh_points',
                                            salary_col='yh_salary',
                                            id_col='id')
        self.assertRaises(ValueError, lambda: optimizer.set_must_include_player(name='Missing Player'))

    def test_include_player_id(self):
        optimizer = YahooNflLineupOptimizer(self.data[self.data['week'] == 4],
                                            points_col='yh_points',
                                            salary_col='yh_salary',
                                            id_col='id')
        optimizer.set_must_include_player(id=1419)
        lineup = optimizer.optimize_lineup()
        self.assertTrue('Aaron Rodgers' in [p.name for p in lineup.players])
        self.assertEqual(lineup.points, 265.68)
        self.assertEqual(lineup.salary, 200)

    def test_include_player_none_id(self):
        optimizer = YahooNflLineupOptimizer(self.data[self.data['week'] == 4],
                                            points_col='yh_points',
                                            salary_col='yh_salary',
                                            id_col='id')
        self.assertRaises(ValueError, lambda: optimizer.set_must_include_player(id=None))

    def test_include_player_missing_id(self):
        optimizer = YahooNflLineupOptimizer(self.data[self.data['week'] == 4],
                                            points_col='yh_points',
                                            salary_col='yh_salary',
                                            id_col='id')
        self.assertRaises(ValueError, lambda: optimizer.set_must_include_player(id=9999))

    def test_exclude_player_name(self):
        optimizer = YahooNflLineupOptimizer(self.data[self.data['week'] == 4],
                                            points_col='yh_points',
                                            salary_col='yh_salary',
                                            id_col='id')
        lineup = optimizer.optimize_lineup()
        self.assertTrue('Joe Mixon' in [p.name for p in lineup.players])
        optimizer.set_exclude_player(name='Joe Mixon')
        lineup = optimizer.optimize_lineup()
        self.assertEqual(lineup.points, 256.08)
        self.assertEqual(lineup.salary, 198)
        self.assertFalse('Joe Mixon' in [p.name for p in lineup.players])

    def test_exclude_player_name_none(self):
        optimizer = YahooNflLineupOptimizer(self.data[self.data['week'] == 4],
                                            points_col='yh_points',
                                            salary_col='yh_salary',
                                            id_col='id')
        self.assertRaises(ValueError, lambda: optimizer.set_exclude_player(name=None))

    def test_exclude_player_name_already_included(self):
        optimizer = YahooNflLineupOptimizer(self.data[self.data['week'] == 4],
                                            points_col='yh_points',
                                            salary_col='yh_salary',
                                            id_col='id')
        optimizer.set_must_include_player(name='Aaron Jones')
        self.assertRaises(InvalidConstraintException, lambda: optimizer.set_exclude_player(name='Aaron Jones'))

    def test_exclude_player_name_missing(self):
        optimizer = YahooNflLineupOptimizer(self.data[self.data['week'] == 4],
                                            points_col='yh_points',
                                            salary_col='yh_salary',
                                            id_col='id')
        self.assertRaises(ValueError, lambda: optimizer.set_exclude_player(name='Missing Player'))

    def test_exclude_player_id(self):
        optimizer = YahooNflLineupOptimizer(self.data[self.data['week'] == 4],
                                            points_col='yh_points',
                                            salary_col='yh_salary',
                                            id_col='id')
        lineup = optimizer.optimize_lineup()
        self.assertTrue('Joe Mixon' in [p.name for p in lineup.players])
        optimizer.set_exclude_player(id=1456)
        lineup = optimizer.optimize_lineup()
        self.assertEqual(lineup.points, 256.08)
        self.assertEqual(lineup.salary, 198)
        self.assertFalse('Joe Mixon' in [p.name for p in lineup.players])

    def test_exclude_player_id_already_included(self):
        optimizer = YahooNflLineupOptimizer(self.data[self.data['week'] == 4],
                                            points_col='yh_points',
                                            salary_col='yh_salary',
                                            id_col='id')
        optimizer.set_must_include_player(id=1456)
        self.assertRaises(InvalidConstraintException, lambda: optimizer.set_exclude_player(id=1456))

    def test_exclude_player_id_none(self):
        optimizer = YahooNflLineupOptimizer(self.data[self.data['week'] == 4],
                                            points_col='yh_points',
                                            salary_col='yh_salary',
                                            id_col='id')
        self.assertRaises(ValueError, lambda: optimizer.set_exclude_player(id=None))

    def test_exclude_player_id_missing(self):
        optimizer = YahooNflLineupOptimizer(self.data[self.data['week'] == 4],
                                            points_col='yh_points',
                                            salary_col='yh_salary',
                                            id_col='id')
        self.assertRaises(ValueError, lambda: optimizer.set_exclude_player(id=9999))

    def test_max_from_team(self):
        optimizer = YahooNflLineupOptimizer(self.data[self.data['week'] == 4],
                                            points_col='yh_points',
                                            salary_col='yh_salary')
        lineup = optimizer.optimize_lineup()
        self.assertEqual(lineup.points, 270.38)
        self.assertEqual(lineup.salary, 196)
        self.assertTrue(len([filter(lambda p: p.team == 'DAL', lineup.players)]), 2)
        optimizer.set_max_players_from_team(1, 'DAL')
        lineup = optimizer.optimize_lineup()
        self.assertEqual(lineup.points, 269.56)
        self.assertEqual(lineup.salary, 196)
        self.assertTrue(len([filter(lambda p: p.team == 'DAL', lineup.players)]), 1)
        optimizer.clear_constraints()
        optimizer.set_max_players_from_team(0, 'DAL')
        lineup = optimizer.optimize_lineup()
        self.assertEqual(lineup.points, 265.26)
        self.assertEqual(lineup.salary, 192)
        self.assertTrue(len([filter(lambda p: p.team == 'DAL', lineup.players)]), 0)

    def test_max_from_team_twice(self):
        optimizer = YahooNflLineupOptimizer(self.data[self.data['week'] == 3],
                                            points_col='yh_points',
                                            salary_col='yh_salary')
        with self.assertRaises(InvalidConstraintException):
            optimizer.set_max_players_from_team(0, 'CHI')
            optimizer.set_max_players_from_team(1, 'CHI')

    def test_max_from_team_less_than_min(self):
        optimizer = YahooNflLineupOptimizer(self.data[self.data['week'] == 3],
                                            points_col='yh_points',
                                            salary_col='yh_salary')
        optimizer.set_min_players_from_team(3, 'CHI')
        self.assertRaises(InvalidConstraintException, lambda: optimizer.set_max_players_from_team(2, 'CHI'))

    def test_max_from_team_none_value(self):
        optimizer = YahooNflLineupOptimizer(self.data[self.data['week'] == 3],
                                            points_col='yh_points',
                                            salary_col='yh_salary')
        self.assertRaises(ValueError, lambda: optimizer.set_max_players_from_team(None, 'CHI'))

    def test_max_from_team_negative_value(self):
        optimizer = YahooNflLineupOptimizer(self.data[self.data['week'] == 3],
                                            points_col='yh_points',
                                            salary_col='yh_salary')
        self.assertRaises(ValueError, lambda: optimizer.set_max_players_from_team(-2, 'CHI'))

    def test_max_from_team_none_team(self):
        optimizer = YahooNflLineupOptimizer(self.data[self.data['week'] == 3],
                                            points_col='yh_points',
                                            salary_col='yh_salary')
        self.assertRaises(ValueError, lambda: optimizer.set_max_players_from_team(2, None))

    def test_max_from_team_missing_team(self):
        optimizer = YahooNflLineupOptimizer(self.data[self.data['week'] == 3],
                                            points_col='yh_points',
                                            salary_col='yh_salary')
        self.assertRaises(ValueError, lambda: optimizer.set_max_players_from_team(2, 'MISSING'))

    def test_min_from_team(self):
        optimizer = YahooNflLineupOptimizer(self.data[self.data['week'] == 2],
                                            points_col='yh_points',
                                            salary_col='yh_salary')
        lineup = optimizer.optimize_lineup()
        self.assertEqual(len(list(filter(lambda p: p.team == 'CIN', lineup.players))), 0)
        optimizer.set_min_players_from_team(2, 'CIN')
        lineup = optimizer.optimize_lineup()
        self.assertEqual(len(list(filter(lambda p: p.team == 'CIN', lineup.players))), 2)

    def test_min_from_team_none_value(self):
        optimizer = YahooNflLineupOptimizer(self.data[self.data['week'] == 2],
                                            points_col='yh_points',
                                            salary_col='yh_salary')
        self.assertRaises(ValueError, lambda: optimizer.set_min_players_from_team(n=None, team='CIN'))

    def test_min_from_team_too_large(self):
        optimizer = YahooNflLineupOptimizer(self.data[self.data['week'] == 2],
                                            points_col='yh_points',
                                            salary_col='yh_salary')
        self.assertRaises(ValueError, lambda: optimizer.set_min_players_from_team(n=20, team='CIN'))

    def test_min_from_team_none_team(self):
        optimizer = YahooNflLineupOptimizer(self.data[self.data['week'] == 2],
                                            points_col='yh_points',
                                            salary_col='yh_salary')
        self.assertRaises(ValueError, lambda: optimizer.set_min_players_from_team(n=2, team=None))

    def test_min_from_team_missing_team(self):
        optimizer = YahooNflLineupOptimizer(self.data[self.data['week'] == 2],
                                            points_col='yh_points',
                                            salary_col='yh_salary')
        self.assertRaises(ValueError, lambda: optimizer.set_min_players_from_team(n=2, team='MISSING'))

    def test_min_from_team_already_having_max_less_than(self):
        optimizer = YahooNflLineupOptimizer(self.data[self.data['week'] == 2],
                                            points_col='yh_points',
                                            salary_col='yh_salary')
        with self.assertRaises(InvalidConstraintException):
            optimizer.set_max_players_from_team(n=2, team='CIN')
            optimizer.set_min_players_from_team(n=3, team='CIN')

    def test_min_from_team_twice(self):
        optimizer = YahooNflLineupOptimizer(self.data[self.data['week'] == 2],
                                            points_col='yh_points',
                                            salary_col='yh_salary')
        with self.assertRaises(InvalidConstraintException):
            optimizer.set_min_players_from_team(n=2, team='CIN')
            optimizer.set_min_players_from_team(n=3, team='CIN')

    def test_max_salary(self):
        optimizer = YahooNflLineupOptimizer(self.data[self.data['week'] == 3],
                                            points_col='yh_points',
                                            salary_col='yh_salary')
        optimizer.set_max_salary(n=150)
        lineup = optimizer.optimize_lineup()
        self.assertEqual(lineup.salary, 150)
        self.assertEqual(lineup.points, 248.1)

    def test_max_salary_none(self):
        optimizer = YahooNflLineupOptimizer(self.data[self.data['week'] == 3],
                                            points_col='yh_points',
                                            salary_col='yh_salary')
        self.assertRaises(ValueError, lambda: optimizer.set_max_salary(n=None))

    def test_max_salary_zero(self):
        optimizer = YahooNflLineupOptimizer(self.data[self.data['week'] == 3],
                                            points_col='yh_points',
                                            salary_col='yh_salary')
        self.assertRaises(ValueError, lambda: optimizer.set_max_salary(n=0))

    def test_max_salary_already_having_min_greater_than(self):
        optimizer = YahooNflLineupOptimizer(self.data[self.data['week'] == 3],
                                            points_col='yh_points',
                                            salary_col='yh_salary')
        with self.assertRaises(InvalidConstraintException):
            optimizer.set_min_salary(n=175)
            optimizer.set_max_salary(n=170)

    def test_min_salary(self):
        optimizer = YahooNflLineupOptimizer(self.data[self.data['week'] == 4],
                                            points_col='yh_points',
                                            salary_col='yh_salary')
        lineup = optimizer.optimize_lineup()
        self.assertLess(lineup.salary, 200)
        optimizer.set_min_salary(200)
        lineup = optimizer.optimize_lineup()
        self.assertEqual(lineup.salary, 200)
        self.assertEqual(lineup.points, 268.26)

    def test_min_salary_none(self):
        optimizer = YahooNflLineupOptimizer(self.data[self.data['week'] == 4],
                                            points_col='yh_points',
                                            salary_col='yh_salary')
        self.assertRaises(ValueError, lambda: optimizer.set_min_salary(n=None))

    def test_min_salary_too_high(self):
        optimizer = YahooNflLineupOptimizer(self.data[self.data['week'] == 4],
                                            points_col='yh_points',
                                            salary_col='yh_salary')
        self.assertRaises(ValueError, lambda: optimizer.set_min_salary(n=250))

    def test_min_salary_already_having_max_lower(self):
        optimizer = YahooNflLineupOptimizer(self.data[self.data['week'] == 4],
                                            points_col='yh_points',
                                            salary_col='yh_salary')
        with self.assertRaises(InvalidConstraintException):
            optimizer.set_max_salary(n=190)
            optimizer.set_min_salary(n=195)

    def test_num_players_from_team(self):
        optimizer = YahooNflLineupOptimizer(self.data[self.data['week'] == 4],
                                            points_col='yh_points',
                                            salary_col='yh_salary')
        optimizer.set_num_players_from_team(4, 'GB')
        optimizer.set_num_players_from_team(2, 'DET')
        lineup = optimizer.optimize_lineup()
        self.assertEqual(4, len(list(filter(lambda p: p.team == 'GB', lineup.players))))
        self.assertEqual(2, len(list(filter(lambda p: p.team == 'DET', lineup.players))))

    def test_num_players_from_team_none_value(self):
        optimizer = YahooNflLineupOptimizer(self.data[self.data['week'] == 4],
                                            points_col='yh_points',
                                            salary_col='yh_salary')
        self.assertRaises(ValueError, lambda: optimizer.set_num_players_from_team(n=None, team='GB'))

    def test_num_players_from_team_value_too_high(self):
        optimizer = YahooNflLineupOptimizer(self.data[self.data['week'] == 4],
                                            points_col='yh_points',
                                            salary_col='yh_salary')
        self.assertRaises(ValueError, lambda: optimizer.set_num_players_from_team(n=10, team='GB'))

    def test_num_players_from_team_none_team(self):
        optimizer = YahooNflLineupOptimizer(self.data[self.data['week'] == 4],
                                            points_col='yh_points',
                                            salary_col='yh_salary')
        self.assertRaises(ValueError, lambda: optimizer.set_num_players_from_team(n=3, team=None))

    def test_num_players_from_team_missing_team(self):
        optimizer = YahooNflLineupOptimizer(self.data[self.data['week'] == 4],
                                            points_col='yh_points',
                                            salary_col='yh_salary')
        self.assertRaises(ValueError, lambda: optimizer.set_num_players_from_team(n=3, team='MISSING'))

    def test_num_players_from_team_already_specified(self):
        optimizer = YahooNflLineupOptimizer(self.data[self.data['week'] == 4],
                                            points_col='yh_points',
                                            salary_col='yh_salary')
        with self.assertRaises(InvalidConstraintException):
            optimizer.set_num_players_from_team(n=3, team='GB')
            optimizer.set_num_players_from_team(n=2, team='GB')

    def test_qb_receiver_stack(self):
        optimizer = YahooNflLineupOptimizer(self.data[self.data['week'] == 1],
                                            points_col='yh_points',
                                            salary_col='yh_salary')
        optimizer.set_qb_receiver_stack(team='NE')
        lineup = optimizer.optimize_lineup()
        self.assertEqual(lineup.points, 223.9)
        self.assertEqual(lineup.salary, 193)
        self.assertEqual(2, len(list(filter(lambda p: p.team == 'NE', lineup.players))))

    def test_qb_receiver_stack_none_team(self):
        optimizer = YahooNflLineupOptimizer(self.data[self.data['week'] == 1],
                                            points_col='yh_points',
                                            salary_col='yh_salary')
        self.assertRaises(ValueError, lambda: optimizer.set_qb_receiver_stack(team=None))

    def test_qb_receiver_stack_missing_team(self):
        optimizer = YahooNflLineupOptimizer(self.data[self.data['week'] == 1],
                                            points_col='yh_points',
                                            salary_col='yh_salary')
        self.assertRaises(ValueError, lambda: optimizer.set_qb_receiver_stack(team='MISSING'))

    def test_qb_receiver_stack_twice(self):
        optimizer = YahooNflLineupOptimizer(self.data[self.data['week'] == 1],
                                            points_col='yh_points',
                                            salary_col='yh_salary')
        with self.assertRaises(InvalidConstraintException):
            optimizer.set_qb_receiver_stack(team='PIT')
            optimizer.set_qb_receiver_stack(team='BAL')

    def test_qb_receiver_stack_team_already_excluded(self):
        optimizer = YahooNflLineupOptimizer(self.data[self.data['week'] == 1],
                                            points_col='yh_points',
                                            salary_col='yh_salary')
        with self.assertRaises(InvalidConstraintException):
            optimizer.set_exclude_teams(teams=['BAL'])
            optimizer.set_qb_receiver_stack(team='BAL')

    def test_qb_receiver_stack_with_position(self):
        optimizer = YahooNflLineupOptimizer(self.data[self.data['week'] == 1],
                                            points_col='yh_points',
                                            salary_col='yh_salary')
        optimizer.set_qb_receiver_stack(team='TB')
        lineup = optimizer.optimize_lineup()  # lineup will include TB QB/TE stack
        self.assertEqual(227.66, lineup.points)
        self.assertEqual(197, lineup.salary)
        tb_players = list(filter(lambda p: p.team == 'TB', lineup.players))
        self.assertTrue(tb_players[0].position == 'QB')
        self.assertTrue(tb_players[1].position == 'TE')
        optimizer.clear_constraints()
        optimizer.set_qb_receiver_stack(team='TB', position='WR')
        lineup = optimizer.optimize_lineup()  # lineup will include TB QB/WR stack
        tb_players = list(filter(lambda p: p.team == 'TB', lineup.players))
        self.assertTrue(tb_players[0].position == 'QB')
        self.assertTrue(tb_players[1].position == 'WR')
        optimizer.clear_constraints()
        optimizer.set_qb_receiver_stack(team='BUF', position='TE')
        lineup = optimizer.optimize_lineup()
        buf_players = list(filter(lambda p: p.team == 'BUF', lineup.players))
        self.assertTrue(buf_players[0].position == 'QB')
        self.assertTrue(buf_players[1].position == 'TE')

    def test_qb_receiver_stack_non_receiver_position(self):
        optimizer = YahooNflLineupOptimizer(self.data[self.data['week'] == 1],
                                            points_col='yh_points',
                                            salary_col='yh_salary')
        self.assertRaises(ValueError, lambda: optimizer.set_qb_receiver_stack(team='MIA', position='RB'))

    def test_qb_receiver_stack_with_num(self):
        optimizer = YahooNflLineupOptimizer(self.data[self.data['week'] == 3],
                                            points_col='yh_points',
                                            salary_col='yh_salary')
        optimizer.set_qb_receiver_stack(team='DEN')
        lineup = optimizer.optimize_lineup()
        den_players = list(filter(lambda p: p.team == 'DEN', lineup.players))
        self.assertTrue(len(den_players) == 2)
        self.assertTrue(den_players[0].position == 'QB')
        self.assertTrue(den_players[1].position == 'WR')
        optimizer.clear_constraints()
        optimizer.set_qb_receiver_stack(team='DEN', num_receivers=2)
        lineup = optimizer.optimize_lineup()
        den_players = list(filter(lambda p: p.team == 'DEN', lineup.players))
        self.assertTrue(len(den_players) == 3)
        self.assertTrue(den_players[0].position == 'QB')
        self.assertTrue(den_players[1].position == 'WR')
        self.assertTrue(den_players[2].position == 'TE')

    def test_qb_receiver_stack_num_receivers_and_position(self):
        optimizer = YahooNflLineupOptimizer(self.data[self.data['week'] == 3],
                                            points_col='fd_points',
                                            salary_col='fd_salary')
        self.assertRaises(ValueError,
                          lambda: optimizer.set_qb_receiver_stack(team='DEN', position='WR', num_receivers=2))

    def test_rb_dst_stack(self):
        optimizer = YahooNflLineupOptimizer(self.data[self.data['week'] == 4],
                                            points_col='yh_points',
                                            salary_col='yh_salary')
        lineup = optimizer.optimize_lineup()
        self.assertTrue(len(list(filter(lambda p: p.team == 'CLE' and p.position in ['RB', 'DST'], lineup.players))) == 0)
        optimizer.set_rb_dst_stack(team='CLE')
        lineup = optimizer.optimize_lineup()
        self.assertEqual(1, len(list(filter(lambda p: p.team == 'CLE' and p.position == 'RB', lineup.players))))
        self.assertEqual(1, len(list(filter(lambda p: p.team == 'CLE' and p.position == 'DST', lineup.players))))

    def test_rb_dst_stack_none_team(self):
        optimizer = YahooNflLineupOptimizer(self.data[self.data['week'] == 4],
                                            points_col='yh_points',
                                            salary_col='yh_salary')
        self.assertRaises(ValueError, lambda: optimizer.set_rb_dst_stack(team=None))

    def test_rb_dst_stack_missing_team(self):
        optimizer = YahooNflLineupOptimizer(self.data[self.data['week'] == 4],
                                            points_col='yh_points',
                                            salary_col='yh_salary')
        self.assertRaises(ValueError, lambda: optimizer.set_rb_dst_stack(team='MISSING'))

    def test_rb_dst_stack_already_set(self):
        optimizer = YahooNflLineupOptimizer(self.data[self.data['week'] == 4],
                                            points_col='yh_points',
                                            salary_col='yh_salary')
        with self.assertRaises(InvalidConstraintException):
            optimizer.set_rb_dst_stack(team='LAC')
            optimizer.set_rb_dst_stack(team='LAR')

    def test_optimizer_without_id_col(self):
        optimizer = YahooNflLineupOptimizer(self.data[self.data['week'] == 1],
                                            points_col='yh_points',
                                            salary_col='yh_salary')
        self.assertRaises(ValueError, lambda: optimizer.set_must_include_player(id=1))
        self.assertRaises(ValueError, lambda: optimizer.set_exclude_player(id=1))
        lineup = optimizer.optimize_lineup()
        self.assertEqual(244.68, lineup.points)
        self.assertEqual(195, lineup.salary)

    def test_multi_game(self):
        optimizer = YahooNflLineupOptimizer(self.data[self.data['week'] == 1],
                                            points_col='yh_points',
                                            salary_col='yh_salary')
        lineup = optimizer.optimize_lineup()
        self.assertEqual(244.68, lineup.points)
        self.assertEqual(195, lineup.salary)

    def test_game_slate_sunday(self):
        optimizer = YahooNflLineupOptimizer(self.data[self.data['week'] == 1],
                                            points_col='yh_points',
                                            salary_col='yh_salary')
        lineup = optimizer.optimize_lineup()
        self.assertNotEqual(0, len(list(filter(lambda p: p.datetime.weekday() != 6, lineup.players))))
        optimizer.set_game_slate_sunday()
        lineup = optimizer.optimize_lineup()
        self.assertEqual(0, len(list(filter(lambda p: p.datetime.weekday() != 6, lineup.players))))

    def test_game_slate_sunday_early(self):
        optimizer = YahooNflLineupOptimizer(self.data[self.data['week'] == 1],
                                            points_col='yh_points',
                                            salary_col='yh_salary')
        lineup = optimizer.optimize_lineup()
        self.assertNotEqual(0, len(list(filter(lambda p: p.datetime.hour != 13, lineup.players))))
        optimizer.set_game_slate_sunday_early()
        lineup = optimizer.optimize_lineup()
        self.assertEqual(0, len(list(filter(lambda p: p.datetime.hour != 13, lineup.players))))

    def test_game_slate_sunday_early_and_late(self):
        optimizer = YahooNflLineupOptimizer(self.data[self.data['week'] == 1],
                                            points_col='yh_points',
                                            salary_col='yh_salary')
        lineup = optimizer.optimize_lineup()
        self.assertNotEqual(0, len(list(filter(lambda p: p.datetime.hour not in [13, 16], lineup.players))))
        optimizer.set_game_slate_sunday_early()
        lineup = optimizer.optimize_lineup()
        self.assertEqual(0, len(list(filter(lambda p: p.datetime.hour not in [13, 16], lineup.players))))

    def test_game_slate_sunday_and_monday(self):
        optimizer = YahooNflLineupOptimizer(self.data[self.data['week'] == 3],
                                            points_col='yh_points',
                                            salary_col='yh_salary')
        lineup = optimizer.optimize_lineup()
        self.assertNotEqual(0, len(list(filter(lambda p: p.datetime.weekday() not in [0, 6], lineup.players))))
        optimizer.set_game_slate_sunday_and_monday()
        lineup = optimizer.optimize_lineup()
        self.assertEqual(0, len(list(filter(lambda p: p.datetime.weekday() not in [0, 6], lineup.players))))

    def test_missing_datetime_col(self):
        with self.assertRaises(InvalidDataFrameException):
            YahooNflLineupOptimizer(self.data[self.data['week'] == 1],
                                    points_col='yh_points',
                                    salary_col='yh_salary',
                                    datetime_col='datetime_missing')

    def test_game_slate_already_included(self):
        optimizer = YahooNflLineupOptimizer(self.data[self.data['week'] == 1],
                                            points_col='yh_points',
                                            salary_col='yh_salary')
        with self.assertRaises(InvalidConstraintException):
            optimizer.set_game_slate_sunday_early()
            optimizer.set_game_slate_sunday_early()

    def test_flex_position(self):
        optimizer = YahooNflLineupOptimizer(self.data[self.data['week'] == 1],
                                            points_col='yh_points',
                                            salary_col='yh_salary')
        lineup = optimizer.optimize_lineup()
        self.assertEqual(4, len(list(filter(lambda x: x.position == 'WR', lineup.players))))
        self.assertEqual(1, len(list(filter(lambda x: x.lineup_position == 'FLEX', lineup.players))))
        self.assertTrue(sorted(list(filter(lambda x: x.position == 'WR', lineup.players)),
                               key=lambda x: x.datetime)[-1].lineup_position == 'FLEX')

    def test_slate_monday(self):
        optimizer = YahooNflLineupOptimizer(self.data[self.data['week'] == 1],
                                            points_col='yh_points',
                                            salary_col='yh_salary')
        lineup = optimizer.optimize_lineup()
        self.assertNotEqual(0, len(list(filter(lambda p: p.datetime.weekday() != 0, lineup.players))))
        optimizer.set_game_slate_monday()
        lineup = optimizer.optimize_lineup()
        self.assertEqual(0, len(list(filter(lambda p: p.datetime.weekday() != 0, lineup.players))))

    def test_slate_monday_and_thursday(self):
        optimizer = YahooNflLineupOptimizer(self.data[self.data['week'].isin([2, 3])],
                                            points_col='yh_points',
                                            salary_col='yh_salary')
        optimizer.set_game_slate_monday_and_thursday()
        lineup = optimizer.optimize_lineup()
        self.assertEqual(9, len(list(filter(lambda x: x.team in ('JAC', 'MIA', 'NO', 'LV'), lineup.players))))

    def test_slate_monday_and_thursday_not_two_weeks(self):
        optimizer = YahooNflLineupOptimizer(self.data[self.data['week'] == 2],
                                            points_col='yh_points',
                                            salary_col='yh_salary')
        self.assertRaises(ValueError, lambda: optimizer.set_game_slate_monday_and_thursday())
        optimizer = YahooNflLineupOptimizer(self.data[self.data['week'].isin([2, 3, 4])],
                                            points_col='yh_points',
                                            salary_col='yh_salary')
        self.assertRaises(ValueError, lambda: optimizer.set_game_slate_monday_and_thursday())

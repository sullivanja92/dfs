from abc import ABC, abstractmethod


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

    @abstractmethod
    def test_optimized_lineup_salary_cap(self):
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

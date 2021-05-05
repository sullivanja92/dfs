import csv
from collections.abc import Mapping
from typing import AbstractSet, List, Union, Iterator

import pandas as pd
from pulp import LpMaximize, LpProblem, LpVariable, lpSum, PULP_CBC_CMD

from dfs import constraints
from dfs import file_utils
from dfs import positions, data_frame_utils, pulp_utils
from dfs import sites
from dfs.exceptions import InvalidDataFrameException, UnsolvableLineupException, InvalidConstraintException
from dfs.schedule import ScheduleType


class OptimizedLineup:
    """
    A class that represents an optimized fantasy football lineup for a given site.
    """

    def __init__(self, problem: LpProblem, data: pd.DataFrame, site: str):
        """
        :param problem: The LP Problem.
        :param data: The player data frame.
        :param site: The fantasy site that the lineup has been generated for.
        """
        self.site = site
        self.index = [pulp_utils.int_index_from_lp_variable_name(p.name)
                      for p in filter(lambda x: x.varValue == 1, problem.variables())]
        players = data.loc[self.index]
        self.points = round(players['points'].sum(), 2)
        self.salary = players['salary'].sum()
        self.players = [LineupPlayer(p) for p in players.to_dict('records')]

    def write_to_file(self, file_path: str) -> None:
        """
        Writes the optimized lineup to a CSV file.

        :param file_path: the path to the file which will be created if it does not exist.
        :return: None
        :raises: ValueError if file_path is None or points to a non-CSV file.
        """
        if file_path is None:
            raise ValueError('File path cannot be none')
        extension = file_utils.get_extension(file_path)
        if extension != '.csv':
            raise ValueError(f"Only CSV output is supported, found: {extension}")
        file_exists = file_utils.file_exists(file_path)
        with open(file_path, mode='a') as f:
            writer = csv.DictWriter(f, fieldnames=self.players[0].keys())
            if not file_exists:
                writer.writeheader()
            writer.writerows(self.players)

    def __repr__(self):
        return (f"pygskin.optimize.OptimizedLineup(site={self.site}, points={self.points}, salary={self.salary}, "
                f"players={self.players}, index={self.index})")

    def __str__(self):
        players_string = '\n'.join([f"{p['position'].value} - {p['name']} {p['points']} @ {p['salary']} salary"
                                    for p in self.players])
        return (f"Optimized {self.site} Lineup \n"
                f"{self.points} points @ {self.salary} salary \n") + players_string


class LineupPlayer(Mapping):
    """
    A model of a player included in an optimized lineup.
    """

    def __len__(self) -> int:
        return len(vars(self))

    def __iter__(self) -> Iterator[str]:
        return iter({a: getattr(self, a) for a in vars(self)})

    def keys(self) -> AbstractSet[str]:
        return vars(self).keys()

    def __init__(self, player_dict):
        """
        :param player_dict: the player dict from dataframe
        """
        self.name = player_dict['name']
        self.year = player_dict['year']
        self.week = player_dict['week']
        self.position = player_dict['position']
        self.team = player_dict['team']
        self.opponent = player_dict['opponent']
        self.datetime = player_dict['datetime']
        self.points = player_dict['points']
        self.salary = player_dict['salary']

    def __getitem__(self, item):
        return getattr(self, item)


class LineupOptimizer:
    """
    A pandas data frame-based fantasy football lineup optimizer.
    This class is used to generate optimal fantasy football lineups for various sites when provided
    a data frame containing player, position, salary and points information.
    """

    _LP_VAR_COL = 'LpVariable'

    def __init__(self,
                 data: pd.DataFrame,
                 id_col: str = 'id',
                 name_col: str = 'name',
                 points_col: str = 'points',
                 position_col: str = 'position',
                 salary_col: str = 'salary',
                 team_col: str = 'team',
                 datetime_col: str = 'datetime',
                 year_col: str = 'year',
                 week_col: str = 'week',
                 opponent_col: str = 'opponent'):
        """
        :param data: The pandas data frame containing fantasy data.
        :param id_col: The player ID column. Default is 'id'.
        :param name_col: The player name column. Default is 'name'.
        :param points_col: The fantasy points column. Default is 'points'.
        :param position_col: The player position column. Default is 'position'.
        :param salary_col: The player salary column. Default is 'salary'.
        :param team_col: The player team column. Default is 'team'.
        :param datetime_col: The game datetime column. Default is 'datetime'.
        :param year_col: The dataframe year column. Default is 'year'.
        :param week_col: The dataframe week column. Default is 'week'.
        :param opponent_col: The dataframe opponent column. Default is 'opponent'.
        """
        self._data = data
        if not all(c in data.columns for c in [name_col, points_col, position_col, salary_col, team_col]):
            raise ValueError('DataFrame does not contain necessary columns')
        self._id_col = id_col
        self._name_col = name_col
        self._points_col = points_col
        self._position_col = position_col
        self._salary_col = salary_col
        self._team_col = team_col
        self._datetime_col = datetime_col
        self._year_col = year_col
        self._week_col = week_col
        self._opponent_col = opponent_col
        self._constraints = []

    @property
    def data(self):
        return self._data

    @property
    def id_col(self):
        return self._id_col

    @property
    def name_col(self):
        return self._name_col

    @property
    def points_col(self):
        return self._points_col

    @property
    def position_col(self):
        return self._position_col

    @property
    def salary_col(self):
        return self._salary_col

    @property
    def team_col(self):
        return self._team_col

    @property
    def datetime_col(self):
        return self._datetime_col

    @property
    def year_col(self):
        return self._year_col

    @property
    def week_col(self):
        return self._week_col

    @property
    def opponent_col(self):
        return self._opponent_col

    def set_only_include_teams(self, teams: List[str]) -> None:
        """
        Sets the teams that are to be considered for the lineup optimization.

        :param teams: The list of teams to consider.
        :return: None
        :raises: ValueError if teams to include is none or empty.
        """
        if teams is None or len(teams) == 0:
            raise ValueError('Included teams must not be none or empty')
        self._add_constraint(constraints.OnlyIncludeTeamsConstraint(teams=teams,
                                                                    team_column=self._team_col,
                                                                    lp_var_col=self._LP_VAR_COL))

    def set_exclude_teams(self, teams: List[str]) -> None:
        """
        Sets the list of teams whose players are to be excluded from lineup optimization.

        :param teams: The list of teams to exclude.
        :return: None
        :raises: ValueError if teams to exclude is none or empty.
        """
        if teams is None or len(teams) == 0:
            raise ValueError('Teams to exclude must not be none or empty')
        for team in teams:
            self.set_max_players_from_team(n=0, team=team)

    def set_must_include_team(self, team: str):
        """
        Specifies that a lineup must include a player from a given team.

        :param team: The team that the lineup must include.
        :return: None
        :raises: ValueError if team is none or not found in data frame.
        """
        self.set_min_players_from_team(n=1, team=team)

    def set_must_include_player(self, **kwargs) -> None:  # TODO: refactor following two methods for explicit id or name
        """
        Specifies that a lineup must include a player identified by either name or id.
        Either name or id must be provided in kwargs.

        :return: None
        :raises: ValueError if the player is None or not found in the dataframe
        """
        if all([it not in kwargs for it in ['id', 'name']]):
            raise ValueError('Must provide id or name')
        key, col = (kwargs['id'], self._id_col) if 'id' in kwargs else (kwargs['name'], self.name_col)
        if key is None or key not in self._data[col].unique():
            raise ValueError(f"{key} not found in data frame's {col} column")
        self._add_constraint(constraints.IncludePlayerConstraint(player=key,
                                                                 name_col=col,
                                                                 lp_var_col=self._LP_VAR_COL))

    def set_exclude_player(self, **kwargs) -> None:
        """
        Specifies that a lineup must exclude a player identified by name.

        :return: None
        :raises: ValueError if player is None or not found in dataframe
        """
        if all([it not in kwargs for it in ['id', 'name']]):
            raise ValueError('Must provide id or name')
        key, col = (kwargs['id'], self._id_col) if 'id' in kwargs else (kwargs['name'], self.name_col)
        if key is None or key not in self._data[col].unique():
            raise ValueError(f"{key} not found in data frame's {col} column")
        self._add_constraint(constraints.ExcludePlayerConstraint(player=key,
                                                                 name_col=col,
                                                                 lp_var_col=self._LP_VAR_COL))

    def set_num_players_from_team(self, n: int, team: str):
        """
        Sets the number of players from a team that an optimized lineup must include.

        :param n: the number of players
        :param team: the team name
        :return: None
        :raises: ValueError if number of players or team are invalid
        """
        if n is None or all([n > s.num_players() for s in list(sites.Site)]):
            raise ValueError('Invalid number of players')
        if team is None or team not in self._data[self._team_col].unique():
            raise ValueError('Invalid team name')
        self._add_constraint(constraints.MaxPlayersFromTeamConstraint(maximum=n,
                                                                      team=team,
                                                                      team_col=self._team_col,
                                                                      lp_var_col=self._LP_VAR_COL))
        try:
            self._add_constraint(constraints.MinPlayersFromTeamConstraint(minimum=n,
                                                                          team=team,
                                                                          team_col=self._team_col,
                                                                          lp_var_col=self._LP_VAR_COL))
        except InvalidConstraintException:
            self._constraints.pop()  # remove max players constraint if this one fails
            raise

    def set_max_players_from_team(self, n: int, team: str) -> None:
        """
        Sets the maximum number of players that can be included in an optimized lineup from a particular team.

        :param n: the maximum number of players that can be included from a particular team
        :param team: the name of the team
        :return: None
        :raises: ValueError if maximum or team are invalid
        """
        if n is None or n < 0:
            raise ValueError('Invalid maximum players')
        if team is None or team not in self._data[self._team_col].unique():
            raise ValueError('Invalid team name')
        self._add_constraint(constraints.MaxPlayersFromTeamConstraint(maximum=n,
                                                                      team=team,
                                                                      team_col=self._team_col,
                                                                      lp_var_col=self._LP_VAR_COL))

    def set_min_players_from_team(self, n: int, team: str) -> None:
        """
        Sets the minimum number of players from a given team that must be included in an optimized lineup.

        :param n: the minimum number of players from the specified team that must be included
        :param team: the name of the team
        :return: None
        :raises: ValueError if minimum or team are invalid
        """
        if n is None or all([n > s.num_players() for s in list(sites.Site)]):
            raise ValueError('Invalid minimum number of players')
        if team is None or team not in self._data[self._team_col].unique():
            raise ValueError('Invalid team name')
        if n == 0:
            return
        self._add_constraint(constraints.MinPlayersFromTeamConstraint(minimum=n,
                                                                      team=team,
                                                                      team_col=self._team_col,
                                                                      lp_var_col=self._LP_VAR_COL))

    def set_max_salary(self, n: int) -> None:
        """
        Sets the maximum salary that can be used in an optimized lineup.

        :param n: the max salary.
        :return: None
        :raises: ValueError if maximum is invalid
        """
        if n is None or n <= 0:
            raise ValueError('Invalid maximum')
        self._add_constraint(constraints.MaxSalaryCapConstraint(salary=n,
                                                                salary_col=self._salary_col,
                                                                lp_var_col=self._LP_VAR_COL))

    def set_min_salary(self, n: int) -> None:
        """
        Sets the minimum salary that can be used in an optimized lineup.

        :param n: the minimum salary
        :return: None
        :raises: ValueError if minimum is invalid
        """
        if n is None or all([n > s.salary_cap() for s in list(sites.Site)]):
            raise ValueError('Invalid minimum')
        self._add_constraint(constraints.MinSalaryCapConstraint(salary=n,
                                                                salary_col=self._salary_col,
                                                                lp_var_col=self._LP_VAR_COL))

    def set_qb_receiver_stack(self, team: str) -> None:
        """
        Specifies that an optimized lineup should include a QB/receiver stack from a given team.

        :param team: the team name
        :return: None
        :raises: ValueError if team name is invalid
        """
        if team not in self._data[self._team_col].unique():
            raise ValueError('Invalid team name')
        self._add_constraint(constraints.QbReceiverStackConstraint(lp_var_col=self._LP_VAR_COL,
                                                                   position_col=self._position_col,
                                                                   team=team,
                                                                   team_col=self._team_col))

    def set_rb_def_stack(self, team=None) -> None:
        raise NotImplementedError()

    def _add_constraint(self, constraint: constraints.LineupConstraint) -> None:
        """
        Internal method used to add a constraint by first checking if it is valid.

        :param constraint: The constraint to add.
        :return: None
        :raises: InvalidConstraintException if the constraint is not valid
        """
        is_valid, message = constraint.is_valid(self._constraints)
        if is_valid:
            self._constraints.append(constraint)
        else:
            raise InvalidConstraintException(f"Invalid constraint: {message}")

    def clear_constraints(self) -> None:
        """
        Clears the current lineup optimizer constraints.

        :return: None
        """
        self._constraints = []

    def optimize_lineup(self, site: Union[sites.Site, str], schedule_type: ScheduleType = None) -> OptimizedLineup:
        """
        Generates and returns an optimized lineup for a given fantasy football site.
        The lineup is generated using the class's data variable and is optimized under provided constraints.

        :param site: The fantasy site to generate a lineup for. Can be of type Site or str (full or abbreviation).
        :param schedule_type: The schedule type to optimize lineup for. Default is ALL.
        :return: The optimized lineup.
        :raises: ValueError, InvalidDataFrameException
        """
        if (type(site) is str and site.lower() in ('draftkings', 'dk')) or site == sites.Site.DRAFTKINGS:
            site = sites.Site.DRAFTKINGS
        elif (type(site) is str and site.lower() in ('fanduel', 'fd')) or site == sites.Site.FANDUEL:
            site = sites.Site.FANDUEL
        else:
            raise ValueError('The provided fantasy site is invalid')
        df = self._data.copy()
        if not df.index.dtype == 'int64':
            raise InvalidDataFrameException(('Only int64-type indices are currently supported. '
                                             'Consider calling reset_index() on data frame'))
        if not data_frame_utils.contains_all_columns(df, [self._points_col, self.position_col, self.salary_col]):
            raise InvalidDataFrameException(('The data frame is missing a required column. '
                                             'Please add this or update column names'))
        df[self.position_col] = df[self.position_col].apply(lambda x: positions.normalize_position(x))
        position_constraints = site.position_constraints()
        if not data_frame_utils.col_contains_all_values(df, self.position_col, position_constraints.keys()):
            raise InvalidDataFrameException('Data frame is missing required positions. '
                                            f"Required: {position_constraints.keys()}")
        df.dropna(subset=[self._points_col, self.salary_col], inplace=True)  # TODO: include more columns?
        if schedule_type is not None:
            df = df[df[self.datetime_col].apply(lambda x: schedule_type.matches(x))]  # filter data based on schedule
        df[self._LP_VAR_COL] = df.apply(lambda x: LpVariable(f"{x[self._position_col]}_{x.name}", cat='Binary'), axis=1)
        problem = LpProblem(f"{site.name()} Lineup Optimization", LpMaximize)
        for k, v in position_constraints.items():
            players = df[df[self._position_col] == k]
            problem += lpSum(players[self._LP_VAR_COL]) >= v[0]
            problem += lpSum(players[self._LP_VAR_COL]) <= v[1]
        problem += lpSum(df[self._points_col] * df[self._LP_VAR_COL])
        problem += constraints.LineupSizeConstraint(site.num_players(), self._LP_VAR_COL).apply(df)[0]
        problem += constraints.MaxSalaryCapConstraint(site.salary_cap(), self._salary_col, self._LP_VAR_COL).apply(df)[0]
        for constraint in self._constraints:
            for c in constraint.apply(df):  # stack-related constraints may return multiple from apply()
                problem += c
        problem.solve(PULP_CBC_CMD(msg=False))
        if not pulp_utils.is_optimal_solution_found(problem):
            raise UnsolvableLineupException('No optimal solution found under current lineup constraints')
        col_mappings = {self.name_col: 'name',
                        self._points_col: 'points',
                        self.position_col: 'position',
                        self.salary_col: 'salary',
                        self.team_col: 'team',
                        self.datetime_col: 'datetime',
                        self._year_col: 'year',
                        self._week_col: 'week',
                        self._opponent_col: 'opponent'}
        return OptimizedLineup(problem, data_frame_utils.map_cols_and_filter_by_values(df, col_mappings), site.name())

from typing import Any, Dict, List, Union

import pandas as pd
from pulp import LpMaximize, LpProblem, LpVariable, lpSum

from pygskin import constraints
from pygskin import positions, data_frame_utils, pulp_utils
from pygskin import sites
from pygskin.exceptions import InvalidDataFrameException, UnsolvableLineupException
from pygskin.schedule import ScheduleType


class OptimizedLineup:
    """
    A class that represents an optimized fantasy football lineup for a given site.
    """

    def __init__(self,
                 site: str,
                 points: float,
                 salary: int,
                 players: List[Dict[str, Any]],
                 index: List[int]):
        """
        :param site: The fantasy football site name.
        :param points: The points scored by the optimized lineup.
        :param salary: The salary used by the lineup.
        :param players: The players, represented as dicts, included in the lineup.
        :param index: The indices of the lineup players in the original data frame.
        """
        self.site = site
        self.points = round(points, 2)
        self.salary = salary
        self.players = players
        self.index = index

    def __repr__(self):
        return (f"pygskin.optimize.OptimizedLineup(site={self.site}, points={self.points}, salary={self.salary}, "
                f"players={self.players}, index={self.index})")

    def __str__(self):
        players_string = '\n'.join([f"{p['position'].value} - {p['name']} {p['points']} @ {p['salary']} salary"
                                    for p in self.players])
        return (f"Optimized {self.site} Lineup \n"
                f"{self.points} points @ {self.salary} salary \n") + players_string


class LineupOptimizer:
    """
    A pandas data frame-based fantasy football lineup optimizer.
    This class is used to generate optimal fantasy football lineups for various sites when provided
    a data frame containing player, position, salary and points information.
    """

    def __init__(self,
                 data: pd.DataFrame,
                 name_col: str = 'name',
                 points_col: str = 'points',
                 position_col: str = 'position',
                 salary_col: str = 'salary',
                 team_col: str = 'team',
                 datetime_col: str = 'datetime'):
        """
        :param data: The pandas data frame containing fantasy data.
        :param name_col: The player name column. Default is 'name'.
        :param points_col: The fantasy points column. Default is 'points'.
        :param position_col: The player position column. Default is 'position'.
        :param salary_col: The player salary column. Default is 'salary'.
        :param team_col: The player team column. Default is 'team'.
        :param datetime_col: The game datetime column. Default is 'datetime'.
        """
        self._data = data
        if not all(c in data.columns for c in [name_col, points_col, position_col, salary_col, team_col, datetime_col]):
            raise ValueError('DataFrame does not contain necessary columns')
        self._name_col = name_col
        self._points_col = points_col
        self._position_col = position_col
        self._salary_col = salary_col
        self._team_col = team_col
        self._datetime_col = datetime_col
        self._constraints = []

    @property
    def data(self):
        return self._data

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

    def only_include_teams(self, teams: List[str]):
        """
        Sets the teams that are to be considered for the lineup optimization.

        :param teams: The list of teams to consider.
        :raises: ValueError if teams to include is none or empty.
        """
        if teams is None or len(teams) == 0:
            raise ValueError('Included teams must not be none or empty')
        self._constraints.append(constraints.OnlyIncludeTeamsConstraint(teams, self._data, self._team_col))

    def optimize_lineup(self,
                        site: Union[sites.Site, str],
                        schedule_type: ScheduleType = None) -> OptimizedLineup:
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
        salaries = {}  # index/salary dicts mapped to position
        points = {}  # index/points dicts mapped to position
        for position in position_constraints.keys():
            players = df[df[self.position_col] == position]  # players for current position
            salaries[position] = data_frame_utils.map_index_to_col(players, self.salary_col)
            points[position] = data_frame_utils.map_index_to_col(players, self._points_col)
        position_to_index_dict = {k: LpVariable.dict(k.value, v, cat='Binary') for k, v in points.items()}
        problem = LpProblem(f"{site.name()} Lineup Optimization", LpMaximize)
        rewards = []
        for k, v in position_to_index_dict.items():
            rewards += lpSum([points[k][i] * position_to_index_dict[k][i] for i in v])  # sum player points
            constraints_for_position = position_constraints[k]
            problem += lpSum([position_to_index_dict[k][i] for i in v]) >= constraints_for_position[0]
            problem += lpSum([position_to_index_dict[k][i] for i in v]) <= constraints_for_position[1]
        index_to_variable_dict = data_frame_utils.merge_dicts(*position_to_index_dict.values())
        index_to_salary_dict = data_frame_utils.merge_dicts(*salaries.values())
        constraints.LineupSizeConstraint(site.num_players()).apply(problem, index_to_variable_dict)
        constraints.SalaryCapConstraint(site.salary_cap(), index_to_salary_dict).apply(problem, index_to_variable_dict)
        problem += lpSum(rewards)
        for constraint in self._constraints:
            constraint.apply(problem, index_to_variable_dict)
        problem.solve()
        column_mappings = {self.name_col: 'name',
                           self._points_col: 'points',
                           self.position_col: 'position',
                           self.salary_col: 'salary',
                           self.team_col: 'team',
                           self.datetime_col: 'datetime'}
        lineup = parse_lineup_from_problem(problem,
                                           data_frame_utils.map_cols_and_filter_by_values(df, column_mappings),
                                           site.name())
        return lineup


def parse_lineup_from_problem(problem: LpProblem, data: pd.DataFrame, site: str) -> OptimizedLineup:  # TODO: move this?
    if not pulp_utils.is_optimal_solution_found(problem):
        raise UnsolvableLineupException('No optimal solution found under current lineup constraints')
    index = [pulp_utils.int_index_from_lp_variable_name(p.name)
             for p in filter(lambda x: x.varValue == 1, problem.variables())]
    players = data.loc[index]
    points = players['points'].sum()
    salary = players['salary'].sum()
    return OptimizedLineup(site, points, salary, players.to_dict('records'), index)

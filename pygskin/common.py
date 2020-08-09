from abc import ABC, abstractmethod

from pulp import LpMaximize, LpProblem, LpVariable, lpSum

from pygskin import positions
from pygskin.exceptions import InvalidDataFrameException
from pygskin.util import data_frame_utils, pulp_utils


class LineupOptimizer(ABC):

    def __init__(self,
                 data,
                 name_col='name',
                 points_col='points',
                 position_col='position',
                 salary_col='salary',
                 team_col='team'):
        self.data = data
        self.name_col = name_col
        self.points_col = points_col
        self.position_col = position_col
        self.salary_col = salary_col
        self.team_col = team_col

    def optimize_lineup(self):
        df = self.data.copy()
        if not data_frame_utils.contains_all_columns(df, [self.points_col, self.position_col, self.salary_col]):
            raise InvalidDataFrameException(('The data frame is missing a required column. '
                                             'Please add this or update column names'))
        df[self.position_col] = df[self.position_col].apply(lambda x: positions.normalize_position(x))
        position_constraints = self.position_constraints()
        if not data_frame_utils.col_contains_all_values(df, self.position_col, position_constraints.keys()):
            raise InvalidDataFrameException('Data frame is missing required positions. '
                                            f"Required: {position_constraints.keys()}")
        df.dropna(subset=[self.points_col, self.salary_col], inplace=True)
        salaries = {}  # name/salary dicts mapped to position
        points = {}  # name/points dicts mapped to position
        for position in position_constraints.keys():
            players = df[df[self.position_col] == position]  # players for current position
            salaries[position] = data_frame_utils.map_index_to_col(players, self.salary_col)
            points[position] = data_frame_utils.map_index_to_col(players, self.points_col)
        _vars = {k: LpVariable.dict(k.value, v, cat='Binary') for k, v in points.items()}
        problem = LpProblem(f"{self.site()} Lineup Optimization", LpMaximize)
        costs, rewards = [], []
        for k, v in _vars.items():
            costs += lpSum([salaries[k][i] * _vars[k][i] for i in v])  # sum player salaries
            rewards += lpSum([points[k][i] * _vars[k][i] for i in v])  # sum player points
            constraints_for_position = position_constraints[k]
            problem += lpSum([_vars[k][i] for i in v]) >= constraints_for_position[0]  # min for position
            problem += lpSum([_vars[k][i] for i in v]) <= constraints_for_position[1]  # max for position
        total_players = []
        for k, v in _vars.items():
            total_players += lpSum([_vars[k][i] for i in v])
        problem += lpSum(total_players) == self.num_players()
        problem += lpSum(rewards)
        problem += lpSum(costs) <= self.salary_cap()
        problem.solve()
        lineup = parse_lineup_from_problem(problem, self._normalize_data_frame(df), self.site())
        print(repr(lineup))
        return lineup

    def _normalize_data_frame(self, df):
        column_mapping = {self.name_col: 'name',
                          self.points_col: 'points',
                          self.position_col: 'position',
                          self.salary_col: 'salary',
                          self.team_col: 'team'}
        df.rename(columns=column_mapping, inplace=True)
        return df[['name', 'points', 'position', 'salary', 'team']]

    @abstractmethod
    def position_constraints(self):
        pass

    @abstractmethod
    def num_players(self):
        pass

    @abstractmethod
    def salary_cap(self):
        pass

    @abstractmethod
    def site(self):
        pass


class OptimizedLineup:

    def __init__(self, site, points, salary, players, index):
        self.site = site
        self.points = points
        self.salary = salary
        self.players = players
        self.index = index

    def __repr__(self):
        return f"pygskin.common.LineupOptimizer(site={self.site}, points={self.points}, salary={self.salary}, players={self.players}, index={self.index})"

    def __str__(self):
        return f"Points: {self.points} Salary: {self.salary} Players: {self.players}"


def parse_lineup_from_problem(problem, data, site):
    index = [pulp_utils.index_from_lp_variable_name(p.name)
             for p in filter(lambda x: x.varValue == 1, problem.variables())]
    for i in index:
        print(data.loc[i])
    print(index)
    print(data.index)
    players = data.loc[index]
    points = players['points'].sum()
    salary = players['salary'].sum()
    return OptimizedLineup(site, points, salary, players.to_dict('records'), index)

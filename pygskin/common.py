from abc import ABC, abstractmethod
from pulp import LpMaximize, LpProblem, LpVariable, lpSum
from pygskin import positions
from pygskin.exceptions import InvalidDataFrameException
from pygskin.util import data_frame_utils


class LineupOptimizer(ABC):

    def __init__(self, data, name_col='name', points_col='points', position_col='position', salary_col='salary'):
        self.data = data
        self.name_col = name_col
        self.points_col = points_col
        self.position_col = position_col
        self.salary_col = salary_col

    def optimize_lineup(self):
        df = self.data.copy()
        if not data_frame_utils.contains_all_columns(df, [self.name_col, self.points_col, self.position_col, self.salary_col]):
            raise InvalidDataFrameException('The data frame is missing a required column. Please add this or update column names')
        df[self.position_col] = df[self.position_col].apply(lambda x: positions.normalize_position(x))
        position_constraints = self.position_constraints()
        if not data_frame_utils.col_contains_all_values(df, self.position_col, position_constraints.keys()):
            raise InvalidDataFrameException(f"Data frame is missing required positions. Required: {position_constraints.keys()}")
        df.dropna(subset=[self.points_col, self.salary_col], inplace=True)
        salaries = {}  # name/salary dicts mapped to position
        points = {}  # name/points dicts mapped to position
        for position in position_constraints.keys():
            players = df[df[self.position_col] == position]  # players for current position
            salaries[position] = data_frame_utils.dict_from_data_frame_columns(players, self.name_col, self.salary_col)
            points[position] = data_frame_utils.dict_from_data_frame_columns(players, self.name_col, self.points_col)
        _vars = {k: LpVariable.dict(k.value, v, cat='Binary') for k, v in points.items()}
        problem = LpProblem(self._problem_name(), LpMaximize)
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
        return parse_lineup_from_problem(problem)

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
    def _problem_name(self):
        pass


class OptimizedLineup:

    def __init__(self):
        self.points = 0
        self.salary = 0

    def __gt__(self, other):
        return self.points > other.points

    def __lt__(self, other):
        return self.points < other.points

    def __eq__(self, other):
        return self.points == other.points


def parse_lineup_from_problem(problem):
    lineup = OptimizedLineup()
    for p in problem.variables():
        if p.varValue == 1:
            print(p)
            print(vars(p))
    return lineup

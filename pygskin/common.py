from abc import ABC, abstractmethod
from pygskin.util import data_frame_utils
from pulp import LpMaximize, LpProblem, LpVariable, lpSum


class LineupOptimizer(ABC):

    def __init__(self, data, name_col='name', points_col='points', position_col='position', salary_col='salary'):
        self.data = data
        self.name_col = name_col
        self.points_col = points_col
        self.position_col = position_col
        self.salary_col = salary_col

    def optimize_lineup(self):
        df = self.data.dropna(subset=[self.points_col, self.salary_col])
        # if not data_frame_utils.col_contains_all_values(df, 'position', self.position_constraints().keys()):
        salaries = {}  # name/salary dicts mapped to position
        points = {}  # name/points dicts mapped to position
        for position in df[self.position_col].unique():
            players = df[df[self.position_col] == position]  # players for current position
            salaries[position] = data_frame_utils.dict_from_data_frame_columns(players, self.name_col, self.salary_col)
            print(salaries[position])
            points[position] = data_frame_utils.dict_from_data_frame_columns(players, self.name_col, self.points_col)
            print(points[position])
        _vars = {k: LpVariable.dict(k, v, cat='Binary') for k, v in points.items()}
        problem = LpProblem(self._problem_name(), LpMaximize)
        costs, rewards = [], []
        for k, v in _vars.items():
            costs += lpSum([salaries[k][i] * _vars[k][i] for i in v])  # sum player salaries
            rewards += lpSum([points[k][i] * _vars[k][i] for i in v])  # sum player points
            position_constraints = self.position_constraints()[k]
            problem += lpSum([_vars[k][i] for i in v]) >= position_constraints[0]  # min for position
            problem += lpSum([_vars[k][i] for i in v]) <= position_constraints[1]  # max for position
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
    return lineup

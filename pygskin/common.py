from abc import ABC, abstractmethod
from pygskin.util import data_frame_utils
from pulp import LpMaximize, LpProblem, LpVariable, lpSum


class LineupOptimizer(ABC):

    def __init__(self, data):
        self.data = data
        self.name_col = 'name'
        self.points_col = 'points'
        self.position_col = 'position'
        self.salary_col = 'salary'

    def optimize_lineup(self):
        self.data[self.points_col] = self.data[self.points_col].fillna(0)  # TODO: correct data
        self.data.dropna(subset=[self.salary_col], inplace=True)
        # if not data_frame_utils.col_contains_all_values(self.data, 'position', self.lineup_options()[0].keys()):
        salaries_for_position, points_for_position = {}, {}
        for position in self.data[self.position_col].unique():  # TODO: handle column overrides
            players_for_position = self.data[self.data[self.position_col] == position]
            salaries_for_position[position] = data_frame_utils\
                .dict_from_data_frame_columns(players_for_position, self.name_col, self.salary_col)
            points_for_position[position] = data_frame_utils\
                .dict_from_data_frame_columns(players_for_position, self.name_col, self.points_col)
        _vars = {k: LpVariable.dict(k, v, cat='Binary') for k, v in points_for_position.items()}
        max_lineup = None
        for lineup_option in self.lineup_options():
            problem = LpProblem(f"{self._problem_name()} Optimized Lineup", LpMaximize)
            costs, rewards = [], []
            for k, v in _vars.items():
                costs += lpSum([salaries_for_position[k][i] * _vars[k][i] for i in v])
                rewards += lpSum([points_for_position[k][i] * _vars[k][i] for i in v])
                problem += lpSum([_vars[k][i] for i in v]) <= lineup_option[k]
            problem += lpSum(rewards)
            problem += lpSum(costs) <= self.salary_cap()
            problem.solve()
            lineup = OptimizedLineup(problem)
            max_lineup = lineup if max_lineup is None else max(max_lineup, lineup)
            for p in problem.variables():
                if p.varValue == 1:
                    print(type(p))
                    print(p)
        return max_lineup

    @abstractmethod
    def lineup_options(self):
        pass

    @abstractmethod
    def salary_cap(self):
        pass

    @abstractmethod
    def _problem_name(self):
        pass


class OptimizedLineup:

    def __init__(self, problem):
        self.points = 0
        self.salary = 0

    def __gt__(self, other):
        return self.points > other.points

    def __lt__(self, other):
        return self.points < other.points

    def __eq__(self, other):
        return self.points == other.points

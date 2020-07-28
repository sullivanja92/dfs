from abc import ABC, abstractmethod
from pygskin.util import data_frame_utils
from pulp import LpMaximize, LpProblem, LpVariable, lpSum


class LineupOptimizer(ABC):

    data_columns = {
        'name_col': 'name',
        'position_col': 'position',
        'team_col': 'team',
        'opponent_col': 'opponent',
        'year_col': 'year',
        'week_col': 'week',
        'salary_col': 'salary',
        'points_col': 'points'
    }

    def __init__(self):
        self.data = None
        self.column_overrides = None

    def set_data(self, data, column_overrides=None):
        if self._is_data_valid(data, column_overrides):
            self.data = data
            self.column_overrides = column_overrides

    def _is_data_valid(self, data, column_overrides):
        return True

    def optimize_lineup(self):
        self.data['dk_points'] = self.data['dk_points'].fillna(0)  # TODO: correct data
        self.data.dropna(subset=['dk_salary'], inplace=True)
        if not data_frame_utils.col_contains_all_values(self.data, 'position', self.lineup_options()[0].keys()):
            pass
        salaries_for_position, points_for_position = {}, {}
        for position in self.data[self.data_columns['position_col']].unique():  # TODO: handle column overrides
            players_for_position = self.data[self.data[self.data_columns['position_col']] == position]
            salaries_for_position[position] = data_frame_utils.data_frame_to_dict(players_for_position, 'name', 'dk_salary')
            points_for_position[position] = data_frame_utils.data_frame_to_dict(players_for_position, 'name', 'dk_points')
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

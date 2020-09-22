from abc import ABC, abstractmethod
from typing import Dict

from pulp import LpProblem, LpVariable, lpSum

from pygskin import data_frame_utils


class LineupConstraint(ABC):
    """
    Abstract base class representing a fantasy lineup constraint.
    """

    @abstractmethod
    def apply(self, problem: LpProblem, index_to_lp_variable_dict: Dict[int, LpVariable]) -> None:
        """
        Applies the given constraint with args provided in constructor.

        :param problem: The LP Problem variable for which to apply the rule.
        :param index_to_lp_variable_dict: The player index to lp variable mapping.
        :return: None
        """
        pass


class LineupSizeConstraint(LineupConstraint):
    """
    A constraint based on the number of players allowed in a lineup.
    """

    def __init__(self, size: int):
        """
        :param size: The size of the lineup
        """
        self.size = size

    def apply(self, problem: LpProblem, index_to_lp_variable_dict: Dict[int, LpVariable]) -> None:
        """
        Takes the sum of players included in a lineup and returns whether that is equal to the required lineup size.

        :param problem: The LP Problem variable for which to apply the rule.
        :param index_to_lp_variable_dict: The player index to lp variable mapping.
        :return: None
        """
        problem += lpSum(index_to_lp_variable_dict.values()) == self.size


class SalaryCapConstraint(LineupConstraint):
    """
    A salary cap-based constraint.
    """

    def __init__(self, salary_cap: int,
                 index_to_salary_dict: Dict[int, int]):
        """
        :param salary_cap: The salary cap.
        :param index_to_salary_dict:  A dict containing index to salary mappings.
        """
        self.salary_cap = salary_cap
        self.index_to_salary_dict = index_to_salary_dict

    def apply(self, problem: LpProblem, index_to_lp_variable_dict: Dict[int, LpVariable]) -> None:
        """
        Takes the sum of included player salaries and compares that to the salary cap.

        :param problem: The LP Problem variable for which to apply the rule.
        :param index_to_lp_variable_dict: The player index to lp variable mapping.
        :return: None
        """
        costs = [self.index_to_salary_dict[i] * index_to_lp_variable_dict[i]
                 for i in index_to_lp_variable_dict.keys()]
        problem += lpSum(costs) <= self.salary_cap


class OnlyIncludeTeamsConstraint(LineupConstraint):
    """
    A constraint used to only consider players for a list of teams.
    """

    def __init__(self, teams_to_include, data, team_column):
        """
        :param teams_to_include: The list of teams to consider.
        :param data: The player data frame.
        :param team_column: The data frame's team column label.
        """
        self.teams_to_include = teams_to_include
        self.data = data
        self.team_column = team_column

    def apply(self, problem: LpProblem, index_to_lp_variable_dict: Dict[int, LpVariable]) -> None:
        """
        Checks that players who do not play for one of the specified teams are not included in the lineup.

        :param problem: The LP Problem variable for which to apply the rule.
        :param index_to_lp_variable_dict: The player index to lp variable mapping.
        :return: None
        """
        index_to_team_dict = data_frame_utils.map_index_to_col(self.data, self.team_column)
        for k, v in index_to_lp_variable_dict.items():
            if index_to_team_dict[k] not in self.teams_to_include:
                problem += v == 0

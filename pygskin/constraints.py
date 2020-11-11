from abc import ABC, abstractmethod
from typing import Dict, List

import pandas as pd
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

    @abstractmethod
    def is_valid(self, constraints: List['LineupConstraint']) -> bool:  # TODO: return tuple (bool, message)
        """
        Checks whether the given lineup constraint can be added to a lineup optimizer based on current constraints.

        :param constraints: The list of constraints to validate against.
        :return: A bool indicating whether the lineup can be added.
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

    def is_valid(self, constraints: List['LineupConstraint']) -> bool:
        """
        Checks whether the given lineup constraint can be added to a lineup optimizer based on current constraints.
        This will always return True.

        :param constraints: The list of constraints to validate against.
        :return: A bool indicating whether the lineup can be added.
        """
        return True


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

    def is_valid(self, constraints: List['LineupConstraint']) -> bool:
        """
        Checks whether the given lineup constraint can be added to a lineup optimizer based on current constraints.
        This will always return True.

        :param constraints: The list of constraints to validate against.
        :return: A bool indicating whether the lineup can be added.
        """
        return True


class OnlyIncludeTeamsConstraint(LineupConstraint):  # TODO: parent class for teams-related constraints
    """
    A constraint used to only consider players for a list of teams.
    """

    def __init__(self, teams: List[str], data: pd.DataFrame, team_column: str):
        """
        :param teams: The list of teams to consider.
        :param data: The player data frame.
        :param team_column: The data frame's team column label.
        """
        self.teams = teams
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
            if index_to_team_dict[k] not in self.teams:
                problem += v == 0

    def is_valid(self, constraints: List['LineupConstraint']) -> bool:
        """
        Checks whether the given lineup constraint can be added to a lineup optimizer based on current constraints.
        This method will check whether any constraints exist which exclude a team that is to be considered.

        :param constraints: The list of constraints to validate against.
        :return: A bool indicating whether the lineup can be added.
        """
        for constraint in constraints:
            if type(constraint) is ExcludeTeamsConstraint:
                if any([t in constraint.teams for t in self.teams]):  # check if any teams to consider are excluded
                    return False
        return True


class ExcludeTeamsConstraint(LineupConstraint):
    """
    A constraint used to exclude players who play for specified teams.
    """

    def __init__(self, teams: List[str], data: pd.DataFrame, team_column: str):
        """
        :param teams: The list of teams to exclude from consideration.
        :param data: The player data frame.
        :param team_column: The data frame's team column label.
        """
        self.teams = teams
        self.data = data
        self.team_column = team_column

    def apply(self, problem: LpProblem, index_to_lp_variable_dict: Dict[int, LpVariable]) -> None:
        """
        Checks that players who play for one of the specified teams are not included in the lineup.

        :param problem: The LP Problem variable for which to apply the rule.
        :param index_to_lp_variable_dict: The player index to lp variable mapping.
        :return: None
        """
        index_to_team_dict = data_frame_utils.map_index_to_col(self.data, self.team_column)
        for k, v in index_to_lp_variable_dict.items():
            if index_to_team_dict[k] in self.teams:
                problem += v == 0

    def is_valid(self, constraints: List['LineupConstraint']) -> bool:
        """
        Checks whether the given lineup constraint can be added to a lineup optimizer based on current constraints.
        This method will check whether any constraints exist which include a team that is to be excluded.

        :param constraints: The list of constraints to validate against.
        :return: A bool indicating whether the lineup can be added.
        """
        for constraint in constraints:
            if type(constraint) is OnlyIncludeTeamsConstraint:
                if any([t in constraint.teams for t in self.teams]):  # check if any teams to exclude are included
                    return False
        return True


class MustIncludeTeamConstraint(LineupConstraint):
    """
    A constraint used to specify that an optimized lineup must include at least one player from a given team.
    """

    def __init__(self, team: str, data: pd.DataFrame, team_column: str):
        """
        :param team: The team that must be included.
        :param data: The player data frame.
        :param team_column: The team column label.
        """
        self.team = team
        self.data = data
        self.team_column = team_column

    def apply(self, problem: LpProblem, index_to_lp_variable_dict: Dict[int, LpVariable]) -> None:
        """
        Checks that at least one player from the specified team is included in the lineup.

        :param problem: The LP Problem variable.
        :param index_to_lp_variable_dict: The mapping of index to lp variable.
        :return: None
        """
        index_to_team_dict = data_frame_utils.map_index_to_col(self.data, self.team_column)
        lp_vars_for_team = []
        for k, v in index_to_lp_variable_dict.items():
            if index_to_team_dict[k] == self.team:
                lp_vars_for_team.append(v)
        problem += lpSum(lp_vars_for_team) >= 1

    def is_valid(self, constraints: List['LineupConstraint']) -> bool:
        """
        Checks whether or not a constraint to exclude the specified team already exists.

        :param constraints: The list of lineup constraints.
        :return: False if a constraint to exclude the specified team exists.
        """
        for constraint in constraints:
            if type(constraint) is ExcludeTeamsConstraint:
                if self.team in constraint.teams:
                    return False
        return True


class IncludePlayerConstraint(LineupConstraint):

    def apply(self, problem: LpProblem, index_to_lp_variable_dict: Dict[int, LpVariable]) -> None:
        pass

    def is_valid(self, constraints: List['LineupConstraint']) -> bool:
        pass


class ExcludePlayerConstraint(LineupConstraint):

    def apply(self, problem: LpProblem, index_to_lp_variable_dict: Dict[int, LpVariable]) -> None:
        pass

    def is_valid(self, constraints: List['LineupConstraint']) -> bool:
        pass

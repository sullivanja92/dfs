from abc import ABC, abstractmethod
from typing import Dict, List, Tuple, Optional

import pandas as pd
from pulp import LpVariable, lpSum, LpAffineExpression

from dfs import data_frame_utils


class LineupConstraint(ABC):
    """
    Abstract base class representing a fantasy lineup constraint.
    """

    @abstractmethod
    def apply(self, index_to_lp_variable_dict: Dict[int, LpVariable]) -> LpAffineExpression:
        """
        Applies the given constraint with args provided in constructor.

        :param index_to_lp_variable_dict: The player index to lp variable mapping.
        :return: An LpAffineExpression to be added to the LpProblem.
        """
        pass

    @abstractmethod
    def is_valid(self, constraints: List['LineupConstraint']) -> Tuple[bool, Optional[str]]:
        """
        Checks whether the given lineup constraint can be added to a lineup optimizer based on current constraints.

        :param constraints: The list of constraints to validate against.
        :return: A bool indicating whether or not the constraint is valid and a message, if appropriate.
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

    def apply(self, index_to_lp_variable_dict: Dict[int, LpVariable]) -> LpAffineExpression:
        """
        Takes the sum of players included in a lineup and returns whether that is equal to the required lineup size.

        :param index_to_lp_variable_dict: The player index to lp variable mapping.
        :return: An LpAffineExpression to be added to the LpProblem.
        """
        return lpSum(index_to_lp_variable_dict.values()) == self.size

    def is_valid(self, constraints: List['LineupConstraint']) -> Tuple[bool, Optional[str]]:
        """
        Checks whether the given lineup constraint can be added to a lineup optimizer based on current constraints.
        This will always return True.

        :param constraints: The list of constraints to validate against.
        :return: A bool indicating whether or not the constraint is valid and a message, if appropriate.
        """
        return True, None


class MaxSalaryCapConstraint(LineupConstraint):
    """
    A constraint to specify an upper bound on an optimized lineup's total salary.
    """

    def __init__(self, salary: int, data: pd.DataFrame, salary_col: str):
        """
        Constructor
        :param salary: The max salary.
        :param data: The player data frame.
        :param salary_col: The name of the data frame's salary column.
        """
        self.salary = salary
        self.data = data
        self.salary_col = salary_col

    def apply(self, index_to_lp_variable_dict: Dict[int, LpVariable]) -> LpAffineExpression:
        """
        Applies the given constraint with args provided in constructor.

        :param index_to_lp_variable_dict: The player index to lp variable mapping.
        :return: An LpAffineExpression to be added to the LpProblem.
        """
        index_to_salary_dict = data_frame_utils.map_index_to_col(self.data, self.salary_col)
        costs = [index_to_salary_dict[k] * v for k, v in index_to_lp_variable_dict.items()]
        return lpSum(costs) <= self.salary

    def is_valid(self, constraints: List['LineupConstraint']) -> Tuple[bool, Optional[str]]:
        """
        This method will return False if any of the below conditions are met:
        1. Constraints already includes a MinSalaryCapConstraint with a salary that's greater than this salary.

        :param constraints:
        :return: A bool indicating whether or not the constraint is valid and a message, if appropriate.
        """
        for constraint in constraints:
            if type(constraint) is MinSalaryCapConstraint:
                if constraint.salary > self.salary:
                    return False, 'A min-salary constraint with value greater than this is already included.'
        return True, None


class MinSalaryCapConstraint(LineupConstraint):
    """
    A constraint to specify a lower bound on an optimized lineup's total salary.
    """

    def __init__(self, salary: int, data: pd.DataFrame, salary_col: str):
        self.salary = salary
        self.data = data
        self.salary_col = salary_col

    def apply(self, index_to_lp_variable_dict: Dict[int, LpVariable]) -> LpAffineExpression:
        """
        Applies the given constraint with args provided in constructor.

        :param index_to_lp_variable_dict: The player index to lp variable mapping.
        :return: An LpAffineExpression to be added to the LpProblem.
        """
        index_to_salary_dict = data_frame_utils.map_index_to_col(self.data, self.salary_col)
        costs = [index_to_salary_dict[k] * v for k, v in index_to_lp_variable_dict.items()]
        return lpSum(costs) >= self.salary

    def is_valid(self, constraints: List['LineupConstraint']) -> Tuple[bool, Optional[str]]:
        """
        This method will return False if any of the below conditions are met:
        1. Constraints already includes a MaxSalaryCapConstraint with a salary that's less than this salary.

        :param constraints:
        :return: A bool indicating whether or not the constraint is valid and a message, if appropriate.
        """
        for constraint in constraints:
            if type(constraint) is MaxSalaryCapConstraint:
                if constraint.salary < self.salary:
                    return False, 'A max-salary constraint with value less than this is already included.'
        return True, None


class OnlyIncludeTeamsConstraint(LineupConstraint):
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

    def apply(self, index_to_lp_variable_dict: Dict[int, LpVariable]) -> LpAffineExpression:
        """
        Checks that players who do not play for one of the specified teams are not included in the lineup.

        :param index_to_lp_variable_dict: The player index to lp variable mapping.
        :return: An LpAffineExpression to be added to the LpProblem.
        """
        index_to_team_dict = data_frame_utils.map_index_to_col(self.data, self.team_column)
        lp_variables_to_exclude = []
        for k, v in index_to_lp_variable_dict.items():
            if index_to_team_dict[k] not in self.teams:
                # problem += v == 0
                lp_variables_to_exclude.append(v)
        return lpSum(lp_variables_to_exclude) == 0

    def is_valid(self, constraints: List['LineupConstraint']) -> Tuple[bool, Optional[str]]:
        """
        Returns false if any of the below conditions are satisfied:
        1. A MaxPlayersFromConstraint with max set to 0 (teams are excluded) for every team in this constraint.

        :param constraints: the list of existing lineup constraints
        :return: True if the constraint is valid
        """
        excluded = {k: False for k in self.teams}
        for constraint in constraints:
            if type(constraint) is MaxPlayersFromTeamConstraint:
                if constraint.team in excluded.keys() and constraint.maximum == 0:
                    excluded[constraint.team] = True
        if all(excluded.values()):
            return False, 'All teams on the list to include are already excluded'
        else:
            return True, None


class IncludePlayerConstraint(LineupConstraint):
    """
    A constraint used to specify that an optimized lineup must contain a specified player.
    """

    def __init__(self, player: str, data: pd.DataFrame, name_col: str):
        """
        Constructor
        :param player: the player's name or id
        :param data: the player data frame
        :param name_col: the name or id column
        """
        self.player = player
        self.data = data
        self.name_col = name_col

    def apply(self, index_to_lp_variable_dict: Dict[int, LpVariable]) -> LpAffineExpression:
        """
        Applies the constraint by ensuring that the lineup includes the specified player.

        :param index_to_lp_variable_dict: the index to lp variable dict
        :return: An LpAffineExpression to be added to the LpProblem.
        """
        index_to_name_dict = data_frame_utils.map_index_to_col(self.data, self.name_col)
        lp_vars_for_name = []  # if multiple players with same name
        for k, v in index_to_lp_variable_dict.items():
            if index_to_name_dict[k] == self.player:
                lp_vars_for_name.append(v)
        return lpSum(lp_vars_for_name) >= 1

    def is_valid(self, constraints: List['LineupConstraint']) -> Tuple[bool, Optional[str]]:
        """
        Returns False if any of the below conditions are met:
        1. This player is already excluded via an ExcludePlayerConstraint

        :param constraints: the list of lineup constraints
        :return: a bool indicating whether the constraint is valid and a message, if appropriate
        """
        for constraint in constraints:
            if type(constraint) is ExcludePlayerConstraint:
                if self.player == constraint.player:
                    return False, 'This player is already set to be excluded from lineup'
        return True, None


class ExcludePlayerConstraint(LineupConstraint):
    """
    A constraint used to specify that a certain player must be excluded from an optimized lineup.
    """

    def __init__(self, player: str, data: pd.DataFrame, name_col: str):
        """
        Constructor
        :param player: the player name or id
        :param data: the player data frame
        :param name_col: the name or id column
        """
        self.player = player
        self.data = data
        self.name_col = name_col

    def apply(self, index_to_lp_variable_dict: Dict[int, LpVariable]) -> LpAffineExpression:
        """
        Applies the constraint by ensuring that the lineup excludes the specified player.

        :param index_to_lp_variable_dict: the index to lp variable dict
        :return: An LpAffineExpression to be added to the LpProblem.
        """
        index_to_name_dict = data_frame_utils.map_index_to_col(self.data, self.name_col)
        lp_vars_for_name = []  # if multiple players with same name
        for k, v in index_to_lp_variable_dict.items():
            if index_to_name_dict[k] == self.player:
                lp_vars_for_name.append(v)
        return lpSum(lp_vars_for_name) == 0

    def is_valid(self, constraints: List['LineupConstraint']) -> Tuple[bool, Optional[str]]:
        """
        Returns False if any of the below conditions are met:
        1. This player is already included via an IncludePlayerConstraint

        :param constraints: the list of lineup constraints
        :return: a bool indicating whether the constraint is valid and a message, if appropriate
        """
        for constraint in constraints:
            if type(constraint) is IncludePlayerConstraint:
                if self.player == constraint.player:
                    return False, 'This player is already set to be included in lineup'
        return True, None


class MaxPlayersFromTeamConstraint(LineupConstraint):
    """
    A constraint specifying that an optimized lineup may contain a maximum number of players from a given team.
    """

    def __init__(self, maximum: int, team: str, data: pd.DataFrame, team_col: str):
        """
        Constructor
        :param maximum: the maximum number of players
        :param team: the name of the team
        :param data: the player data frame
        :param team_col: the name of the team column
        """
        self.maximum = maximum
        self.team = team
        self.data = data
        self.team_col = team_col

    def apply(self, index_to_lp_variable_dict: Dict[int, LpVariable]) -> LpAffineExpression:
        """
        Applies the constraint by ensuring the number of included players from the team is less than the maximum.

        :param index_to_lp_variable_dict: the index to lp variable dict
        :return: An LpAffineExpression to be added to the LpProblem.
        """
        index_to_team_dict = data_frame_utils.map_index_to_col(self.data, self.team_col)
        lp_vars_for_team = []
        for k, v in index_to_lp_variable_dict.items():
            if index_to_team_dict[k] == self.team:
                lp_vars_for_team.append(v)
        return lpSum(lp_vars_for_team) <= self.maximum

    def is_valid(self, constraints: List['LineupConstraint']) -> Tuple[bool, Optional[str]]:
        """
        Returns False if any of the below conditions are met:
        1. A MaxPlayersFromTeamConstraint for this team is already included in the list of constraints
        2. A MinPlayersFromTeamConstraint with minimum greater than this maximum is already included

        :param constraints: the list of lineup constraints
        :return: a bool indicating whether or not the constraint is valid and a message, if appropriate
        """
        for constraint in constraints:
            if type(constraint) is MaxPlayersFromTeamConstraint:
                if constraint.team == self.team:
                    return False, 'Max players from this team already set'
            if type(constraint) is MinPlayersFromTeamConstraint:
                if constraint.team == self.team and constraint.minimum > self.maximum:
                    return False, 'Min players from this team already set to a value greater than this maximum'
        return True, None


class MinPlayersFromTeamConstraint(LineupConstraint):
    """
    A constraint specifying that an optimized lineup must contain a minimum number of players from a given team.
    """

    def __init__(self, minimum: int, team: str, data: pd.DataFrame, team_col: str):
        """
        Constructor
        :param minimum: the minimum number of players from the team that must be included
        :param team: the name of the team
        :param data: the player data frame
        :param team_col: the data frame's team column name
        """
        self.minimum = minimum
        self.team = team
        self.data = data
        self.team_col = team_col

    def apply(self, index_to_lp_variable_dict: Dict[int, LpVariable]) -> LpAffineExpression:
        """
        Applies the constraint.

        :param index_to_lp_variable_dict: the index to lp variable dict
        :return: An LpAffineExpression to be added to the LpProblem.
        """
        index_to_team_dict = data_frame_utils.map_index_to_col(self.data, self.team_col)
        lp_vars_for_team = []
        for k, v in index_to_lp_variable_dict.items():
            if index_to_team_dict[k] == self.team:
                lp_vars_for_team.append(v)
        return lpSum(lp_vars_for_team) >= self.minimum

    def is_valid(self, constraints: List['LineupConstraint']) -> Tuple[bool, Optional[str]]:
        """
        Returns false if any of the below conditions are satisfied:
        1. A MinPlayersFromTeamConstraint is already included for this team
        2. A MaxPlayersFromTeamConstraint is already included for this team with value less than this minimum

        :param constraints: the list of existing lineup constraints
        :return: a bool indicating whether or not the constraint is valid and a message, if appropriate
        """
        for constraint in constraints:
            if type(constraint) is MinPlayersFromTeamConstraint:
                if constraint.team == self.team:
                    return False, 'Min players from this team already set'
            if type(constraint) is MaxPlayersFromTeamConstraint:
                if constraint.team == self.team and constraint.maximum < self.minimum:
                    return False, 'Max players from this team already set to a value less than this minimum'
        return True, None

from abc import ABC, abstractmethod
from typing import List, Tuple, Optional

import pandas as pd
from pulp import lpSum, LpAffineExpression

from dfs.positions import QB, RB, WR, TE, DST
from dfs.slate import GameSlate


class LineupConstraint(ABC):
    """
    Abstract base class representing a fantasy lineup constraint.
    """

    @abstractmethod
    def apply(self, data: pd.DataFrame) -> List[LpAffineExpression]:
        """
        Applies the given constraint with arguments provided in constructor.

        :return: An LpAffineExpression to be added to the LpProblem.
        """
        pass

    @abstractmethod
    def is_valid(self, constraints: List['LineupConstraint']) -> Tuple[bool, Optional[str]]:
        """
        Checks whether the given lineup constraint can be added to a lineup optimizer based on current constraints.

        :param constraints: The list of constraints to validate against.
        :return: A bool indicating whether or not the constraint is valid and an error message, if appropriate.
        """
        pass


class LineupSizeConstraint(LineupConstraint):
    """
    A constraint based on the number of players allowed in a lineup.
    """

    def __init__(self, size: int):
        """
        Constructor

        :param size: The size of the lineup
        """
        super().__init__()
        self.size = size

    def apply(self, data: pd.DataFrame) -> List[LpAffineExpression]:
        """
        Takes the sum of players included in a lineup and returns whether that is equal to the required lineup size.

        :return: An LpAffineExpression to be added to the LpProblem.
        """
        return [lpSum(data['LpVariable']) == self.size]

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

    def __init__(self, salary: int, salary_col: str):
        """
        Constructor

        :param salary: The max salary.
        :param salary_col: The name of the data frame's salary column.
        """
        super().__init__()
        self.salary = salary
        self.salary_col = salary_col

    def apply(self, data: pd.DataFrame) -> List[LpAffineExpression]:
        """
        Applies the given constraint with args provided in constructor.

        :return: An LpAffineExpression to be added to the LpProblem.
        """
        return [lpSum(data[self.salary_col] * data['LpVariable']) <= self.salary]

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

    def __init__(self, salary: int, salary_col: str):
        """
        Constructor

        :param salary: The min salary.
        :param salary_col: The name of the data frame's salary column.
        """
        super().__init__()
        self.salary = salary
        self.salary_col = salary_col

    def apply(self, data: pd.DataFrame) -> List[LpAffineExpression]:
        """
        Applies the given constraint with args provided in constructor.

        :return: An LpAffineExpression to be added to the LpProblem.
        """
        return [lpSum(data[self.salary_col] * data['LpVariable']) >= self.salary]

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

    def __init__(self, teams: List[str], team_column: str):
        """
        Constructor

        :param teams: The list of teams to consider.
        :param team_column: The data frame's team column label.
        """
        super().__init__()
        self.teams = teams
        self.team_column = team_column

    def apply(self, data: pd.DataFrame) -> List[LpAffineExpression]:
        """
        Checks that players who do not play for one of the specified teams are not included in the lineup.

        :return: An LpAffineExpression to be added to the LpProblem.
        """
        return [lpSum(data[~data[self.team_column].isin(self.teams)]['LpVariable']) == 0]

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

    def __init__(self, player: str, name_col: str):
        """
        Constructor

        :param player: the player's name or id
        :param name_col: the name or id column
        """
        super().__init__()
        self.player = player
        self.name_col = name_col

    def apply(self, data: pd.DataFrame) -> List[LpAffineExpression]:
        """
        Applies the constraint by ensuring that the lineup includes the specified player.

        :return: An LpAffineExpression to be added to the LpProblem.
        """
        return [lpSum(data[data[self.name_col] == self.player]['LpVariable']) >= 1]

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

    def __init__(self, player: str, name_col: str):
        """
        Constructor

        :param player: the player name or id
        :param name_col: the name or id column
        """
        super().__init__()
        self.player = player
        self.name_col = name_col

    def apply(self, data: pd.DataFrame) -> List[LpAffineExpression]:
        """
        Applies the constraint by ensuring that the lineup excludes the specified player.

        :return: An LpAffineExpression to be added to the LpProblem.
        """
        return [lpSum(data[data[self.name_col] == self.player]['LpVariable']) == 0]

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

    def __init__(self, maximum: int, team: str, team_col: str):
        """
        Constructor

        :param maximum: the maximum number of players
        :param team: the name of the team
        :param team_col: the name of the team column
        """
        super().__init__()
        self.maximum = maximum
        self.team = team
        self.team_col = team_col

    def apply(self, data: pd.DataFrame) -> List[LpAffineExpression]:
        """
        Applies the constraint by ensuring the number of included players from the team is less than the maximum.

        :return: An LpAffineExpression to be added to the LpProblem.
        """
        return [lpSum(data[data[self.team_col] == self.team]['LpVariable']) <= self.maximum]

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

    def __init__(self, minimum: int, team: str, team_col: str):
        """
        Constructor

        :param minimum: the minimum number of players from the team that must be included
        :param team: the name of the team
        :param team_col: the data frame's team column name
        """
        super().__init__()
        self.minimum = minimum
        self.team = team
        self.team_col = team_col

    def apply(self, data: pd.DataFrame) -> List[LpAffineExpression]:
        """
        Applies the constraint.

        :return: An LpAffineExpression to be added to the LpProblem.
        """
        return [lpSum(data[data[self.team_col] == self.team]['LpVariable']) >= self.minimum]

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


class QbReceiverStackConstraint(LineupConstraint):
    """
    A constraint specifying that an optimized lineup must contain a QB/receiver stack from a given team.
    """

    def __init__(self, position_col: str, team: str, team_col: str, position: str = None, num_receivers: int = None):
        """
        Constructor

        :param position_col: the name of the position column
        :param team: the name of the team
        :param team_col: the name of the team column
        :param position: the receiver position (this is optional)
        :param num_receivers: the number of receivers to include in the stack.
        """
        super().__init__()
        self.position_col = position_col
        self.team = team
        self.team_col = team_col
        self.position = position
        self.num_receivers = num_receivers

    def apply(self, data: pd.DataFrame) -> List[LpAffineExpression]:
        """
        Applies the constraint.

        :return: An LpAffineExpression to be added to the LpProblem.
        """
        positions = [self.position] if self.position is not None else [WR, TE]
        n = 1 if self.num_receivers is None else self.num_receivers
        return [lpSum(data[(data[self.team_col] == self.team) & (data[self.position_col] == QB)]['LpVariable']) >= 1,
                lpSum(data[(data[self.team_col] == self.team) & (data[self.position_col].isin(positions))]['LpVariable']) >= n]

    def is_valid(self, constraints: List['LineupConstraint']) -> Tuple[bool, Optional[str]]:
        """
        Returns false if any of the below conditions are satisfied:
        1. A QbReceiverStackConstraint is already included
        2. A MaxPlayersFromTeamConstraint is already included for this team with value less than two

        :param constraints: the list of existing lineup constraints
        :return: a bool indicating whether or not the constraint is valid and a message, if appropriate
        """
        for constraint in constraints:
            if type(constraint) is QbReceiverStackConstraint:
                return False, 'A QB/receiver stack is already included for this lineup'
            elif type(constraint) is MaxPlayersFromTeamConstraint:
                if constraint.team == self.team and constraint.maximum < 2:
                    return False, f"Max players from {self.team} is already set to {constraint.maximum}"
        return True, None


class RbDstStackConstraint(LineupConstraint):
    """
    A constraint specifying that an optimized lineup must contain a RB/DST stack from a given team.
    """

    def __init__(self, team: str, team_col: str, position_col: str):
        """
        Initializer

        :param team: the name of the team for which to include this stack
        :param team_col: the name of the dataframe's team column
        :param position_col: the name of the dataframe's position column
        """
        super().__init__()
        self.team = team
        self.team_col = team_col
        self.position_col = position_col

    def apply(self, data: pd.DataFrame) -> List[LpAffineExpression]:
        """
        Applies the constraint.

        :param data: the player data frame.
        :return: An LpAffineExpression to be added to the LpProblem.
        """
        return [lpSum(data[(data[self.team_col] == self.team) & (data[self.position_col] == RB)]['LpVariable']) >= 1,
                lpSum(data[(data[self.team_col] == self.team) & (data[self.position_col] == DST)]['LpVariable']) == 1]

    def is_valid(self, constraints: List['LineupConstraint']) -> Tuple[bool, Optional[str]]:
        """
        Returns false if any of the below conditions are satisfied:
        1. A RbDstStackConstraint is already included
        2. A MaxPlayersFromTeamConstraint is already included for this team with value less than two

        :param constraints: the list of existing lineup constraints
        :return: a bool indicating whether or not the constraint is valid and a message, if appropriate
        """
        for constraint in constraints:
            if type(constraint) is RbDstStackConstraint:
                return False, 'An RB/DST stack constraint is already included for this lineup'
            elif type(constraint) is MaxPlayersFromTeamConstraint:
                if constraint.team == self.team and constraint.maximum < 2:
                    return False, f"Max players from {self.team} is already set to {constraint.maximum}"
        return True, None


class GameSlateConstraint(LineupConstraint):
    """
    A constraint specifying that an optimized lineup should only include players from a specified game slate.
    """

    def __init__(self, slate: GameSlate, datetime_col: str, week_col: str, num_players: int):
        """
        Initializer

        :param slate: the game slate to include
        :param datetime_col: the name of the dataframe's team column
        :param week_col: the name of the dataframe's week column (required for Monday/Thursday slate)
        :param num_players: the number of players to include in an optimized lineup
        """
        super().__init__()
        self.slate = slate
        self.datetime_col = datetime_col
        self.week_col = week_col
        self.num_players = num_players

    def apply(self, data: pd.DataFrame) -> List[LpAffineExpression]:
        """
        Applies the constraint.

        :param data: the player data frame.
        :return: An LpAffineExpression to be added to the LpProblem.
        """
        weeks = data[self.week_col].unique()
        return [lpSum(data[data.apply(lambda x: self.slate.filter_function(x, self.datetime_col, self.week_col, weeks),
                                      axis=1)]['LpVariable']) == self.num_players]

    def is_valid(self, constraints: List['LineupConstraint']) -> Tuple[bool, Optional[str]]:
        """
        Returns false if any of the below conditions are satisfied:
        1. The lineup optimizer already includes a GameSlateConstraint.

        :param constraints: the list of existing lineup constraints
        :return: a bool indicating whether or not the constraint is valid and a message, if appropriate
        """
        for constraint in constraints:
            if type(constraint) is GameSlateConstraint:
                return False, 'Optimizer already includes a game slate-related constraint'
        return True, None

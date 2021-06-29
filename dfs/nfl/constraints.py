from typing import List, Tuple, Optional

import pandas as pd
from pulp import lpSum, LpAffineExpression

from dfs import constraints as c
from dfs.nfl.positions import QB, RB, WR, TE, DST


class QbReceiverStackConstraint(c.LineupConstraint):
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

    def is_valid(self, constraints: List[c.LineupConstraint]) -> Tuple[bool, Optional[str]]:
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
            elif type(constraint) is c.MaxPlayersFromTeamConstraint:
                if constraint.team == self.team and constraint.maximum < 2:
                    return False, f"Max players from {self.team} is already set to {constraint.maximum}"
        return True, None


class RbDstStackConstraint(c.LineupConstraint):
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

    def is_valid(self, constraints: List[c.LineupConstraint]) -> Tuple[bool, Optional[str]]:
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
            elif type(constraint) is c.MaxPlayersFromTeamConstraint:
                if constraint.team == self.team and constraint.maximum < 2:
                    return False, f"Max players from {self.team} is already set to {constraint.maximum}"
        return True, None

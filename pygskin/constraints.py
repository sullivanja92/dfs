from abc import ABC, abstractmethod
from typing import Dict

from pulp import LpAffineExpression, LpVariable, lpSum

from pygskin.positions import Position


class LineupConstraint(ABC):
    """
    Abstract base class representing a fantasy lineup constraint.
    """

    @abstractmethod
    def apply(self) -> LpAffineExpression:
        """
        Applies the given constraint with args provided in constructor.

        :return: An LpAffineExpression to add to the pulp problem.
        """
        pass


class LineupSizeConstraint(LineupConstraint):  # TODO: is position dict needed?
    """
    A constraint based on the number of players allowed in a lineup.
    """

    def __init__(self, size: int, position_to_index_dict: Dict[Position, Dict[int, LpVariable]]):
        """
        :param size: The size of the lineup
        :param position_to_index_dict: The dict containing positions mapped to index/variable dicts
        """
        self.size = size
        self.position_to_index_dict = position_to_index_dict

    def apply(self) -> LpAffineExpression:
        """
        Takes the sum of players included in a lineup and returns whether that is equal to the required lineup size.

        :return: The LpAffineExpression to be added to the pulp problem
        """
        total_players = []
        for k, v in self.position_to_index_dict.items():
            total_players += lpSum([self.position_to_index_dict[k][i] for i in v])
        return lpSum(total_players) == self.size

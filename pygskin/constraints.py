from abc import ABC, abstractmethod
from typing import Dict, Iterable

from pulp import LpAffineExpression, LpVariable, lpSum


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


class LineupSizeConstraint(LineupConstraint):
    """
    A constraint based on the number of players allowed in a lineup.
    """

    def __init__(self, size: int, lp_variables: Iterable[LpVariable]):
        """
        :param size: The size of the lineup
        :param lp_variables: The lp variables
        """
        self.size = size
        self.lp_variables = lp_variables

    def apply(self) -> LpAffineExpression:
        """
        Takes the sum of players included in a lineup and returns whether that is equal to the required lineup size.

        :return: The LpAffineExpression representing valid lineup size to be added to the pulp problem.
        """
        return lpSum(self.lp_variables) == self.size


class SalaryCapConstraint(LineupConstraint):
    """
    A salary cap-based constraint.
    """

    def __init__(self, salary_cap: int,
                 index_to_variable_dict: Dict[int, LpVariable],
                 index_to_salary_dict: Dict[int, int]):
        """
        :param salary_cap: The salary cap.
        :param index_to_variable_dict: A dict containing index to lp variable mappings.
        :param index_to_salary_dict:  A dict containing index to salary mappings.
        """
        self.salary_cap = salary_cap
        self.index_to_variable_dict = index_to_variable_dict
        self.index_to_salary_dict = index_to_salary_dict

    def apply(self) -> LpAffineExpression:
        """
        Takes the sum of included player salaries and compares that to the salary cap.

        :return: The LpAffineExpression representing valid lineup salary to be added to the pulp problem.
        """
        costs = [self.index_to_salary_dict[i] * self.index_to_variable_dict[i]
                 for i in self.index_to_variable_dict.keys()]
        return lpSum(costs) <= self.salary_cap

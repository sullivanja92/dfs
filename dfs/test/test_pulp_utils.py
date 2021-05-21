import unittest
from unittest.mock import Mock

from pulp import constants

from dfs import pulp_utils


class TestPulpUtils(unittest.TestCase):

    def test_is_optimal_solution_found(self):
        problem = Mock(status=constants.LpStatusOptimal)
        self.assertTrue(pulp_utils.is_optimal_solution_found(problem=problem))

    def test_is_optimal_solution_found_none(self):
        self.assertRaises(ValueError, lambda: pulp_utils.is_optimal_solution_found(None))

    def test_is_optimal_solution_found_not_solved(self):
        problem = Mock(status=constants.LpStatusNotSolved)
        self.assertFalse(pulp_utils.is_optimal_solution_found(problem=problem))

    def test_is_optimal_solution_found_infeasible(self):
        problem = Mock(status=constants.LpStatusInfeasible)
        self.assertFalse(pulp_utils.is_optimal_solution_found(problem=problem))

    def test_is_optimal_solution_found_unbounded(self):
        problem = Mock(status=constants.LpStatusUnbounded)
        self.assertFalse(pulp_utils.is_optimal_solution_found(problem=problem))

    def test_is_optimal_solution_found_undefined(self):
        problem = Mock(status=constants.LpStatusUndefined)
        self.assertFalse(pulp_utils.is_optimal_solution_found(problem=problem))

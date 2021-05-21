from pulp import LpProblem, LpStatus


def is_optimal_solution_found(problem: LpProblem) -> bool:
    """
    Returns a bool indicating whether an optimal solution has been found for the given problem.

    :param problem: the LpProblem variable
    :return: True if an optimal solution is found, else False
    """
    if problem is None:
        raise ValueError('Problem cannot be none')
    return LpStatus[problem.status] == 'Optimal'

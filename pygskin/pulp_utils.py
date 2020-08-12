from pulp import LpProblem, LpStatus


def int_index_from_lp_variable_name(name: str, delimiter: str = '_') -> int:
    if name is None or name == '':
        raise ValueError('Name must not be None or empty')
    if delimiter is None or delimiter not in name:
        raise ValueError('The delimiter must be found in the variable name')
    return int(name.split(delimiter)[1])


def is_optimal_solution_found(problem: LpProblem) -> bool:
    if problem is None:
        raise ValueError('Problem cannot be none')
    return LpStatus[problem.status] == 'Optimal'

# encoding=utf8
"""
SimpleSolver
"""
from kaiwu_community.core import get_sol_dict
from kaiwu_community.conversion import qubo_model_to_ising_model
from kaiwu_community.core import SolverBase
from kaiwu_community.common import hamiltonian


def _to_ising_matrix(qubo_model):
    ising_model = qubo_model_to_ising_model(qubo_model)
    ising_mat = ising_model.get_matrix()
    bias = ising_model.get_bias()
    vars_dict = ising_model.get_variables()
    return ising_mat, bias, vars_dict


class SimpleSolver(SolverBase):
    """实现用Optimizer直接对QuboModel进行求解

    Examples:
        >>> import kaiwu_community as kw
        >>> n = 10
        >>> W = 5
        >>> p = [i + 1 for i in range(n)]
        >>> w = [(i + 2) / 2 for i in range(n)]
        >>> x = kw.core.ndarray(n, 'x', kw.core.Binary)
        >>> qubo_model = kw.qubo.QuboModel()
        >>> qubo_model.set_objective(sum(x[i] * p[i] * (-1) for i in range(n)))
        >>> qubo_model.add_constraint(sum(x[i] * w[i] for i in range(n)) <= W, "c", penalty=10)
        >>> solver = kw.solver.SimpleSolver(kw.classical.BruteForceOptimizer())
        >>> sol_dict, qubo_val = solver.solve_qubo(qubo_model)
        >>> unsatisfied_count, result_dict = qubo_model.verify_constraint(sol_dict)
        >>> unsatisfied_count
        0

    Returns:
        tuple: Result dictionary and Result dictionary.

        - dict: Result dictionary. The key is the variable name, and the value is the corresponding spin value.

        - float: qubo value.
    """

    def solve_qubo(self, qubo_model):
        ising_mat, bias, vars_dict = _to_ising_matrix(qubo_model)
        solutions = self._optimizer.solve(ising_mat)
        if solutions is None:
            return None, None
        solution_dicts = get_sol_dict(solutions[0][:-1] * solutions[0][-1], vars_dict)
        return solution_dicts, hamiltonian(ising_mat, solutions)[0] + bias


if __name__ == '__main__':
    import doctest

    doctest.testmod()

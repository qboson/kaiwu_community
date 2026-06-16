"""Tests for solver base classes and their common orchestration logic."""

import numpy as np
import pytest

import kaiwu as kw
from kaiwu.core import _base_solver
from kaiwu.core import Binary, IsingSolver, QuboSolver


class RecordingIsingSolver(IsingSolver):
    """Small deterministic solver used to exercise IsingSolver.solve."""

    def __init__(self, solutions):
        super().__init__()
        self.solutions = np.asarray(solutions)
        self.matrix_change_count = 0
        self.solved_matrix = None

    def on_matrix_change(self):
        self.matrix_change_count += 1

    def _solve(self, ising_matrix=None):
        self.solved_matrix = ising_matrix
        return self.solutions


class RecordingQuboSolver(RecordingIsingSolver, QuboSolver):
    """Combines the fake Ising backend with QuboSolver's conversion path."""

    pass


def test_ising_solver_sorts_solutions_and_stores_hamiltonian():
    matrix = np.array([[0.0, 1.0], [1.0, 0.0]])
    solver = RecordingIsingSolver([[1, -1], [1, 1]])

    solutions = solver.solve(matrix, negtail_flip=True, sort_solutions=True)

    # The lower-energy solution is moved first, then negtail_flip normalizes it.
    np.testing.assert_array_equal(solutions, np.array([[1, 1], [-1, 1]]))
    np.testing.assert_array_equal(solver.get_hamiltonian(), np.array([-2.0, 2.0]))
    np.testing.assert_array_equal(solver.solved_matrix, matrix)
    assert solver.matrix_change_count == 1


def test_ising_solver_requires_matrix_before_solving():
    solver = RecordingIsingSolver([[1]])

    with pytest.raises(ValueError, match="Ising matrix must be set"):
        solver.solve()


def test_qubo_solver_returns_best_solution_and_energy():
    x = Binary("x")
    qubo_model = kw.core.QuboModel(x)
    solver = RecordingQuboSolver([[-1, 1], [1, 1]])

    solution, hamiltonian = solver.solve_qubo(qubo_model)

    # QUBO x is minimized by x=0, and the converted Ising bias shifts energy to 0.
    assert solution == {"x": 0.0}
    assert hamiltonian == 0.0
    assert solver.matrix_change_count == 1


def test_qubo_solver_logs_warning_when_no_solution(monkeypatch):
    class EmptyQuboSolver(QuboSolver):
        def solve_qubo(self, qubo_model, sort_solutions=False):
            return None, None

    warnings = []
    # Patch the module logger directly because the project logger has custom handlers.
    monkeypatch.setattr(_base_solver.logger, "warning", warnings.append)

    assert EmptyQuboSolver().solve_qubo(None) == (None, None)

    assert warnings == ["No solution found!"]

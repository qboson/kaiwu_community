import logging
import os
import sys
from unittest.mock import patch

from common.config import BASE_DIR
from kaiwu.core import qubo_model_to_ising_model

sys.path.insert(0, os.path.join(BASE_DIR, "src"))
import numpy as np
import kaiwu as kw
from kaiwu.core import Binary, Integer, PenaltyMethodConstraint


class TestQuboModel:
    def test_add_constraint(self):
        x, y = Binary("x"), Binary("y")
        qexp = x + y * x * 2
        constr = (x * y - 1) ** 2
        qubo_model = kw.core.QuboModel(qexp)
        qubo_model.add_constraint(constr, "hard")
        qubo_model.make()
        assert qubo_model.made, "Failed to add hard constraint!"

    def test_add_constraint_soft(self):
        x, y = Binary("x"), Binary("y")
        qexp = x + y * x * 2
        constr = (x * y - 1) ** 2
        qubo_model = kw.core.QuboModel(qexp)
        qubo_model.add_constraint(constr, "soft", constr_type="soft")
        qubo_model.make()
        assert qubo_model.made, "Failed to add soft constraint!"

    @patch("kaiwu.classical._simulated_annealing.verify_license", return_value=None)
    def test_get_matrix(self, mock_verify_license):
        x = kw.core.ndarray((3,), "x", Integer, (-4, 4)) / 2
        A = np.array([[1, 1, 1], [-1, 0, 0], [0, -1, 0]])
        b = np.array([1, 0, 0])
        qubo_model = kw.core.QuboModel()
        qubo_model.set_objective(-x[2])
        print(kw.core.dot(A, x) <= b)
        qubo_model.add_constraint(kw.core.dot(A, x) <= b, "c")
        # Qubo Model
        qubo_model.set_constraint_handler(PenaltyMethodConstraint)
        qubo_mat = qubo_model.get_matrix()
        # Ising Model
        ising_model = qubo_model_to_ising_model(qubo_model)
        ising_mat = ising_model.get_matrix()
        qubo_mat_from_ising, bias = kw.core.ising_matrix_to_qubo_matrix(ising_mat)
        print(qubo_mat)
        assert (qubo_mat_from_ising == qubo_mat).all()

        optimizer = kw.classical.SimulatedAnnealingOptimizer(
            initial_temperature=100, iterations_per_t=99, rand_seed=239287092
        )
        solver = kw.solver.SimpleSolver(optimizer)
        sol_dicts = solver.solve_qubo(qubo_model)

        # Qubo Model
        qubo_model.verify_constraint(sol_dicts[0])

        # ising model
        ising_solutions = optimizer.solve(ising_mat)
        var_dic = ising_model.get_variables()
        sol_dict_from_ising = kw.core.get_sol_dict(ising_solutions[0], var_dic)

        qubo_value = qubo_model.get_value(sol_dicts[0])
        qubo_value_from_ising = qubo_model.get_value(sol_dict_from_ising)

        assert qubo_value == qubo_value_from_ising

    def test_make(self):
        b1, b2 = Binary("b1"), Binary("b2")
        q = b1 + b2 + b1 * b2
        q_model = kw.core.QuboModel(q)
        q_model.make()

        assert (
            q_model.get_matrix() == [[1.0, 1.0], [0.0, 1.0]]
        ).all(), "matrix does not match!"
        assert q_model.get_offset() == 0, "offset does not match!"
        assert q_model.get_variables() == {"b1": 0, "b2": 1}, "variables do not match"

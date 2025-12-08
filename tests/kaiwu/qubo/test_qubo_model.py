import os
import sys

from common.config import BASE_DIR

sys.path.insert(0, os.path.join(BASE_DIR, 'src'))
import kaiwu as kw
from kaiwu.core import Binary


class TestQuboModel:
    def test_add_constraint(self):
        x, y = Binary("x"), Binary("y")
        qexp = x + y * x * 2
        constr = (x * y - 1) ** 2
        qubo_model = kw.qubo.QuboModel(qexp)
        qubo_model.add_constraint(constr==0, "hard")
        qubo_model.make()
        assert qubo_model.made, "Failed to add hard constraint!"

    def test_add_constraint_soft(self):
        x, y = Binary("x"), Binary("y")
        qexp = x + y * x * 2
        constr = (x * y - 1) ** 2
        qubo_model = kw.qubo.QuboModel(qexp)
        qubo_model.add_constraint(constr==0, "soft", constr_type="soft")
        qubo_model.make()
        assert qubo_model.made, "Failed to add soft constraint!"

    def test_make(self):
        b1, b2 = Binary("b1"), Binary("b2")
        q = b1 + b2 + b1 * b2
        q_model = kw.qubo.QuboModel(q)
        q_model.make()

        assert (q_model.get_matrix() == [[1., 1.], [0., 1.]]).all(), "matrix does not match!"
        assert q_model.get_offset() == 0, "offset does not match!"
        assert q_model.get_variables() == {'bb1': 0, 'bb2': 1}, "variables do not match"



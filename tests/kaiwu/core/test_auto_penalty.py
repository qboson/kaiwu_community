import os
import sys
import unittest

from common.config import BASE_DIR

sys.path.insert(0, os.path.join(BASE_DIR, 'src/'))

from kaiwu.core import Binary, quicksum
from kaiwu.core import get_min_penalty_for_equal_constraint, get_min_penalty


class TestQuboPenalty(unittest.TestCase):

    def test_get_obj_variables(self):
        x0, x1, x2 = Binary('x0'), Binary('x1'), Binary('x2')
        obj = 3 * x0 * x1 + 2 * x2
        variables = obj.get_variables()
        self.assertEqual(variables, ('bx0', 'bx1', 'bx2'))

    def test_get_obj_max_deltas(self):
        x0, x1, x2 = Binary('x0'), Binary('x1'), Binary('x2')
        obj = 3 * x0 + 2 * x1 * x2
        neg_delta, pos_delta = obj.get_max_deltas()
        self.assertEqual(pos_delta['bx0'], 3)
        self.assertEqual(neg_delta['bx0'], -3)
        self.assertEqual(pos_delta['bx1'], 2)
        self.assertEqual(neg_delta['bx1'], 0)
        self.assertEqual(pos_delta['bx2'], 2)
        self.assertEqual(neg_delta['bx2'], 0)

    def test_get_min_penalty_for_equal_constraint_example(self):
        x = [Binary(f"b{i}") for i in range(3)]
        cons = quicksum(x) - 1
        obj = x[1] + x[2]
        penalty = get_min_penalty_for_equal_constraint(obj, cons)
        self.assertEqual(penalty, 1.0)

    def test_get_min_penalty_for_equal_constraint_negative_coefficient(self):
        x = [Binary(f"b{i}") for i in range(3)]
        cons = quicksum(x) - 1
        obj = -x[1] + 2 * x[2]
        penalty = get_min_penalty_for_equal_constraint(obj, cons)
        self.assertEqual(penalty, 2.0)

    def test_get_min_penalty(self):
        x = [Binary(f"b{i}") for i in range(3)]
        cons = quicksum(x) - 1
        obj = x[1] + x[2]
        penalty = get_min_penalty(obj, cons)
        self.assertGreaterEqual(penalty, 1.0)


if __name__ == '__main__':
    unittest.main()

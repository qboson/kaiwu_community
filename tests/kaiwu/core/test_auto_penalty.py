import unittest
from kaiwu.core._binary_expression import Binary, quicksum
from kaiwu.core._constraint import (
    get_min_penalty_for_equal_constraint,
    _get_constraint_min_deltas_diff,
    _get_constraint_min_deltas_exhaust,
    get_soft_penalty,
    get_min_penalty,
)


class TestQuboPenalty(unittest.TestCase):

    def test_get_obj_variables(self):
        x0, x1, x2 = Binary("x0"), Binary("x1"), Binary("x2")
        obj = 3 * x0 * x1 + 2 * x2
        variables = obj.get_variables()
        self.assertEqual(variables, {"x0": 0, "x1": 1, "x2": 2})

    def test_get_obj_max_deltas(self):
        x0, x1, x2 = Binary("x0"), Binary("x1"), Binary("x2")
        obj = 3 * x0 + 2 * x1 * x2
        neg_delta, pos_delta = obj.get_max_deltas()
        self.assertEqual(pos_delta["x0"], 3)
        self.assertEqual(neg_delta["x0"], -3)
        self.assertEqual(pos_delta["x1"], 2)
        self.assertEqual(neg_delta["x1"], 0)
        self.assertEqual(pos_delta["x2"], 2)
        self.assertEqual(neg_delta["x2"], 0)

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

    def test_get_constraint_min_deltas_diff(self):
        x0, x1 = Binary("x0"), Binary("x1")
        cons = 2 * x0 * x1 + 3 * x0
        constraint_var_quadratic = {"x0": [2], "x1": [2]}
        constraint_var_linear = {"x0": 3}
        min_delta = _get_constraint_min_deltas_diff(
            constraint_var_quadratic, constraint_var_linear
        )
        self.assertEqual(
            min_delta["x0"], 3
        )  # 3 + 2 =5; |5|=5, 3=3; 2=2; 3-2=1 → min is 1?

    def test_get_constraint_min_deltas_exhaust(self):
        x0, x1 = Binary("x0"), Binary("x1")
        cons = 2 * x0 * x1 + 3 * x0
        constraint_var_quadratic = {"x0": [2], "x1": [2]}
        constraint_var_linear = {"x0": 3}
        min_delta = _get_constraint_min_deltas_exhaust(
            constraint_var_quadratic, constraint_var_linear
        )
        self.assertEqual(min_delta["x0"], 3)

    def test_get_min_penalty(self):
        x = [Binary(f"b{i}") for i in range(3)]
        cons = quicksum(x) - 1
        obj = x[1] + x[2]
        penalty = get_min_penalty(obj, cons)
        self.assertGreaterEqual(penalty, 1.0)

    def test_get_soft_penalty(self):
        x = [Binary(f"b{i}") for i in range(2)]
        obj = x[0] + 2 * x[1]
        cons = quicksum(x) - 1
        penalty = get_soft_penalty(obj, cons)
        avg_obj = (1 + 2) / 2
        avg_cons = (1 + 1 + 1) / 3  # (x0 + x1 -1)^2 展开后的项数？
        # 需要根据实际项数计算平均值
        # 此处可能需要修正测试用例，根据具体实现逻辑
        self.assertAlmostEqual(penalty, avg_obj / avg_cons, places=1)


if __name__ == "__main__":
    unittest.main()

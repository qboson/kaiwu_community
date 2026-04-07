import os
import sys

from common.config import BASE_DIR
from kaiwu.core import KaiwuError, Binary, Placeholder
from kaiwu.hobo import HoboModel

sys.path.insert(0, os.path.join(BASE_DIR, "src"))
import kaiwu as kw


class TestQuboExpression:
    def test_mul(self):
        a, b, c = Binary("a"), Binary("b"), Binary("c")
        y = (a + 2 * b) * (a * 3 + c) * 0.5 / 2
        coefficient = {
            ("b", "c"): 0.5,
            ("a", "b"): 1.5,
            ("a", "c"): 0.25,
            ("a",): 0.75,
        }
        offset = 0.0
        assert y.coefficient == coefficient, "coefficient error!"
        assert y.offset == offset, "offset error!"

    def test_add(self):
        a, b, c = Binary("a"), Binary("b"), Binary("c")
        y = a + 2 * b + b - 3 * b + 2 * c - 3 * c
        coefficient = {("c",): -1, ("a",): 1}
        offset = 0

        assert y.coefficient == coefficient, "coefficient error!"
        assert y.offset == offset, "offset error!"

    def test_rsub(self):
        a, b = Binary("a"), Binary("b")
        y = 1 - a + b
        coefficient = {("b",): 1, ("a",): -1}
        offset = 1

        assert y.coefficient == coefficient, "coefficient error!"
        assert y.offset == offset, "offset error!"

    def test_pow(self):
        a, b, c = Binary("a"), Binary("b"), Binary("c")
        y = (a + b + c) ** 2

        coefficient = {
            ("b",): 1,
            ("a", "b"): 2,
            ("b", "c"): 2,
            ("a",): 1,
            ("a", "c"): 2,
            ("c",): 1,
        }
        offset = 0

        assert y.coefficient == coefficient, "test_pow coefficient error!"
        assert y.offset == offset, "test_pow offset error!"

        y = a**1 + b**2
        coefficient = {("b",): 1, ("a",): 1}
        offset = 0

        assert y.coefficient == coefficient, "test_pow coefficient error!"
        assert y.offset == offset, "test_pow offset error!"

    def test_eq(self):
        a, b = Binary("a"), Binary("b")
        t = a - a
        assert t == 0

    def test_placeholder(self):
        a, b, c = Binary("a"), Binary("b"), Binary("c")
        p1, p2 = Placeholder("p1"), Placeholder("p2")
        z = a * p1 * c + 2 * b + p1 * p2 + (1 + p2 + 1) * 2 * a

        assert z.coefficient[("b",)] == 2, "ans_z_coefficient coefficient ('b',) error!"

        assert (
            z.coefficient[("a", "c")].coefficient[("p1",)] == 1
        ), "ans_z_coefficient coefficient ('a', 'c') error!"
        assert (
            z.coefficient[("a", "c")].offset == 0
        ), "ans_z_coefficient offset ('a', 'c') error!"

        assert (
            z.coefficient[("a",)].coefficient[("p2",)] == 2
        ), "ans_z_coefficient coefficient ('a', 'c') error!"
        assert (
            z.coefficient[("a",)].offset == 4
        ), "ans_z_coefficient offset ('a',) error!"

        assert (
            z.offset.coefficient[("p1", "p2")] == 1
        ), "ans_z_coefficient offset error!"
        assert z.offset.offset == 0, "ans_z_coefficient offset error!"

        zf = z.feed({"p1": 1, "p2": 3})
        ans_zf_coefficient = {("b",): 2, ("a", "c"): 1, ("a",): 10}
        ans_zf_offset = 3

        assert zf.coefficient == ans_zf_coefficient, "ans_zf_coefficient error!"
        assert zf.offset == ans_zf_offset, "ans_zf_offset error!"

    def test_placeholder_str_with_hobo(self):
        a, b, c = Binary("a"), Binary("b"), Binary("c")
        p1, p2 = Placeholder("p1"), Placeholder("p2")
        z = a * b * p1 * c + 2 + p1 * p2 + (1 + p2 + 1) * 2 * a

        hobo_Model = HoboModel(z)
        qubo_model = hobo_Model.reduce()
        print(qubo_model.objective)
        assert (
            str(qubo_model.objective) == "(2*p2+4)*a+(p1)*_a_b*c+p1*p2+2"
        ), "placeholder show error"

        zf = z.feed({"p1": 1, "p2": 3})
        hobo_Model = HoboModel(zf)
        qubo_model = hobo_Model.reduce()
        assert (
            str(qubo_model.objective) == "10*a+_a_b*c+5"
        ), "Placeholder after feed error"

    def test_spin(self):
        s = kw.core.Spin("a")
        s = s * s
        print(s)

    def test_integer(self):
        try:
            var_i = kw.core.Integer("x", 1, 1)
        except KaiwuError:
            pass
        var_i = kw.core.Integer("x", 1, 8)
        print(var_i)
        assert var_i.coefficient[("x[2]",)] == 4 and ("x[3]",) not in var_i.coefficient
        var_i = kw.core.Integer("x", 0, 8)
        print(var_i)
        assert var_i.coefficient[("x[3]",)] == 1
        var_i = kw.core.Integer("x", 0, 10)
        print(var_i)
        assert var_i.coefficient[("x[3]",)] == 3

    def test_ndarray(self):
        bin_func = Binary
        bin_array = kw.core.ndarray((2, 2), "x", bin_func)
        print(bin_array)

        int_func = kw.core.Integer
        int_array = kw.core.ndarray((2, 2), "x", int_func)
        print(int_array)

        int_array = kw.core.ndarray(
            (2, 2), "x", lambda name: kw.core.Integer(name, 0, 4)
        )
        print(int_array)

        y = Binary("y")
        print(bin_array + y)
        print(y + bin_array)
        print(y - bin_array)
        print(bin_array - y)

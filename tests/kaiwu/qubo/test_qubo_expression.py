import os
import sys
from common.config import BASE_DIR
sys.path.insert(0, os.path.join(BASE_DIR, 'src/com/qboson'))
import kaiwu as kw
from kaiwu.core import KaiwuError, Binary, Placeholder


class TestQuboExpression:
    def test_mul(self):
        a, b, c = Binary('a'), Binary('b'), Binary('c')
        y = (a + 2 * b) * (a * 3 + c) * 0.5 / 2
        coefficient = {('bb', 'bc'): 0.5, ('ba', 'bb'): 1.5,
                                 ('ba', 'bc'): 0.25, ('ba', ): 0.75}
        offset = 0.0
        assert y.name == ''
        assert y.coefficient == coefficient, "coefficient error!"
        assert y.offset == offset, "offset error!"

    def test_add(self):
        a, b, c = Binary('a'), Binary('b'), Binary('c')
        y = a + 2 * b + b - 3 * b + 2 * c - 3 * c
        coefficient = {('bc',): -1, ('ba',): 1}
        offset = 0

        assert y.name == ''
        assert y.coefficient == coefficient, "coefficient error!"
        assert y.offset == offset, "offset error!"

    def test_rsub(self):
        a, b = Binary('a'), Binary('b')
        y = 1 - a + b
        coefficient = {('bb',): 1, ('ba',): -1}
        offset = 1

        assert y.coefficient == coefficient, "coefficient error!"
        assert y.offset == offset, "offset error!"

    def test_pow(self):
        a, b, c = Binary('a'), Binary('b'), Binary('c')
        y = (a + b + c) ** 2

        coefficient = {('bb', ): 1, ('ba', 'bb'): 2, ('bb', 'bc'): 2,
                                 ('ba', ): 1, ('ba', 'bc'): 2, ('bc', ): 1}
        offset = 0

        assert y.coefficient == coefficient, "test_pow coefficient error!"
        assert y.offset == offset, "test_pow offset error!"

        y = a ** 1 + b ** 2
        coefficient = {('bb',): 1, ('ba',): 1}
        offset = 0

        assert y.coefficient == coefficient, "test_pow coefficient error!"
        assert y.offset == offset, "test_pow offset error!"

    def test_eq(self):
        a, b = Binary('a'), Binary('b')
        t = a - a
        assert t == 0

    def test_placeholder(self):
        a, b, c = Binary('a'), Binary('b'), Binary('c')
        p1, p2 = Placeholder('p1'), Placeholder('p2')
        z = a * p1 * c + 2 * b + p1 * p2 + (1 + p2 + 1) * 2 * a

        assert z.coefficient[('bb',)] == 2, "ans_z_coefficient coefficient ('bb',) error!"

        assert z.coefficient[('ba', 'bc')].coefficient[('pp1',)] == 1, \
            "ans_z_coefficient coefficient ('ba', 'bc') error!"
        assert z.coefficient[('ba', 'bc')].offset == 0, \
            "ans_z_coefficient offset ('ba', 'bc') error!"

        assert z.coefficient[('ba',)].coefficient[('pp2',)] == 2, \
            "ans_z_coefficient coefficient ('ba', 'bc') error!"
        assert z.coefficient[('ba',)].offset == 4, \
            "ans_z_coefficient offset ('ba',) error!"

        assert z.offset.coefficient[('pp1', 'pp2')] == 1, "ans_z_coefficient offset error!"
        assert z.offset.offset == 0, "ans_z_coefficient offset error!"

        zf = z.feed({"p1": 1, "p2": 3})
        ans_zf_coefficient = {('bb',): 2, ('ba', 'bc'): 1, ('ba',): 10}
        ans_zf_offset = 3

        assert zf.coefficient == ans_zf_coefficient, "ans_zf_coefficient error!"
        assert zf.offset == ans_zf_offset, "ans_zf_offset error!"

    def test_spin(self):
        s = kw.ising.Spin('a')
        s = s * s
        assert str(s) == "0*a+1"

    def test_integer(self):
        try:
            var_i = kw.core.Integer("x", 1, 1)
        except KaiwuError:
            pass
        var_i = kw.core.Integer("x", 1, 8)
        print(var_i)
        assert var_i.coefficient[("bx[2]",)] == 4 and ("bx[3]",) not in var_i.coefficient
        var_i = kw.core.Integer("x", 0, 8)
        print(var_i)
        assert var_i.coefficient[("bx[3]",)] == 1
        var_i = kw.core.Integer("x", 0, 10)
        print(var_i)
        assert var_i.coefficient[("bx[3]",)] == 3

    def test_ndarray(self):
        bin_func = Binary
        bin_array = kw.core.ndarray((2, 2), "x", bin_func)
        assert str(bin_array) == '[[x[0][0] x[0][1]]\n [x[1][0] x[1][1]]]'

        int_func = kw.core.Integer
        int_array = kw.core.ndarray((2, 2), "x", int_func)
        assert str(int_array) == ('[[x[0][0][0]+2*x[0][0][1]+4*x[0][0][2]+8*x[0][0][3]+16*x[0][0][4]+32*x[0][0][5]+64*x[0][0][6]\n'
 '  '
 'x[0][1][0]+2*x[0][1][1]+4*x[0][1][2]+8*x[0][1][3]+16*x[0][1][4]+32*x[0][1][5]+64*x[0][1][6]]\n'
 ' '
 '[x[1][0][0]+2*x[1][0][1]+4*x[1][0][2]+8*x[1][0][3]+16*x[1][0][4]+32*x[1][0][5]+64*x[1][0][6]\n'
 '  '
 'x[1][1][0]+2*x[1][1][1]+4*x[1][1][2]+8*x[1][1][3]+16*x[1][1][4]+32*x[1][1][5]+64*x[1][1][6]]]')


        int_array = kw.core.ndarray((2, 2), "x", lambda name: kw.core.Integer(name, 0, 4))
        assert str(int_array) == ('[[x[0][0][0]+2*x[0][0][1]+x[0][0][2] x[0][1][0]+2*x[0][1][1]+x[0][1][2]]\n'
 ' [x[1][0][0]+2*x[1][0][1]+x[1][0][2] x[1][1][0]+2*x[1][1][1]+x[1][1][2]]]')

        y = Binary("y")
        assert str(bin_array + y) == '[[y+x[0][0] y+x[0][1]]\n [y+x[1][0] y+x[1][1]]]'
        assert str(y + bin_array) == '[[y+x[0][0] y+x[0][1]]\n [y+x[1][0] y+x[1][1]]]'
        assert str(y - bin_array) == '[[y-x[0][0] y-x[0][1]]\n [y-x[1][0] y-x[1][1]]]'
        assert str(bin_array - y) == '[[-y+x[0][0] -y+x[0][1]]\n [-y+x[1][0] -y+x[1][1]]]'

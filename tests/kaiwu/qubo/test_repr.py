import os
import sys
from common.config import BASE_DIR
from kaiwu.core import Binary, Placeholder

sys.path.insert(0, os.path.join(BASE_DIR, 'src/com/qboson'))


def test_qubo_details():
    a, b, c = Binary('a'), Binary('b'), Binary('c')
    z = a * b * 3 + 2 + c * b + (1 + c + 1) * 2 * a
    qubo_str = str(z)
    ans_str = '2*a*c+4*a+b*c+3*a*b+2'
    assert qubo_str == ans_str


import os
import sys
from common.config import BASE_DIR
sys.path.insert(0, os.path.join(BASE_DIR, 'src'))
import kaiwu_community as kw
from kaiwu_community.qubo import QuboError, QuboModel
from kaiwu_community.core import Binary, quicksum


def test_details():
    a, b, c = Binary('a'), Binary('b'), Binary('c')
    z = a * b * 3 + 2 + c * b + (1 + c + 1) * 2 * a
    qubo_model = QuboModel(z)
    ising_model = kw.conversion.qubo_model_to_ising_model(qubo_model)

    assert str(z) == "2*a*c+4*a+b*c+3*a*b+2"
    assert(str(ising_model) == ('CIM Ising Details:\n'
 '  CIM Ising Matrix:\n'
 '    [[-0.    -0.375 -0.25  -1.625]\n'
 '     [-0.375 -0.    -0.125 -0.5  ]\n'
 '     [-0.25  -0.125 -0.    -0.375]\n'
 '     [-1.625 -0.5   -0.375 -0.   ]]\n'
 '  CIM Ising Bias: 5.5\n'
 '  CIM Ising Variables: a, b, c, __spin__\n'))



def test_quicksum():
    q_list = [Binary(f'z{i}') for i in range(5)]
    q_list.append(-Binary('z2'))
    q_list.append(2)
    qsum = quicksum(q_list)
    qsum2 = sum(q_list)
    assert qsum == qsum2

    try:
        x = quicksum(Binary('x'))
    except QuboError:
        pass


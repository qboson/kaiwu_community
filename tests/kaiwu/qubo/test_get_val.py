import os
import sys
from common.config import BASE_DIR

sys.path.insert(0, os.path.join(BASE_DIR, 'src'))
import numpy as np
import kaiwu as kw
from kaiwu.core import Binary, get_val, get_array_val, get_sol_dict
from kaiwu.qubo import QuboModel


def test_get_sol_dict():
    a, b, c = Binary('a'), Binary('b'), Binary('c')
    z = a * b * 3 + 2 + c * b + (1 + c + 1) * 2 * a
    qubo_model = QuboModel(z)
    ising_model = kw.conversion.qubo_model_to_ising_model(qubo_model)
    sol = np.array([1, -1, 1, 1])
    vars = ising_model.get_variables()
    sol_dict = kw.core.get_sol_dict(sol, vars)
    assert sol_dict == {'a': 1, 'b': 0, 'c': 1}


def test_get_val():
    a, b, c = Binary('a'), Binary('b'), Binary('c')
    z1 = a * b * 3 + 2
    z2 = c * b + (1 + c + 1) * 2 * a
    z = z1 + z2
    sol_dict = {'a': 1, 'b': 0, 'c': 1}
    val = get_val(z1, sol_dict)
    assert val == 2

    sol_dict = {'a': 1, 'b': 0, 'c': 0}
    val = get_val(z, sol_dict)
    assert val == 6


def test_get_array_val():
    import kaiwu as kw
    import numpy as np
    x = kw.core.ndarray((2, 2), "x", Binary)
    y = np.sum(x)
    qubo_model = QuboModel(y)
    y_ising = kw.conversion.qubo_model_to_ising_model(qubo_model)
    vars = y_ising.get_variables()
    s = np.array([1, -1, 1, -1])
    sol_dict = get_sol_dict(s, vars)
    x_val = get_array_val(x, sol_dict)
    ans_x_val = np.array([[1.0, 0.0],
                          [1.0, 0.0]])
    assert (x_val == ans_x_val).all()

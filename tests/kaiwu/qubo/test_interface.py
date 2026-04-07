import os
import sys
from common.config import BASE_DIR

sys.path.insert(0, os.path.join(BASE_DIR, "src"))
import kaiwu as kw
from kaiwu.core import KaiwuError, QuboModel
from kaiwu.core import Binary, quicksum


def test_details():
    a, b, c = Binary("a"), Binary("b"), Binary("c")
    z = a * b * 3 + 2 + c * b + (1 + c + 1) * 2 * a
    qubo_model = QuboModel(z)
    ising_model = kw.core.qubo_model_to_ising_model(qubo_model)
    print(z)
    print(ising_model)


def test_quicksum():
    q_list = [Binary(f"z{i}") for i in range(5)]
    q_list.append(-Binary("z2"))
    q_list.append(2)
    qsum = quicksum(q_list)
    qsum2 = sum(q_list)
    assert qsum == qsum2

    try:
        x = quicksum(Binary("x"))
    except KaiwuError:
        pass

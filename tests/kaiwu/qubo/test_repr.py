import os
import sys
from common.config import BASE_DIR
from kaiwu.core import Binary, Placeholder
from kaiwu.hobo import HoboModel

sys.path.insert(0, os.path.join(BASE_DIR, "src"))


def test_qubo_details_with_hobo():
    a, b, c = Binary("a"), Binary("b"), Binary("c")
    p1, p2 = Placeholder("p1"), Placeholder("p2")
    z = a * b * p1 * c + 2 + p1 * p2 + (1 + p2 + 1) * 2 * a

    hobo_model = HoboModel(z)
    qubo_model = hobo_model.reduce()
    details_str = (
        "Minimize (2*p2+4)*a+(p1)*_a_b*c+p1*p2+2\n"
        "Subject to (hard constraints):\n"
        "a*b-2*_a_b*a-2*_a_b*b+3*_a_b"
    )
    assert str(qubo_model) == details_str, "details error"
    zf = z.feed({"p1": 1, "p2": 3})
    details_str_feed = (
        "Minimize 10*a+_a_b*c+5\n"
        "Subject to (hard constraints):\n"
        "a*b-2*_a_b*a-2*_a_b*b+3*_a_b"
    )
    hobo_model = HoboModel(zf)
    qubo_model = hobo_model.reduce()
    assert str(qubo_model) == details_str_feed, "details after feed error 1"

    zf = z.feed({"p1": 3, "p2": 1})
    hobo_model = HoboModel(zf)
    qubo_model = hobo_model.reduce()
    print(qubo_model)
    details_str_feed = (
        "Minimize 6*a+3*_a_b*c+5\n"
        "Subject to (hard constraints):\n"
        "a*b-2*_a_b*a-2*_a_b*b+3*_a_b"
    )
    assert str(qubo_model) == details_str_feed, "details after feed error 2"


def test_qubo_details():
    a, b, c = Binary("a"), Binary("b"), Binary("c")
    z = a * b * 3 + 2 + c * b + (1 + c + 1) * 2 * a
    qubo_str = str(z)
    ans_str = "2*a*c+4*a+b*c+3*a*b+2"
    assert qubo_str == ans_str

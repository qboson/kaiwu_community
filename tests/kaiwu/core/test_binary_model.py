"""
Tests for core._matrix module
"""

import os
import sys
import numpy as np

from common.config import BASE_DIR

sys.path.insert(0, os.path.join(BASE_DIR, "src"))
import kaiwu as kw
from kaiwu.core import BinaryModel


def test_add_constraint_cnt():
    A = kw.core.ndarray((2, 2), "A", kw.core.Binary)
    B = kw.core.ndarray((2, 2), "B", kw.core.Binary)
    x = kw.core.ndarray((2,), "x", kw.core.Binary)
    b = np.array([1, 2])
    c = np.array([1, -1])
    d = np.array([-1, 1])
    hobo_model = BinaryModel(c.dot(x))
    hobo_model.add_constraint(A.dot(x) == b, "constr1", penalty=2)
    hobo_model.add_constraint(B.dot(x) == d, "constr2", penalty=2)
    assert len(hobo_model.hard_constraints) == 4
    assert len(hobo_model.soft_constraints) == 0

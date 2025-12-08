import os
import sys
import pytest
import time
import numpy as np

from common.config import BASE_DIR

sys.path.insert(0, os.path.join(BASE_DIR, 'src'))
import numbers
import kaiwu.core as kc
from kaiwu.core import Binary, BinaryExpression


def is_zero(qubo_expr):
    """QUBO表达式为0"""
    if isinstance(qubo_expr, numbers.Number):
        return abs(qubo_expr) < 1e-10
    return len(qubo_expr.coefficient) == 0 and np.abs(qubo_expr.offset) < 1e-10


def test_dot():
    mat1 = np.random.randn(2, 3)
    mat2 = np.random.randn(3, 4)
    res1 = np.dot(mat1, mat2)
    res2 = kc.dot(mat1, mat2)
    print(res1.shape, res2.shape)
    print(res1 - res2)
    is_zero_func = np.vectorize(is_zero)
    print(is_zero_func(res2 - res1))
    assert is_zero_func(res2 - res1).all()

    arr_len = 500
    mat1 = np.random.randn(arr_len, arr_len)
    vec = np.random.randn(arr_len)
    time0 = time.time()

    np.dot(vec, mat1).dot(vec)
    print(time.time() - time0)
    time0 = time.time()
    kc.dot(kc.dot(vec, mat1), vec)

    print(time.time() - time0)

    arr_len = 500
    mat2 = np.random.randn(arr_len, arr_len)
    vec = kc.ndarray((arr_len,), "z", Binary)
    time0 = time.time()

    print(time.time() - time0)
    time0 = time.time()
    kc.dot(kc.dot(vec, mat2), vec)
    print(time.time() - time0)
    assert True


class TestQuboArray:
    def test_dot(self):
        mat1 = kc.ndarray((2,), "x", Binary)
        mat2 = np.ones((2, 4))
        mat3 = kc.ndarray((4,), "z", Binary)
        mat4 = np.dot(mat1, np.dot(mat2, mat3))
        assert isinstance(mat4, BinaryExpression)

        with pytest.raises(ValueError):
            mat1 = kc.ndarray((3, 2), "x", Binary)
            mat2 = kc.ndarray((1, 4), "x", Binary)
            mat1.dot(mat2)


def test_relation():
    arr_len = 2
    mat1 = kc.ndarray((arr_len, arr_len), "x", Binary)
    mat2 = kc.ndarray((arr_len, arr_len), "y", Binary)
    print(mat1 < mat2)
    import re
    clean = lambda s: re.sub(r'\s+', '', s)
    ineq = '[[-y[0][0]+x[0][0]<0,-y[0][1]+x[0][1]<0,][-y[1][0]+x[1][0]<0,-y[1][1]+x[1][1]<0,]]'
    assert clean(str(mat1 < mat2)) == clean(ineq)

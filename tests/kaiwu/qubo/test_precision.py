import os
import sys
import numpy as np
import pytest
from numpy.testing import assert_equal
from common.config import BASE_DIR

sys.path.insert(0, os.path.join(BASE_DIR, 'src/com/qboson'))
import kaiwu as kw


def test_adjust_qubo_matrix_precision():
    qubo_mat = np.array([[0.89, 0.22, 0.198],
                         [0.22, 0.23, 0.197],
                         [0.198, 0.197, 0.198]])
    _qubo_mat = np.array([[348., 168., 152.],
                          [-0., 92., 152.],
                          [-0., -0., 80.]])
    qubo_mat = kw.qubo.adjust_qubo_matrix_precision(qubo_mat)
    assert_equal(qubo_mat, _qubo_mat)


def test_check_qubo_matrix_bit_width():
    # 正常通过校验
    qubo_mat = np.array([[348., 84., 76.],
                         [84., 92., 76.],
                         [76., 76., 80.]])
    kw.qubo.check_qubo_matrix_bit_width(qubo_mat)
    # 校验失败
    error_qubo_mat = np.array([[0.89, 0.22, 0.198],
                               [0.22, 0.23, 0.197],
                               [0.198, 0.197, 0.198]])
    with pytest.raises(ValueError):
        kw.qubo.check_qubo_matrix_bit_width(error_qubo_mat)

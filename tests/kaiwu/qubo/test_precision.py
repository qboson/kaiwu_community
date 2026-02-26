import os
import sys
import numpy as np
import pytest
from numpy.testing import assert_equal
from common.config import BASE_DIR

sys.path.insert(0, os.path.join(BASE_DIR, "src"))
import kaiwu as kw


def test_adjust_qubo_matrix_precision():
    qubo_mat = np.array(
        [[0.89, 0.22, 0.198], [0.22, 0.23, 0.197], [0.198, 0.197, 0.198]]
    )
    _qubo_mat = np.array(
        [[348.0, 168.0, 152.0], [-0.0, 92.0, 152.0], [-0.0, -0.0, 80.0]]
    )
    qubo_mat = kw.qubo.adjust_qubo_matrix_precision(qubo_mat)
    assert_equal(qubo_mat, _qubo_mat)


def test_check_qubo_matrix_bit_width():
    # 正常通过校验
    qubo_mat = np.array([[348.0, 84.0, 76.0], [84.0, 92.0, 76.0], [76.0, 76.0, 80.0]])
    kw.qubo.check_qubo_matrix_bit_width(qubo_mat)
    # 校验失败
    error_qubo_mat = np.array(
        [[0.89, 0.22, 0.198], [0.22, 0.23, 0.197], [0.198, 0.197, 0.198]]
    )
    with pytest.raises(ValueError):
        kw.qubo.check_qubo_matrix_bit_width(error_qubo_mat)

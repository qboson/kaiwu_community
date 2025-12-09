# -*- coding: utf-8 -*-
"""
模块: qubo

功能: QUBO矩阵和Ising矩阵相关转化
"""
from decimal import Decimal
import numpy as np


def ising_matrix_to_qubo_matrix(ising_mat, remove_linear_bit=True):
    """Ising矩阵转QUBO矩阵

    Args:
        ising_mat (np.ndarray): Ising矩阵

        remove_linear_bit (bool): QUBO转Ising时会增加一个辅助变量表示线性项。是否移除最后一个自旋变量。默认为True。

    Returns:
        tuple: QUBO矩阵和bias

            - qubo_mat (np.ndarray): QUBO矩阵
            - bias (float): QUBO与Ising相差的常数项

    Examples:
        >>> import numpy as np
        >>> import kaiwu_community as kw
        >>> matrix = -np.array([[ 0. ,  1. ,  0. ,  1. ,  1. ],
        ...                     [ 1. ,  0. ,  0. ,  1.,   1. ],
        ...                     [ 0. ,  0. ,  0. ,  1.,   1. ],
        ...                     [ 1. ,  1.,   1. ,  0. ,  1. ],
        ...                     [ 1. ,  1.,   1. ,  1. ,  0. ]])
        >>> _qubo_mat, _ = kw.conversion.ising_matrix_to_qubo_matrix(matrix)
        >>> _qubo_mat
        array([[-4.,  8.,  0.,  8.],
               [-0., -4.,  0.,  8.],
               [-0., -0., -0.,  8.],
               [-0., -0., -0., -8.]])
    """
    # 计算前转Decimal以防精度损失
    ising_mat = np.vectorize(str)(ising_mat)
    ising_mat = np.vectorize(Decimal)(ising_mat)

    ising_mat = (ising_mat + ising_mat.T) / 2
    ising_mat_linear = None
    if remove_linear_bit:
        ising_mat_linear = ising_mat[-1, :-1] * 2
        ising_mat = ising_mat[:-1, :-1]
    qubo_mat = ising_mat * 4
    diag_vec = - 4 * np.sum(ising_mat, axis=0)
    bias = np.sum(ising_mat)
    if remove_linear_bit:
        bias -= np.sum(ising_mat_linear)
        diag_vec += 2 * ising_mat_linear
    qubo_mat = np.triu(qubo_mat * 2)
    np.fill_diagonal(qubo_mat, diag_vec)
    qubo_mat = np.array(qubo_mat, dtype=np.float64)
    return -qubo_mat, -float(bias)


def qubo_matrix_to_ising_matrix(qubo_mat):
    """QUBO矩阵转Ising矩阵

    Args:
        qubo_mat (np.ndarray): QUBO矩阵

    Returns:
        tuple: Ising矩阵和bias
            - ising_mat (np.ndarray): Ising矩阵
            - bias (float): QUBO与Ising相差的常数项

    Examples:
        >>> import numpy as np
        >>> import kaiwu_community as kw
        >>> matrix = -np.array([[-4.,  8.,  0.,  8.],
        ...                     [-0., -4.,  0.,  8.],
        ...                     [-0., -0., -0.,  8.],
        ...                     [-0., -0., -0., -8.]])
        >>> _ising_mat, _ = kw.conversion.qubo_matrix_to_ising_matrix(matrix)
        >>> _ising_mat
        array([[-0.,  1., -0.,  1.,  1.],
               [ 1., -0., -0.,  1.,  1.],
               [-0., -0., -0.,  1.,  1.],
               [ 1.,  1.,  1., -0.,  1.],
               [ 1.,  1.,  1.,  1., -0.]])
    """
    # 计算前转Decimal以防精度损失
    qubo_mat = np.vectorize(str)(qubo_mat)
    qubo_mat = np.vectorize(Decimal)(qubo_mat)

    ising_size = qubo_mat.shape[0] + 1
    ising_mat = np.zeros((ising_size, ising_size))
    qubo_mat = (qubo_mat + qubo_mat.T) / 8
    qubo_div_4_diagoal = np.diagonal(qubo_mat).copy()
    qubo_div_4 = qubo_mat
    np.fill_diagonal(qubo_div_4, 0)
    ising_mat[:-1, :-1] = qubo_div_4
    ising_mat[-1, :-1] = np.sum(qubo_div_4, axis=0) + qubo_div_4_diagoal
    ising_mat[:-1, -1] = np.sum(qubo_div_4, axis=0) + qubo_div_4_diagoal
    bias = np.sum(qubo_div_4) + np.sum(qubo_div_4_diagoal) * 2
    ising_mat = np.array(ising_mat, dtype=np.float64)
    return -ising_mat, float(bias)


if __name__ == '__main__':
    import doctest

    doctest.testmod()

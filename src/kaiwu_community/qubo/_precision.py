# -*- coding: utf-8 -*-
"""
模块: qubo

功能: 校验、调整QUBO模型参数精度，满足真机位宽限制
"""
from kaiwu_community.ising import calculate_ising_matrix_bit_width, adjust_ising_matrix_precision
from kaiwu_community.conversion import qubo_matrix_to_ising_matrix, ising_matrix_to_qubo_matrix


def check_qubo_matrix_bit_width(qubo_matrix, bit_width=8):
    """校验QUBO矩阵元素位宽

    将QUBO矩阵转为伊辛矩阵，通过校验伊辛矩阵的元素位宽来实现对QUBO矩阵的校验

    Args:
        qubo_matrix (np.ndarray): QUBO矩阵

        bit_width (int): 位宽

    Raises:
        ValueError: 当矩阵元素位宽超过指定位宽时抛出异常

    Examples1:
        >>> import numpy as np
        >>> import kaiwu_community as kw
        >>> _matrix = -np.array([[-480., 508., -48.],
        ...                      [ 508., -508., -48.],
        ...                      [ -48., -48., 60.]])
        >>> kw.qubo.check_qubo_matrix_bit_width(_matrix)

    Examples2（缩放后符合要求）:
        >>> import numpy as np
        >>> import kaiwu_community as kw
        >>> _matrix = -np.array([[-512.,  520.,  -48.],
        ...                      [ 520., -520.,  -48.],
        ...                      [ -48.,  -48.,   40.]])
        >>> kw.qubo.check_qubo_matrix_bit_width(_matrix)

    Examples3(缩放后也不符合要求):
        >>> import numpy as np
        >>> import kaiwu_community as kw
        >>> _matrix = -np.array([[-488.,  516.,  -48.],
        ...                      [ 516., -516.,  -48.],
        ...                      [ -48.,  -48.,   60.]])
        >>> kw.qubo.check_qubo_matrix_bit_width(_matrix)
        Traceback (most recent call last):
        ...
        ValueError: CIM only supports signed 8-bit number
    """
    # qubo模型转ising
    ising_matrix, _ = qubo_matrix_to_ising_matrix(qubo_matrix)
    result = calculate_ising_matrix_bit_width(ising_matrix, bit_width)
    if result.get('precision') > bit_width:
        raise ValueError("CIM only supports signed 8-bit number")


def adjust_qubo_matrix_precision(qubo_matrix, bit_width=8):
    """调整矩阵精度, 通过此接口调整后矩阵可能会有较大的精度损失，比如矩阵有一个数远大于其它数时，调整后矩阵精度损失严重无法使用

    Args:
        qubo_matrix (np.ndarray): 目标矩阵

        bit_width (int): 精度范围，目前只支持8位，有一位是符号位

    Returns:
        np.ndarray: 符合精度要求的QUBO矩阵

    Examples:
        >>> import numpy as np
        >>> import kaiwu_community as kw
        >>> ori_qubo_mat1 = np.array([[0.89, 0.22, 0.198],
        ...                      [0.22, 0.23, 0.197],
        ...                      [0.198, 0.197, 0.198]])
        >>> qubo_mat1 = kw.qubo.adjust_qubo_matrix_precision(ori_qubo_mat1)
        >>> qubo_mat1
        array([[348., 168., 152.],
               [ -0.,  92., 152.],
               [ -0.,  -0.,  80.]])
        >>> ori_qubo_mat2 = np.array([[0.89, 0.22, 0.198],
        ...                           [0.22, 0.23, 0.197],
        ...                           [0.198, 0.197, 100]])
        >>> qubo_mat2 = kw.qubo.adjust_qubo_matrix_precision(ori_qubo_mat2)
        >>> qubo_mat2  # The solutions obtained by qubo_mat2 and ori_qubo_mat2 matrices are quite different
        array([[  8.,  -0.,  -0.],
               [ -0.,   4.,  -0.],
               [ -0.,  -0., 508.]])
    """
    # qubo矩阵转ising
    ising_matrix, _ = qubo_matrix_to_ising_matrix(qubo_matrix)
    # 校验矩阵精度范围，如何符合要求直接返回
    result = calculate_ising_matrix_bit_width(ising_matrix)
    if result.get('precision') > bit_width:
        _ising_matrix = adjust_ising_matrix_precision(ising_matrix, bit_width)
        # 符合精度要求的qubo矩阵
        qubo_matrix, _ = ising_matrix_to_qubo_matrix(_ising_matrix)
    return qubo_matrix


if __name__ == '__main__':
    import doctest

    doctest.testmod()

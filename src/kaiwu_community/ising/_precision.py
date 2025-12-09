# -*- coding: utf-8 -*-
"""
提供Ising矩阵精度校验相关功能
"""
import numpy as np


def calculate_ising_matrix_bit_width(ising_matrix, bit_width=8):
    """计算 ising 矩阵的参数位宽

    Args:
        ising_matrix (np.ndarray): ising 矩阵

        bit_width (int): 最大位宽限制

    Returns:
        dict: 返回Ising矩阵的精度和缩放因子

            - precision (int): Ising矩阵精度
            - multiplier (float): 缩放因子

    示例1:
        >>> import numpy as np
        >>> import kaiwu_community as kw
        >>> _matrix = -np.array([[ -0., 127., -12.,  -5.],
        ...                      [127.,  -0., -12., -12.],
        ...                      [-12., -12.,  -0.,  -9.],
        ...                      [ -5., -12.,  -9.,  -0.]])
        >>> kw.ising.calculate_ising_matrix_bit_width(_matrix)
        {'precision': 8, 'multiplier': np.float64(1.0)}

    示例2（缩放后符合要求）:
        >>> import numpy as np
        >>> import kaiwu_community as kw
        >>> _matrix = -np.array([[ -0., 12.7, -1.2,  -0.5],
        ...                      [12.7,  -0., -1.2, -1.2],
        ...                      [-1.2, -1.2, -0.,   -0.9],
        ...                      [-0.5, -1.2, -0.9,  -0.]])
        >>> kw.ising.calculate_ising_matrix_bit_width(_matrix)
        {'precision': 8, 'multiplier': np.float64(10.0)}

    示例3(缩放后也不符合要求):
        >>> import numpy as np
        >>> import kaiwu_community as kw
        >>> _matrix = -np.array([[-488.,  516.,  -48.],
        ...                      [ 516., -516.,  -48.],
        ...                      [ -48.,  -48.,   60.]])
        >>> kw.ising.calculate_ising_matrix_bit_width(_matrix)
        {'precision': inf, 'multiplier': inf}
    """
    bit_width = bit_width - 1  # 留一位符号位

    if not np.any(ising_matrix):
        return np.inf, np.inf

    abs_matrix = np.abs(ising_matrix)
    threshold = 1e-10
    non_zero_elements = abs_matrix[np.where(np.abs(abs_matrix) > threshold)]
    normalization_factor = np.min(non_zero_elements)
    normalized_matrix = ising_matrix / normalization_factor
    abs_normalized_matrix = np.abs(normalized_matrix)
    scaling_factor_upper_limit = int(np.floor(2 ** bit_width / abs_normalized_matrix.max())) + 1

    for i in range(1, scaling_factor_upper_limit):
        scaled_normalized_matrix = ising_matrix * i / normalization_factor
        if np.array_equal(np.around(scaled_normalized_matrix, decimals=0),
                          np.around(scaled_normalized_matrix, decimals=8)):
            for j in range(1, bit_width + 1):
                upper_bound = 2 ** j
                if np.around(scaled_normalized_matrix.max()) == upper_bound:
                    continue
                if i < int(np.floor(upper_bound / abs_normalized_matrix.max())) + 1:
                    return {"precision": j + 1, "multiplier": i / normalization_factor}

    return {"precision": np.inf, "multiplier": np.inf}


def adjust_ising_matrix_precision(ising_matrix, bit_width=8):
    """调整 ising 矩阵精度, 通过此接口调整后矩阵可能会有较大的精度损失，比如矩阵有一个数远大于其它数时，调整后矩阵精度损失严重无法使用

    Args:
        ising_matrix(np.ndarray): 目标矩阵

        bit_width(int): 精度范围，目前只支持8位，有一位是符号位

    Returns:
        np.ndarray: 符合精度要求的 ising 矩阵

    Examples:
        >>> import numpy as np
        >>> import kaiwu_community as kw
        >>> ori_ising_mat1 = np.array([[0, 0.22, 0.198],
        ...                            [0.22, 0, 0.197],
        ...                            [0.198, 0.197, 0]])
        >>> ising_mat1 = kw.ising.adjust_ising_matrix_precision(ori_ising_mat1)
        >>> ising_mat1
        array([[  0, 127, 114],
               [127,   0, 114],
               [114, 114,   0]])
        >>> ori_ising_mat2 = np.array([[0, 0.22, 0.198],
        ...                            [0.22, 0, 50],
        ...                            [0.198, 50, 0]])
        >>> ising_mat2 = kw.ising.adjust_ising_matrix_precision(ori_ising_mat2)
        >>> ising_mat2  # The solutions obtained by qubo_mat2 and ori_qubo_mat2 matrices are quite different
        array([[  0,   1,   1],
               [  1,   0, 127],
               [  1, 127,   0]])
    """
    # 校验矩阵精度范围，如何符合要求直接返回
    result = calculate_ising_matrix_bit_width(ising_matrix, bit_width)
    if result.get('precision') > bit_width:
        # 保留一位符号位
        bit_width = bit_width - 1
        # 取绝对值
        abs_matrix = np.abs(ising_matrix)
        # 缩放因子
        factor = (2 ** bit_width - 1) / abs_matrix.max()
        # 小数位数
        decimal_bit_width = 0
        # 符合精度要求的ising矩阵
        ising_matrix = np.round(factor * ising_matrix * pow(2, decimal_bit_width)).astype(int)
    return ising_matrix


if __name__ == '__main__':
    import doctest

    doctest.testmod()

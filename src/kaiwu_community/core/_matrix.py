# -*- coding: utf-8 -*-
"""
时间: 2021-07-07
作者: wangyong@boseq.com
"""
from typing import Union, Tuple, List
import numpy as np
from kaiwu_community.core._binary_expression import quicksum
from kaiwu_community.core._expression import Expression


def dot(mat_left, mat_right):
    """矩阵乘法

    Args:
        mat_left (numpy.array): 矩阵1

        mat_right (numpy.array): 矩阵2

    Raises:
        ValueError: 两个输入都必须是np.ndarray
        ValueError: 两个输入的维度必须匹配

    Returns:
        np.ndarray: 乘积矩阵
    """
    # 检查输入是否为NumPy数组
    if not isinstance(mat_left, np.ndarray) or not isinstance(mat_right, np.ndarray):
        raise ValueError("Both inputs must be NumPy arrays")
    left_is_vector = len(mat_left.shape) == 1
    right_is_vector = len(mat_right.shape) == 1
    # 为了方便使用矩阵运算的写法进行运算，根据位置把向量补全成为矩阵
    if left_is_vector:
        mat_left = mat_left[np.newaxis, :]
    if right_is_vector:
        mat_right = mat_right[:, np.newaxis]
    mat_right = mat_right.swapaxes(-1, -2)

    # 获取数组的形状
    mat_left_shape = mat_left.shape
    mat_right_shape = mat_right.shape

    # 确保两个输入的最后一个维度相同，或者其中一个是1
    if mat_left_shape[-1] != mat_right_shape[-1]:
        raise ValueError("The last dimension of A must be equal to the"
                         " second last dimension of B for dot product")

    # 初始化结果数组
    result_shape = mat_left_shape[:-1] + mat_right_shape[:-1]
    result = BinaryExpressionNDArray(result_shape, dtype=Expression)

    # 使用嵌套循环和np.sum来实现多维点积
    for a_idx in np.ndindex(mat_left_shape[:-1]):
        for b_idx in np.ndindex(mat_right_shape[:-1]):
            result[a_idx + b_idx] = quicksum((mat_left[a_idx] * mat_right[b_idx]).tolist())

    if right_is_vector:
        result = result.squeeze(-1)
    if left_is_vector:
        result = result[0]
    return result


def _is_less(qubo_left, qubo_right):
    return qubo_left < qubo_right


def _is_less_equal(qubo_left, qubo_right):
    return qubo_left <= qubo_right


def _is_greater(qubo_left, qubo_right):
    return qubo_left > qubo_right


def _is_greater_equal(qubo_left, qubo_right):
    return qubo_left >= qubo_right


def _is_equal(qubo_left, qubo_right):
    return qubo_left == qubo_right


class BinaryExpressionNDArray(np.ndarray):
    """基于 np.ndarray 的QUBO容器.
    该容器支持各种 numpy 原生的向量化运算
    """

    def __lt__(self, other):
        return np.vectorize(_is_less)(self, other)

    def __le__(self, other):
        return np.vectorize(_is_less_equal)(self, other)

    def __gt__(self, other):
        return np.vectorize(_is_greater)(self, other)

    def __ge__(self, other):
        return np.vectorize(_is_greater_equal)(self, other)

    def __eq__(self, other):
        return np.vectorize(_is_equal)(self, other)

    def __matmul__(self, other):
        return self.dot(other)

    def dot(self, b, out=None):
        """使用quicksum的矩阵乘法

        Args:
            b (BinaryExpressionNDArray): 另一个矩阵

            out: 可选输出数组，用于存储结果。需与预期输出形状一致。

        Returns:
            BinaryExpressionNDArray: 乘积
        """
        if out is not None:
            idx = (slice(None),) * len(out.shape)
            out[idx] = dot(self, b)
            return out
        return dot(self, b)

    # pylint: disable=W0613, R0917
    def sum(self, axis=None, dtype=None, out=None, keepdims=False, initial=0, where=True):
        """使用quicksum的求和方法

        Args:
            axis: 指定求和的轴（维度）。默认为 None，表示对所有元素求和；若为整数或元组，则沿指定轴求和。

            dtype: 指定输出数据类型。若未提供，则默认使用输入数组的 dtype，但整数类型可能提升为平台整数精度。暂不支持。

            out: 可选输出数组，用于存储结果。需与预期输出形状一致。

            keepdims: 布尔值。若为 True，则保留被求和的轴作为长度为1的维度。暂不支持 。

            initial: 求和的初始值（标量），默认为0。暂不支持。

            where: 布尔数组，指定哪些元素参与求和（NumPy 1.20+支持）。暂不支持。

        Returns:
            BinaryExpressionNDArray: 乘积
        """
        # 检查输入是否为NumPy数组
        if not isinstance(self, np.ndarray):
            raise ValueError("Input must be a NumPy array")
        # 如果没有指定轴，则对整个数组求和
        if axis is None:
            # 将数组展平成一个列表并使用quicksum求和
            return quicksum(self.flatten().tolist())
        # 指定轴的情况
        if axis < 0:
            axis += self.ndim  # 转换负轴索引为正轴索引

        # 初始化结果数组
        new_shape = self.shape[:axis] + self.shape[axis + 1:]
        result = BinaryExpressionNDArray(new_shape, dtype=Expression)

        # 对指定轴进行求和
        for idx in np.ndindex(new_shape):
            # 获取当前轴的子数组
            sub_array = self[idx[:axis] + (slice(None),) + idx[axis:]]
            result[idx] = quicksum(sub_array.flatten().tolist())

        if out is not None:
            idx = (slice(None),) * len(out.shape)
            out[idx] = result
            return out
        if not result.shape:
            result = result.tolist()
        return result


def ndarray(shape: Union[int, Tuple[int, ...], List[int]], name, var_func, var_func_param=None):
    """基于 np.ndarray 的QUBO容器.
    该容器支持各种 numpy 原生的向量化运算

    Args:
        shape (Union[int, Tuple[int, ...]]): 形状

        name (str): 生成的变量的标识符.

        var_func (class for func): 用于生成元素的方法或类. 第一个参数必须是name

        var_func_param (tuple): var_func除了name以外的参数 

    Returns:
        np.ndarray: 多维容器.

    Examples:
        >>> import numpy as np
        >>> import kaiwu_community as kw
        >>> A = kw.core.ndarray((2,3,4), "A", kw.core.Binary)
        >>> A
        BinaryExpressionNDArray([[[A[0][0][0], A[0][0][1], A[0][0][2],
                                   A[0][0][3]],
                                  [A[0][1][0], A[0][1][1], A[0][1][2],
                                   A[0][1][3]],
                                  [A[0][2][0], A[0][2][1], A[0][2][2],
                                   A[0][2][3]]],
        <BLANKLINE>
                                 [[A[1][0][0], A[1][0][1], A[1][0][2],
                                   A[1][0][3]],
                                  [A[1][1][0], A[1][1][1], A[1][1][2],
                                   A[1][1][3]],
                                  [A[1][2][0], A[1][2][1], A[1][2][2],
                                   A[1][2][3]]]], dtype=object)
        >>> A[1,2]
        BinaryExpressionNDArray([A[1][2][0], A[1][2][1], A[1][2][2], A[1][2][3]],
                                dtype=object)
        >>> A[:, [0,2]]
        BinaryExpressionNDArray([[[A[0][0][0], A[0][0][1], A[0][0][2],
                                   A[0][0][3]],
                                  [A[0][2][0], A[0][2][1], A[0][2][2],
                                   A[0][2][3]]],
        <BLANKLINE>
                                 [[A[1][0][0], A[1][0][1], A[1][0][2],
                                   A[1][0][3]],
                                  [A[1][2][0], A[1][2][1], A[1][2][2],
                                   A[1][2][3]]]], dtype=object)
        >>> B = kw.core.ndarray(3, "B", kw.core.Binary)
        >>> B
        BinaryExpressionNDArray([B[0], B[1], B[2]], dtype=object)
        >>> C = kw.core.ndarray([3,3], "C", kw.core.Binary)
        >>> C
        BinaryExpressionNDArray([[C[0][0], C[0][1], C[0][2]],
                                 [C[1][0], C[1][1], C[1][2]],
                                 [C[2][0], C[2][1], C[2][2]]], dtype=object)
        >>> D = 2 * B.dot(C) + 2
        >>> str(D[0])
        '2*B[0]*C[0][0]+2*B[1]*C[1][0]+2*B[2]*C[2][0]+2'
        >>> E = B.sum()
        >>> str(E)
        'B[0]+B[1]+B[2]'
        >>> F = np.diag(C)
        >>> F
        BinaryExpressionNDArray([C[0][0], C[1][1], C[2][2]], dtype=object)
    """
    if isinstance(shape, int):
        shape = (shape,)
    if isinstance(shape, list):
        shape = tuple(shape)
    if 0 in shape:
        raise ValueError("The argument shape cannot contain 0.")
    if var_func_param is None:
        var_func_param = ()

    arr = BinaryExpressionNDArray(shape, dtype=Expression)
    for idx in np.ndindex(shape):
        item_str = name
        for i, idx_i in enumerate(idx):
            len_str_k = len(str(shape[i] - 1))
            item_str += f"[{str(idx_i).zfill(len_str_k)}]"
        arr[idx] = var_func(item_str, *var_func_param)
    return arr


if __name__ == '__main__':
    import doctest

    doctest.testmod()

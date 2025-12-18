"""
一些简单的工具
"""

import numpy as np


def check_symmetric(mat, tolerance=1e-8):
    """检查矩阵是否为对称矩阵，允许一定误差

    Args:
        mat (np.ndarray): 矩阵.

        tolerance (float): 误差.

    Returns:
        bool: 是否为对称矩阵.

    Examples:
        >>> import numpy as np
        >>> import kaiwu_community as kw
        >>> ising_matrix = -np.array([[ 0. ,  1. ,  0. ,  1. ,  1. ],
        ...                           [ 1. ,  0. ,  0. ,  1.,   1. ],
        ...                           [ 0. ,  0. ,  0. ,  1.,   1. ],
        ...                           [ 1. ,  1.,   1. ,  0. ,  1. ],
        ...                           [ 1. ,  1.,   1. ,  1. ,  0. ]])
        >>> print(kw.common.check_symmetric(ising_matrix))
        True
    """
    result = np.all(np.abs(mat - mat.T) < tolerance)
    return result


def hamiltonian(ising_matrix, c_list):
    """计算哈密顿量.

    Args:
        ising_matrix (np.ndarray): CIM Ising 矩阵.

        c_list (np.ndarray): 要计算哈密顿量的变量组合集合.

    Returns:
        np.ndarray: 哈密顿量集合.

    Examples:
        >>> import numpy as np
        >>> import kaiwu_community as kw
        >>> ising_matrix = -np.array([[ 0. ,  1. ,  0. ,  1. ,  1. ],
        ...                     [ 1. ,  0. ,  0. ,  1.,   1. ],
        ...                     [ 0. ,  0. ,  0. ,  1.,   1. ],
        ...                     [ 1. ,  1.,   1. ,  0. ,  1. ],
        ...                     [ 1. ,  1.,   1. ,  1. ,  0. ]])
        >>> rng = np.random.default_rng(10)
        >>> optimizer = kw.classical.BruteForceOptimizer()
        >>> output = optimizer.solve(ising_matrix)
        >>> h = kw.common.hamiltonian(ising_matrix, output)
        >>> h   # doctest: +SKIP
        array([-0.60179257, -0.60179257, -0.60179257, -0.60179257, -0.60179257,
               -1.20358514, -0.60179257, -0.60179257, -0.60179257, -1.20358514])
    """
    # 方法1 by 王勇 邵帅 (最快版)
    return -np.einsum("ij,ij->i", (c_list.dot(ising_matrix)), c_list)

    # 方法2 by 王勇 邵帅
    # return ((c_list.dot(matrix))*c_list).sum(axis=1)
    #
    # 方法3 by 王勇
    # temp = c_list.dot(matrix)
    # return -np.array([temp[i] * c_list[i] for i in range(len(c_list))])
    #
    # 方法4 by 王勇
    # return -np.diag((c_list.dot(matrix)).dot(c_list.T)) # 空间复杂度高
    #
    # 方法5 by 邵帅
    # return -np.einsum('ij,ik,jk->i', c_list, c_list, matrix)


if __name__ == '__main__':
    import doctest

    doctest.testmod()

# -*- coding: utf-8 -*-
"""
ising矩阵暴力求解器
"""
import math
import numpy as np
from kaiwu_community.core import OptimizerBase


class BruteForceOptimizer(OptimizerBase):
    """求解Ising模型矩阵的暴力求解器，慢而准."""

    def solve(self, ising_matrix=None):
        """求解Ising矩阵solve接口

        Args:
            ising_matrix (np.ndarray, optional): Ising矩阵. Defaults to None.

        Returns:
            np.ndarray: 1个或者多个能量最低的解向量.

        Examples:
            >>> import kaiwu_community as kw
            >>> import numpy as np
            >>> mat = np.array([[0, 2, -3],[2, 0, -1],[-3, -1, 0]])
            >>> optimizer = kw.classical.BruteForceOptimizer()
            >>> optimizer.solve(mat)
            array([[-1, -1,  1],
                   [-1, -1,  1]])

        """
        size = ising_matrix.shape[0]
        h_ret = math.inf
        solutions = []
        for i in range(2 ** size):
            val = i
            vlist = [0] * size
            for j in range(size):
                vlist[j] = val % 2
                val //= 2
            sol = np.array(vlist) * 2 - 1
            hmt = -sol.dot(ising_matrix).dot(sol)
            if hmt < h_ret:
                h_ret = hmt
                solutions = [sol]
            elif hmt == h_ret:
                solutions.append(sol)
        sols = np.array(solutions)
        sols[sols[:, -1] <= 0, :] *= -1
        return sols

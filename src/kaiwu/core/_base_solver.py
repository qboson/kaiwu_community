"""
基础模块 Optimizer base class
"""

import logging
import abc
import numpy as np

from ._model_converter import qubo_model_to_ising_model
from ._get_val import get_sol_dict

logger = logging.getLogger(__name__)


class IsingSolver:
    """
    Ising求解器基类
    """

    def __init__(self):
        self.matrix = None

    def set_matrix(self, ising_matrix):
        """设置矩阵并更新相关内容"""
        if ising_matrix is not None:
            self.matrix = ising_matrix
            self.on_matrix_change()
            logger.debug("Matrix set in the optimizer.")
        if self.matrix is None:
            raise ValueError("Ising matrix must be set")

    def on_matrix_change(self):
        """
        更新矩阵相关信息, 继承IsingSolver时可以实现。当处理的ising矩阵发生变化时，这个函数的实现会被调用，从而有机会做相应动作
        """

        logger.debug(
            "Method on_matrix_change is not implemented in the class inherited from IsingSolver!"
        )

    def _solve(self, ising_matrix=None):
        "求解逻辑"
        raise NotImplementedError

    def solve(self, ising_matrix=None, negtail_flip=True, sort_solutions=False):
        """求解Ising矩阵

        Args:
            ising_matrix (np.ndarray): Ising矩阵

            negtail_flip (bool): 是否进行负尾翻转

            sort_solutions (bool): 是否对解进行排序

        Returns:
            output (np.ndarray): 解向量
        """
        self.set_matrix(ising_matrix)
        solutions = self._solve(self.matrix)
        solutions, self._hamiltonian = get_sorted_solutions(
            self.matrix, solutions, 0, negtail_flip, sort_solutions
        )
        return solutions

    def get_hamiltonian(self):
        """
        Returns:
            float: 当前Hamiltonian值
        """
        return self._hamiltonian

    def _to_ising_matrix(self, qubo_model):
        ising_model = qubo_model_to_ising_model(qubo_model)
        ising_mat = ising_model.get_matrix()
        bias = ising_model.get_bias()
        vars_dict = ising_model.get_variables()
        return ising_mat, bias, vars_dict

    def solve_qubo(self, qubo_model):
        """求解QUBO模型"""
        if isinstance(self, IsingSolver):
            ising_mat, bias, vars_dict = self._to_ising_matrix(qubo_model)
            output = self.solve(ising_mat)
            if output is None:
                return None, None
            solutions, hamiltons = get_sorted_solutions(
                ising_mat, output, 0, negtail_ff=True, sort_solution=True
            )
            solution_dict = get_sol_dict(
                solutions[0][:-1] * solutions[0][-1], vars_dict
            )
            return solution_dict, hamiltons[0] + bias
        raise NotImplementedError


class QuboSolverMeta(abc.ABCMeta):
    """Solver自定义元类"""

    def __new__(mcs, name, bases, namespace, **kwargs):
        if name != "Base" and "solve_qubo" in namespace:
            original_execute = namespace["solve_qubo"]

            def wrapped_execute(self, *args, **kwargs):
                result = original_execute(self, *args, **kwargs)
                if result[0] is None:
                    logger.warning("No solution found!")
                return result

            namespace["solve_qubo"] = wrapped_execute
        return super().__new__(mcs, name, bases, namespace, **kwargs)


class QuboSolver(metaclass=QuboSolverMeta):
    """Solver基类

    Args:
        optimizer (IsingSolver): Ising求解器
    """

    def __init__(self, optimizer):
        self._optimizer = optimizer

    @abc.abstractmethod
    def solve_qubo(self, qubo_model):
        """求解QUBO

        Args:
            qubo_model (QuboModel): QUBO模型

        Returns:
            tuple: 元组，包含求解结果信息
                - dict: 解字典
                - float: QUBO值
        """
        raise NotImplementedError


def get_sorted_solutions(matrix, c_set, bias=0.0, negtail_ff=True, sort_solution=True):
    """对解决方案进行排序

    Args:
        matrix (np.ndarray): CIM Ising 矩阵
        c_set (np.ndarray): 候选解集合
        bias (float): 偏置值
        negtail_ff (bool): 是否进行末尾翻转
        sort_solution (bool): 是否对结果排序

    Returns:
        tuple: (sorted_c_set, hamiltonians) 排序后的解集合和对应的哈密顿量值
    """
    hamilton = -np.einsum("ij,ij->i", (c_set.dot(matrix)), c_set) + bias
    if sort_solution:
        index = np.argsort(hamilton)
        c_set = c_set[index]
        hamilton = hamilton[index]
    if negtail_ff:
        c_set = c_set * c_set[:, [-1]]
    return c_set, hamilton

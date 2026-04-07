"""
基础模块 Optimizer base class
"""

import logging
import abc

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

    def solve(self, ising_matrix=None):
        """求解"""
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

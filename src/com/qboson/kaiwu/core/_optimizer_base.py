"""
基础模块 Optimizer base class
"""
import logging

logger = logging.getLogger(__name__)


class OptimizerBase:
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
        更新矩阵相关信息, 继承OptimizerBase时可以实现。当处理的ising矩阵发生变化时，这个函数的实现会被调用，从而有机会做相应动作
        """

        logger.debug("Method on_matrix_change is not implemented in the class inherited from OptimizerBase!")

    def solve(self, ising_matrix=None):
        """求解"""
        raise NotImplementedError

# encoding=utf8
"""
SolverBase
Provide some basic implementation of solver and its interface
"""
import logging
import abc
from functools import wraps

logger = logging.getLogger(__name__)


class SolverBaseMeta(abc.ABCMeta):
    """Solver自定义元类"""

    def __new__(mcs, name, bases, namespace, **kwargs):
        if name != 'Base' and 'solve_qubo' in namespace:
            original_execute = namespace['solve_qubo']

            @wraps(original_execute)
            def wrapped_execute(self, *args, **kwargs):
                result = original_execute(self, *args, **kwargs)
                if result[0] is None:
                    logger.warning("No solution found!")
                return result

            namespace['solve_qubo'] = wrapped_execute
        return super().__new__(mcs, name, bases, namespace, **kwargs)


class SolverBase(metaclass=SolverBaseMeta):
    """Solver基类

    Args:
        optimizer (OptimizerBase): Ising求解器
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

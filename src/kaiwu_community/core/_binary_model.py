"""
模块: Model

功能: Binary Model基础类
"""
import collections.abc
import copy
from typing import Literal
import logging
import numpy as np
from kaiwu_community.core._penalty_method_constraint import PenaltyMethodConstraint
from kaiwu_community.core._constraint import get_min_penalty_from_min_diff, get_soft_penalty
from kaiwu_community.core._get_val import get_val
from kaiwu_community.core._error import KaiwuError

logger = logging.getLogger(__name__)


class BinaryModel:
    """二值模型类

    Args:
        objective (BinaryExpression, optional): 目标函数. 默认为None
    """

    def __init__(self, objective=None):
        self.objective = copy.deepcopy(objective)
        self.hard_constraints = {}
        self.soft_constraints = {}
        self.hard_constraints_made = {}
        self.soft_constraints_made = {}
        self.compiled = False
        self.constraint_handler = PenaltyMethodConstraint

    def set_constraint_handler(self, constraint_handler):
        """设置约束项无约束化方法

        Args:
            constraint_handler: 设置约束项无约束化表示方法类
        """
        self.constraint_handler = constraint_handler

    def set_objective(self, objective):
        """设置目标函数

        Args:
            objective (BinaryExpression): 目标函数表达式
        """
        if self.objective is not None:
            raise KaiwuError("Object already exists, please reinitialize")
        self.objective = copy.deepcopy(objective)

    def add_constraint(self, constraint_in, name=None, constr_type: Literal["soft", "hard"] = "hard", penalty=None):
        """添加约束项（支持单个或多个约束）

        Args:
            constraint_in (ConstraintDefinition or iterable): 约束表达式或其可迭代对象

            name (str or list, optional): 约束名称或名称列表，默认自动命名

            constr_type (str, optional): 约束类型，可以设置为"soft"或"hard"，默认为"hard"

            penalty (float): 缺省惩罚系数
        """

        if constr_type not in ["hard", "soft"]:
            raise KaiwuError(f"No such type {constr_type}")

        # Handle multiple constraints
        if isinstance(constraint_in, (list, tuple, np.ndarray)) or (
            isinstance(constraint_in, collections.abc.Iterable) and not isinstance(constraint_in, (str, bytes))
        ):
            # If name is a list/tuple, use as names; else auto-generate
            names = name if isinstance(name, (list, tuple, np.ndarray)) else None
            for idx, constraint in enumerate(constraint_in):
                item_name = (
                    names[idx] if names is not None and idx < len(names)
                    else f"constraint{len(self.hard_constraints) + len(self.soft_constraints) + idx}"
                )
                self.add_constraint(constraint, item_name, constr_type, penalty)
            return

        # Single constraint
        if name is None:
            name = f"constraint{len(self.hard_constraints) + len(self.soft_constraints)}"
        if name in self.hard_constraints or name in self.soft_constraints:
            logger.warning("Constraint %s is already added. The original one will be replaced.", name)
        constraint_in.default_penalty = penalty
        if constr_type == "soft":
            self.soft_constraints[name] = constraint_in
        else:
            self.hard_constraints[name] = constraint_in

    def get_value(self, solution_dict):
        """根据结果字典将变量值带入qubo变量.

        Args:
            solution_dict (dict): 由get_sol_dict生成的结果字典。

        Returns:
            float: 带入qubo后所得的值
        """
        return get_val(self.objective, solution_dict)

    def verify_constraint(self, solution_dict, constr_type: Literal["soft", "hard"] = "hard"):
        """确认约束是否满足

        Args:
            solution_dict (dict): QUBO模型解字典

            constr_type(str, optional): 约束类型，可以设置为"soft"或"hard"，默认为"hard"

        Returns:
            tuple: 约束满足信息
                - int: 不满足的约束个数
                - dict: 包含约束值的字典
        """
        if constr_type not in ["soft", "hard"]:
            raise KaiwuError(f"No such type {constr_type}")
        unsatisfied_count = 0
        result_dict = {}
        temp_constraint_dicts = self.hard_constraints
        if constr_type == "soft":
            temp_constraint_dicts = self.soft_constraints

        for name, constr_info in temp_constraint_dicts.items():
            if not constr_info.is_satisfied(solution_dict):
                unsatisfied_count += 1
            result_dict[name] = get_val(constr_info.left_operand, solution_dict)

        logger.debug("unsatisfied %s constraints count = %s | objective = %s",
                     constr_type, unsatisfied_count, self.get_value(solution_dict))

        return unsatisfied_count, result_dict

    def initialize_penalties(self):
        """ 自动初始化所有的惩罚系数"""
        positive_delta = {}
        negative_delta = {}

        if self.objective is not None:
            negative_delta, positive_delta = self.objective.get_max_deltas()

        for _, constraint_info in self.hard_constraints_made.items():
            constraint_info.set_penalty(
                get_min_penalty_from_min_diff(constraint_info.constraint_expr, negative_delta, positive_delta))
        for _, constraint_info in self.soft_constraints_made.items():
            constraint_info.set_penalty(get_soft_penalty(self.objective, constraint_info.constraint_expr))

    def get_constraints_expr_list(self):
        """获取当前所有的constraint。

        Returns:
            List of all constraints.

        """

        constraint_expr_list = []
        for _, constraint_info in self.hard_constraints_made.items():
            constraint_expr_list.append(constraint_info.penalty * constraint_info.constraint_expr)
        for _, constraint_info in self.soft_constraints_made.items():
            constraint_expr_list.append(constraint_info.penalty * constraint_info.constraint_expr)
        return constraint_expr_list

    def compile_constraints(self):
        """ 按照不同的风格转换约束项为Expression
        对于不等式约束，目前支持的是罚函数方式，
        """
        if self.compiled:
            return
        if self.constraint_handler is None:
            raise KaiwuError("Please set constraint handler first!")

        # 整理约束项
        for name, constraint in self.hard_constraints.items():
            self.hard_constraints_made[name] = (
                self.constraint_handler.from_constraint_definition(name, constraint, self))
        for name, constraint in self.soft_constraints.items():
            self.soft_constraints_made[name] = (
                self.constraint_handler.from_constraint_definition(name, constraint, self))
        self.compiled = True

"""
模块: Model

功能: Binary Model基础类
"""

import copy
from typing import Literal
import logging
import numpy as np
from kaiwu.core._penalty_method_constraint import PenaltyMethodConstraint
from kaiwu.core._constraint import get_min_penalty_from_min_diff, get_soft_penalty
from kaiwu.core._get_val import get_val
from kaiwu.core._error import KaiwuError
from kaiwu.core._binary_expression import BinaryExpression
from kaiwu.core._constraint import Constraint

logger = logging.getLogger(__name__)


class BinaryModel:
    """二值模型类

    Args:
        objective (BinaryExpression, optional): 目标函数. 默认为None
    """

    def __init__(self, objective=None):
        if objective is None:
            self.objective = BinaryExpression({}, 0)
        else:
            self.objective = copy.deepcopy(objective)
        self.hard_constraints = {}
        self.soft_constraints = {}
        self.hard_constraints_made = {}
        self.soft_constraints_made = {}
        self.compiled = False
        self.constraint_handler = PenaltyMethodConstraint

        self._cnt = 0

    def __repr__(self):
        return f"{self.__class__.__name__}({vars(self)!r})"

    def __str__(self):
        print_data = f"Minimize {str(self.objective)}"
        if len(self.hard_constraints) > 0:
            print_data += "\nSubject to (hard constraints):\n"
            print_data += "\n".join(
                str(constr) for constr in self.hard_constraints.values()
            )
        if len(self.soft_constraints) > 0:
            print_data += "\nSubject to (soft constraints):\n"
            print_data += "\n".join(
                str(constr) for constr in self.soft_constraints.values()
            )
        return print_data

    def set_constraint_handler(self, constraint_handler):
        """设置约束项无约束化方法

        Args:
            constraint_handler: 设置约束项无约束化表示方法类
        """
        self.constraint_handler = constraint_handler

    def _on_objective_change(self):
        """当目标函数发生变化时调用，重置相关状态"""
        self.compiled = False

    def set_objective(self, objective):
        """设置目标函数

        Args:
            objective (BinaryExpression): 目标函数表达式
        """
        self.objective = copy.deepcopy(objective)
        self._on_objective_change()

    def add_constraint(
        self,
        constraint_in,
        name=None,
        constr_type: Literal["soft", "hard"] = "hard",
        penalty=1,
        slack_var_expr=None,
    ):
        """添加约束项，支持单个或多个约束

        Args:
            constraint_in: 约束表达式，支持两种输入类型：

                1. 单个约束: BinaryExpression 或 Constraint 对象
                   例如: ``quicksum(x) - 1`` 或 ``Constraint(quicksum(x) - 1, "==", 1)``

                2. 多个约束: list/tuple/np.ndarray，自动遍历逐个添加
                   例如: ``[constraint1, constraint2, constraint3]``

            name (str or list, optional): 约束名称，默认自动命名。当为多个约束时，
                若传入字符串则为公共前缀，若传入字符串列表则需与约束数量一致。

            penalty (float, optional): 缺省惩罚系数

            constr_type (str, optional): 约束类型，可以设置为"soft"或"hard"，默认为"hard"

            slack_var_expr (BinaryExpression, optional): 松弛变量表达式，仅在不等式约束中使用,
                默认为自动生成

        Examples:
            # 类型1: 单个 BinaryExpression
            >>> import kaiwu as kw
            >>> model = kw.core.QuboModel()
            >>> x = [kw.core.Binary(f"x{i}") for i in range(3)]
            >>> model.add_constraint(kw.core.quicksum(x) - 1)

            # 类型1: 单个 Constraint 对象 (带关系运算符)
            >>> from kaiwu.core._constraint import Constraint
            >>> model.add_constraint(Constraint(kw.core.quicksum(x) - 1, "==", 1))

            # 类型2: 多个约束 (list/tuple)
            >>> constraints = [x[i] - 1 for i in range(3)]
            >>> model.add_constraint(constraints, name="my_constraints")
        """
        if constr_type not in ["hard", "soft"]:
            raise KaiwuError(f"No such type {constr_type}")

        if isinstance(constraint_in, BinaryExpression):
            constraint_in = Constraint(constraint_in, None)

        # Handle multiple constraints
        if name is None:
            name = f"_constraint{self._cnt}"
            self._cnt += 1
        if isinstance(constraint_in, (list, tuple, np.ndarray)):
            if slack_var_expr is not None and not (
                type(slack_var_expr) is type(constraint_in)
                and len(slack_var_expr) == len(constraint_in)
            ):
                raise KaiwuError(
                    "Slack variable expression must match the type and shape of constraints."
                )
            len_str_k = len(str(len(constraint_in) - 1))
            for idx, constraint in enumerate(constraint_in):
                item_name = f"{name}[{str(idx).zfill(len_str_k)}]"
                tmp_slack = slack_var_expr[idx] if slack_var_expr is not None else None
                self.add_constraint(
                    constraint, item_name, constr_type, penalty, tmp_slack
                )
            return

        # Single constraint
        if name in self.hard_constraints or name in self.soft_constraints:
            logger.warning(
                "Constraint %s is already added. The original one will be replaced.",
                name,
            )
        constraint_in.default_penalty = penalty
        constraint_in.slack_var_expr = slack_var_expr
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

    def verify_constraint(
        self, solution_dict, constr_type: Literal["soft", "hard"] = "hard"
    ):
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

        logger.debug(
            "unsatisfied %s constraints count = %s | objective = %s",
            constr_type,
            unsatisfied_count,
            self.get_value(solution_dict),
        )

        return unsatisfied_count, result_dict

    def initialize_penalties(self):
        """自动初始化所有的惩罚系数"""
        positive_delta = {}
        negative_delta = {}

        if self.objective is not None:
            negative_delta, positive_delta = self.objective.get_max_deltas()

        for _, constraint_info in self.hard_constraints_made.items():
            constraint_info.set_penalty(
                get_min_penalty_from_min_diff(
                    constraint_info.constraint_expr, negative_delta, positive_delta
                )
            )
        for _, constraint_info in self.soft_constraints_made.items():
            constraint_info.set_penalty(
                get_soft_penalty(self.objective, constraint_info.constraint_expr)
            )

    def get_constraints_expr_list(self):
        """获取当前所有的constraint。

        Returns:
            list: 所有constraints的列表.

        """
        constraint_expr_list = []
        for _, constraint_info in self.hard_constraints_made.items():
            constraint_expr_list.append(
                constraint_info.penalty * constraint_info.constraint_expr
            )
        for _, constraint_info in self.soft_constraints_made.items():
            constraint_expr_list.append(
                constraint_info.penalty * constraint_info.constraint_expr
            )
        return constraint_expr_list

    def compile_constraints(self):
        """按照不同的风格转换约束项为Expression"""
        if self.compiled:
            return
        if self.constraint_handler is None:
            raise KaiwuError("Please set constraint handler first!")

        # 整理约束项
        for name, constraint in self.hard_constraints.items():
            self.hard_constraints_made[name] = (
                self.constraint_handler.from_constraint_definition(
                    name, constraint, self
                )
            )
        for name, constraint in self.soft_constraints.items():
            self.soft_constraints_made[name] = (
                self.constraint_handler.from_constraint_definition(
                    name, constraint, self
                )
            )
        self.compiled = True

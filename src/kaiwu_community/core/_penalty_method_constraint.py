# -*- coding: utf-8 -*-
"""
模块: core.PMConstraint

功能: 生成基于penalty method的约束项
"""
import logging
from kaiwu_community.core._binary_expression import Integer
from kaiwu_community.core._get_val import get_val
from kaiwu_community.core._constraint import ConstraintDefinition
logger = logging.getLogger(__name__)


class PenaltyMethodConstraint:
    """有约束转无约束的penalty method方法

    Args:
        expr (Expression): 编译后的约束项表达式

        penalty (float): 约束项惩罚系数

    """

    def __init__(self, expr, penalty=1, parent_model=None):

        self.constraint_expr = expr
        self.previous_penalty = 1
        self.penalty = penalty
        self.pre_constr_val = 0
        self.current_value = 0
        self._parent_model = parent_model

    @classmethod
    def from_constraint_definition(cls, name, constraint: ConstraintDefinition, parent_model):

        """Prepare QUBO expression for the given constraint, automatically determining slack variables if needed.

        Args:
         name: Name of the constraint.

         constraint: The relation constraint to process.

         parent_model: the model it belongs to.

        """

        if constraint.relation == '==':
            # 等式约束直接平方处理
            expr = constraint.left_operand - constraint.expected_value
        else:
            # 处理不等式约束的方向
            diff_qubo = _adjust_inequality_direction(constraint)
            slack_expr = _create_slack_variable(name, diff_qubo, constraint.relation)
            # 构建最终的约束表达式（等式平方形式）
            expr = diff_qubo + slack_expr - constraint.expected_value
            expr = expr ** 2

        logger.debug("Constraint expression: %s", expr)

        return PenaltyMethodConstraint(expr, constraint.default_penalty, parent_model)

    def set_penalty(self, penalty):
        """ 设置惩罚系数"""
        if penalty is None:
            penalty = 1
        self.previous_penalty = self.penalty
        self.penalty = penalty
        if self._parent_model:
            self._parent_model.invalidate_made_state()
        logger.debug("Penalty: %s Constraint expression: %s", self.penalty, self.constraint_expr)

    def penalize_more(self):
        """增加惩罚系数"""
        self.set_penalty(self.penalty * 2)

    def penalize_less(self):
        """降低惩罚系数"""
        if self.previous_penalty is None:
            self.previous_penalty = 0
        self.set_penalty((self.previous_penalty + self.penalty) / 2)

    def __str__(self):
        return f"penalty={self.penalty}, constraint_expr={self.constraint_expr}"

    def __repr__(self) -> str:
        return self.__str__()

    def is_satisfied(self, solution_dict):
        """验证约束满足情况"""
        self.current_value = float(get_val(self.constraint_expr, solution_dict))
        return abs(self.current_value) < 1e-5


def _find_min_interval(diff_qubo):
    """找到系数间的最小正间隔"""
    coefficients = sorted(diff_qubo.coefficient.values())
    # 添加0以处理边界情况
    coefficients.append(0)
    # 计算相邻系数的最小正差值
    min_diff = min(
        abs(coefficients[i + 1] - coefficients[i])
        for i in range(len(coefficients) - 1)
        if coefficients[i + 1] != coefficients[i]
    )
    return min_diff


def _calculate_slack_range(diff_qubo):
    """计算松弛变量的最大取值范围"""
    # 累加所有负系数（考虑最坏情况）
    negative_sum = sum(-v for v in diff_qubo.coefficient.values() if v < 0)
    # 计算初始范围并确保非负
    slack_range = max(0, negative_sum - diff_qubo.offset)
    return slack_range


def _create_slack_variable(name, diff_qubo, relation):
    """自动创建松弛变量表达式"""
    # 确定松弛变量的最小值
    slack_min = 0 if relation in ['>=', '<='] else 1

    # 计算松弛变量的取值范围
    slack_range = _calculate_slack_range(diff_qubo)
    if slack_range == 0:
        raise ValueError("Slack range cannot be zero for non-equality constraint")

    # 确定离散化精度
    min_diff = _find_min_interval(diff_qubo)
    precision_steps = int(round(slack_range / min_diff))

    # 创建整数变量并线性缩放
    slack_var = Integer(f"_slack_{name}", slack_min, precision_steps + slack_min)
    return slack_var * (slack_range / precision_steps)


def _adjust_inequality_direction(constraint):
    """根据不等式方向调整QUBO表达式符号"""
    if constraint.relation in ['>', '>=']:
        return -constraint.left_operand
    return constraint.left_operand

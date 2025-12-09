# -*- coding: utf-8 -*-
"""
模块: core.constraint

功能: 提供约束项基础定义类
"""
import math
import operator
import logging

from kaiwu_community.core._get_val import get_val
from kaiwu_community.core._error import KaiwuError

logger = logging.getLogger(__name__)


# Mapping from string to actual operator function
ops = {
    '==': operator.eq,
    '!=': operator.ne,
    '>': operator.gt,
    '>=': operator.ge,
    '<': operator.lt,
    '<=': operator.le,
}


class ConstraintDefinition:
    """约束定义

    Args:
        expr_left (Expression): 约束项左算子

        relation (string): 关系运算符

        expected_value(float): 约束项右算子， 缺省为0
    """

    def __init__(self, expr_left, relation, expected_value=0):
        self.left_operand = expr_left
        self.relation = relation
        self.expected_value = expected_value
        self.default_penalty = None

        # 是否需要二次方
        self.should_prepare = True

    def __str__(self):
        return f"{self.left_operand}{self.relation}{self.expected_value},"

    def __repr__(self) -> str:
        return self.__str__()

    def is_satisfied(self, solution_dict):
        """验证约束满足情况"""
        left = float(get_val(self.left_operand, solution_dict))
        right = float(self.expected_value)
        if self.relation != '==':
            return ops[self.relation](left, right)

        return abs(left - right) < 1e-5




def get_min_penalty_from_deltas(cons,
                                neg_delta, pos_delta, obj_vars, min_delta_method='diff'):
    """返回约束项cons对应的最小惩罚系数，惩罚项优先满足

    Args：
        cons：约束项的qubo表达式

        neg_delta: 各个变量1变为0时最大变化量的dict

        pos_delta: 各个变量0变为1时最大变化量的dict

        obj_vars: 第三个元素为变量列表

        min_delta_method: 声明在。分别用两种方法寻找最小变化值
                        MIN_DELTA_METHODS = {"diff": _get_constraint_min_deltas_diff,
                                     "exhaust": _get_constraint_min_deltas_exhaust}

    Examples:
        >>> import kaiwu_community as kw
        >>> x = [kw.core.Binary("b"+str(i)) for i in range(3)]
        >>> cons = kw.core.quicksum(x) - 1
        >>> obj = x[1]+2*x[2]
        >>> kw.core.get_min_penalty(obj, cons)
        2.0
    """
    constraint_var_quadratic = {}
    constraint_var_linear = {}
    for var_tuple, value in cons.coefficient.items():
        if len(var_tuple) == 2:
            for var_x in var_tuple:
                if var_x not in obj_vars:
                    continue
                if var_x not in constraint_var_quadratic:
                    constraint_var_quadratic[var_x] = [value]
                else:
                    constraint_var_quadratic[var_x].append(value)
        else:  # len == 1
            if var_tuple[0] in obj_vars:
                constraint_var_linear[var_tuple[0]] = value
    if min_delta_method not in MIN_DELTA_METHODS:
        raise KaiwuError("No such method for getting min delta")
    min_delta = MIN_DELTA_METHODS[min_delta_method](constraint_var_quadratic, constraint_var_linear)

    penalty = 0  # 惩罚系数，初始化
    for var_x, min_delta_x in min_delta.items():
        if var_x in pos_delta and min_delta_x != 0:
            penalty = max(pos_delta[var_x] / min_delta_x,
                          neg_delta[var_x] / min_delta_x, penalty)
    return penalty


def get_min_penalty_from_min_diff(cons, negative_delta, positive_delta):
    """ 根据objective的最大值，最小值估算约束项的最小惩罚系数

    Args:
        cons:  约束项

        negative_delta: objective最小值

        positive_delta: objective最大值

    Returns:
        找到的最小惩罚系数
    """
    # 如果正反向变化都没有，penalty置为1
    if not negative_delta or not positive_delta:
        return 1

    values = list(cons.coefficient.values())
    for i in range(len(cons.coefficient)):
        values.append(-values[i])
    values.append(0)
    values.sort()
    min_diff = math.inf
    for i in range(len(values) - 1):
        if values[i + 1] - values[i] > 0:
            min_diff = min(min_diff, values[i + 1] - values[i])
    penalty = 0  # 惩罚系数，初始化
    for max_delta_x in negative_delta.values():
        penalty = max(max_delta_x / min_diff, penalty)
    for max_delta_x in positive_delta.values():
        penalty = max(max_delta_x / min_diff, penalty)
    return penalty


def get_min_penalty_for_equal_constraint(obj, cons):
    """返回一次等式约束项cons对应的最小惩罚系数：把满足这个约束的解的某一位比特翻转一下的最坏情况。
    这个惩罚系数有效是指能够保证原问题的可行解是目标函数的局部最优（在一位比特翻转的局部意义下）。

    Args：
        obj: 原目标函数的qubo表达式。

        cons：线性的等式约束cons=0中的线性表达式。

    Returns:
        float: 一次等式约束项cons对应的最小惩罚系数.

    Examples：
        >>> import kaiwu_community as kw
        >>> x = [kw.core.Binary("b"+str(i)) for i in range(3)]
        >>> cons = kw.core.quicksum(x)-1
        >>> obj = x[1]+2*x[2]
        >>> kw.core.get_min_penalty_for_equal_constraint(obj,cons)
        2.0
    """
    # constraint_tuples为一次等式约束项cons所包含的所有变量及其相应的系数
    constraint_tuples = [(key[0], cons.coefficient[key]) for key in cons.coefficient]
    penalty = 0  # 惩罚系数，初始化
    neg_delta, pos_delta = obj.get_max_deltas()
    for vari, coef in constraint_tuples:
        if vari in neg_delta:
            penalty = max(pos_delta[vari] / pow(coef, 2), neg_delta[vari] / pow(coef, 2), penalty)
    return penalty


def _get_constraint_min_deltas_diff(constraint_var_quadratic, constraint_var_linear):
    """
    估计每个变量反转后在约束中引起的最小变化量
    准确求解需要枚举2^n种变量取值，用只有0、1、2个变量取1的情况来估计该值。
    """
    min_delta_dict = {}
    for var_x, value_list in constraint_var_quadratic.items():
        sorted_list = sorted(value_list)  # 对var_x相关的二次项进行排序
        if var_x in constraint_var_linear:
            # 有一次项，则翻转必然有影响，设为初值
            linear_coe = constraint_var_linear[var_x]
            min_delta = abs(linear_coe)
        else:
            # 没有一次项，初值为0
            linear_coe = 0
            min_delta = abs(sorted_list[-1])

        # 求出只考虑一个二次项时的最小变化量
        for i, val in enumerate(sorted_list):
            if linear_coe + val != 0:
                min_delta = min(min_delta, abs(linear_coe + val))
        i = 0
        j = len(sorted_list) - 1
        # 求出只考虑两个二次项时的最小变化量
        while i < j:
            new_delta = sorted_list[i] + sorted_list[j] + linear_coe
            if new_delta != 0:
                min_delta = min(min_delta, abs(new_delta))
            if -sorted_list[i] > sorted_list[j]:
                i += 1
            else:
                j -= 1
        min_delta_dict[var_x] = min_delta

    for var_x, value in constraint_var_linear.items():
        if var_x not in min_delta_dict:
            min_delta_dict[var_x] = value
    return min_delta_dict


def _get_constraint_min_deltas_exhaust(constraint_var_quadratic, constraint_var_linear):
    """
    计算每个变量反转后在约束中引起的最小变化量
    """
    min_delta_dict = {}
    for var_x, value_list in constraint_var_quadratic.items():
        if var_x in constraint_var_linear:
            # 有一次项，则翻转必然有影响，设为初值
            value_set = {constraint_var_linear[var_x]}
            min_delta = abs(constraint_var_linear[var_x])
        else:
            # 没有一次项，初值为0
            value_set = {0}
            min_delta = math.inf
        for coe in value_list:
            copy_set = value_set.copy()
            for sum_value in copy_set:
                value_set.add(sum_value + coe)
                if abs(sum_value + coe) < min_delta and sum_value + coe != 0:
                    min_delta = abs(sum_value + coe)
        min_delta_dict[var_x] = min_delta

    for var_x, value in constraint_var_linear.items():
        if var_x not in min_delta_dict:
            min_delta_dict[var_x] = value
    return min_delta_dict


MIN_DELTA_METHODS = {"diff": _get_constraint_min_deltas_diff,
                     "exhaust": _get_constraint_min_deltas_exhaust}


def get_soft_penalty(obj, cons):
    """返回soft约束项cons对应的惩罚系数，使其约束项和目标函数的系数平均数相同

    Args:
        obj (QuboExpression): 原目标函数的qubo表达式。

        cons (QuboExpression): 约束项的qubo表达式

    Returns:
        float: 返回约束项cons对应的惩罚系数.
    """
    avg_obj_coe = obj.get_average_coefficient()
    avg_cons_coe = cons.get_average_coefficient()
    return avg_obj_coe / avg_cons_coe


def get_min_penalty(obj, cons):
    """返回约束项cons对应的最小惩罚系数，惩罚项优先满足

    Args:
        obj: 原目标函数的qubo表达式。

        cons：约束项的qubo表达式

    Returns:
        float: 返回约束项cons对应的最小惩罚系数.

    Examples：
        >>> import kaiwu_community as kw
        >>> x = [kw.core.Binary("b"+str(i)) for i in range(3)]
        >>> cons = kw.core.quicksum(x) - 1
        >>> obj = x[1] + 2 * x[2]
        >>> kw.core.get_min_penalty(obj, cons)
        2.0
    """
    negative_delta, positive_delta = obj.get_max_deltas()
    return get_min_penalty_from_min_diff(cons, negative_delta, positive_delta)

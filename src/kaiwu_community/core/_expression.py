# -*- coding: utf-8 -*-
"""
模块: qubo

功能: QUBO及Ising表达式运算类
"""
import copy
import numbers
from kaiwu_community.core._error import KaiwuError
from kaiwu_community.core._constraint import ConstraintDefinition

QUBO_MAINTAINED_KEY = ["hard_constraint", "soft_constraint", "hobo_var_dict", "hobo_constraint"]


def is_zero(qubo_expr):
    """QUBO表达式为0"""
    if isinstance(qubo_expr, numbers.Number):
        return qubo_expr == 0
    return len(qubo_expr.coefficient) == 0 and qubo_expr.offset == 0


def update_constraint(qubo_origin, qubo_result):
    """将qexp的约束以及降阶约束信息更新到q"""
    for key in QUBO_MAINTAINED_KEY:
        if key in qubo_origin:
            if key in qubo_result:
                qubo_result[key].update(qubo_origin[key])
            else:
                qubo_result[key] = qubo_origin[key]


def expr_add(expr_left, expr_right, expr_result):
    """通用二次表达式相加"""
    if isinstance(expr_right, numbers.Number):
        expr_result.coefficient = expr_left.coefficient.copy()
        expr_result.offset = expr_left.offset + expr_right
        update_constraint(expr_left, expr_result)
    else:
        expr_result.offset = expr_left.offset + expr_right.offset
        if len(expr_right.coefficient) < len(expr_left.coefficient):
            expr_result.coefficient = expr_left.coefficient.copy()
            expr_other = expr_right
        else:
            expr_result.coefficient = expr_right.coefficient.copy()
            expr_other = expr_left

        for key in expr_other.coefficient:
            if key in expr_result.coefficient:
                expr_result.coefficient[key] += expr_other.coefficient[key]
                if expr_result.coefficient[key] == 0:
                    expr_result.coefficient.pop(key)
            else:
                expr_result.coefficient[key] = expr_other.coefficient[key]


def expr_neg(expr_origin, expr_result):
    """通用二次表达式取负"""
    for key in expr_origin.coefficient:
        expr_result.coefficient[key] = -expr_origin.coefficient[key]
    expr_result.offset = -expr_origin.offset
    update_constraint(expr_origin, expr_result)


def _expr_dicts_mul(expr_left, expr_right, expr_result):
    for lkey in expr_left.coefficient:
        for rkey in expr_right.coefficient:
            key = list(set(lkey + rkey))
            key.sort()
            key = tuple(key)
            if key in expr_result.coefficient:
                expr_result.coefficient[key] += expr_left.coefficient[lkey] * \
                                                expr_right.coefficient[rkey]
                if expr_result.coefficient[key] == 0:
                    expr_result.coefficient.pop(key)
            else:
                expr_result.coefficient[key] = expr_left.coefficient[lkey] * \
                                               expr_right.coefficient[rkey]
        if not is_zero(expr_right.offset):
            if lkey in expr_result.coefficient:
                expr_result.coefficient[lkey] += expr_left.coefficient[lkey] * \
                                                 expr_right.offset
            else:
                expr_result.coefficient[lkey] = expr_left.coefficient[lkey] * \
                                                expr_right.offset
    if not is_zero(expr_left.offset):
        for rkey in expr_right.coefficient:
            if rkey in expr_result.coefficient:
                expr_result.coefficient[rkey] += expr_right.coefficient[rkey] * \
                                                 expr_left.offset
            else:
                expr_result.coefficient[rkey] = expr_right.coefficient[rkey] * \
                                                expr_left.offset
        expr_result.offset += expr_left.offset * expr_right.offset


def expr_mul(expr_left, expr_right, expr_result):
    """通用二次表达式相乘"""
    if isinstance(expr_right, numbers.Number):
        if not is_zero(expr_right):
            for lkey in expr_left.coefficient:
                expr_result.coefficient[lkey] = expr_left.coefficient[lkey] * expr_right
            expr_result.offset = expr_left.offset * expr_right
        update_constraint(expr_left, expr_result)
    else:
        _expr_dicts_mul(expr_left, expr_right, expr_result)


def expr_pow(expr_left, expr_right, expr_result):
    """通用二次表达式乘方，要求expr_right只能为1或者2"""
    if expr_right == 1:
        expr_result.offset = expr_left.offset
        expr_result.coefficient = expr_left.coefficient.copy()
    elif expr_right == 2:
        expr_mul(expr_left, expr_left, expr_result)
    else:
        if len(expr_left.coefficient) == 1 and \
                (list(expr_left.coefficient.keys())[0][0][0] == "b"):
            expr_result.offset = expr_left.offset
            expr_result.coefficient = expr_left.coefficient.copy()
        else:
            raise KaiwuError("Items higher than quadratic.")
    update_constraint(expr_left, expr_result)


def _check_unit(checked_str):
    if len(checked_str) > 2:
        if checked_str[:2] == "1*":
            checked_str = checked_str[2:]
        elif checked_str[:3] == "-1*":
            checked_str = "-" + checked_str[3:]
    return checked_str


class Expression(dict):
    """QUBO/Ising 通用表达式基类（提供默认二次表达式实现）"""

    def __init__(self, coefficient: dict = None, offset: float = 0):
        super().__init__()
        if coefficient is None:
            self.coefficient = {}
        else:
            self.coefficient = coefficient

        self.offset = offset

    def clear(self) -> None:
        """初始化所有属性"""
        self.coefficient = {}
        self.offset = 0

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        expression_str = ""
        for p_key in self.coefficient:
            p_str = ""
            for p_var in p_key:
                p_str += "*" + p_var[1:]
            coe = self.coefficient[p_key]
            if not isinstance(coe, numbers.Number) and len(coe.coefficient) > 0:
                coe_str = "(" + str(coe) + ")"
            else:
                coe_str = str(coe)
            p_str = _check_unit(coe_str + p_str)

            if p_str[0] == "-":
                expression_str += p_str
            else:
                if expression_str == "":
                    expression_str += p_str
                else:
                    expression_str += "+" + p_str

        if not (is_zero(self.offset) and expression_str != ""):
            offset_str = str(self.offset)
            if offset_str[0] == "-":
                expression_str += offset_str
            else:
                if expression_str == "":
                    expression_str += offset_str
                else:
                    expression_str += "+" + offset_str
        return _check_unit(expression_str)

    def __radd__(self, other):
        return self.__add__(other)

    def __add__(self, other):
        q_ret = copy.copy(self)
        q_ret.clear()

        expr_add(self, other, q_ret)
        return q_ret

    def __rsub__(self, other):
        return (-self).__add__(other)

    def __sub__(self, other):
        return self.__add__(-other)

    def __rmul__(self, other):
        return self.__mul__(other)

    def __mul__(self, other):
        q_ret = copy.copy(self)
        q_ret.clear()

        expr_mul(self, other, q_ret)
        return q_ret

    def __truediv__(self, other):
        return self.__mul__(1 / other)

    def __pow__(self, other):
        q_ret = copy.copy(self)
        q_ret.clear()

        expr_pow(self, other, q_ret)
        return q_ret

    def __neg__(self):
        q_ret = copy.copy(self)
        q_ret.clear()

        expr_neg(self, q_ret)
        return q_ret

    def __eq__(self, other):
        return ConstraintDefinition(self - other, '==')

    def __ge__(self, other):
        return ConstraintDefinition(self - other, '>=')

    def __le__(self, other):
        return ConstraintDefinition(self - other, '<=')

    def __gt__(self, other):
        return ConstraintDefinition(self - other, '>')

    def __lt__(self, other):
        return ConstraintDefinition(self - other, '<')

    def get_variables(self):
        """获取变量名集合

            Returns:
                variables: (tuple) 返回构成expression的变量集合

        """
        variables = set()  # 放目标函数obj所包含的所有变量
        for key in self.coefficient:
            variables.add(key[0])
            if len(key) == 2:
                variables.add(key[1])

        return tuple(sorted(list(variables)))

    def get_max_deltas(self):
        """求出每个变量翻转引起目标函数变化的上界
        返回值negative_delta，positive_delta分别为该变量1->0和0->1所引起的最大变化量
        """
        obj_variables = self.get_variables()
        positive_delta = {var_x: 0 for var_x in obj_variables}
        negative_delta = {var_x: 0 for var_x in obj_variables}
        for var_tuple in self.coefficient.keys():
            for var_x in var_tuple:
                # 二次项受另一个变量影响，另一个变量为0时系数不引起变化
                if len(var_tuple) == 2:
                    positive_delta[var_x] += max(self.coefficient[var_tuple], 0)
                    # 变量0->1引起的变化量为-coefficient
                    negative_delta[var_x] += max(-self.coefficient[var_tuple], 0)

                # 一次项不受另一个变量影响，变量翻转一定引起变化
                elif len(var_tuple) == 1:
                    positive_delta[var_x] += self.coefficient[var_tuple]
                    # 变量0->1引起的变化为-coefficient,与二次项的情况一致
                    negative_delta[var_x] -= self.coefficient[var_tuple]
        return negative_delta, positive_delta

    def get_average_coefficient(self):
        """ 返回coefficient的平均值"""
        coe_sum = 0
        num_item = 0
        for _, coe in self.coefficient.items():
            coe_sum += abs(coe)
            num_item += 1
        return coe_sum / num_item

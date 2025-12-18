"""
BinaryExpression
Binary变量构成的表达式
"""

import copy
import math
import numbers
import numpy as np

from kaiwu_community.core._expression import update_constraint
from kaiwu_community.core._expression import Expression, expr_add, expr_neg, expr_mul, expr_pow
from kaiwu_community.core._error import KaiwuError


class BinaryExpression(Expression):
    """QUBO表达式的基础数据结构"""

    def __init__(self, coefficient: dict = None, offset: float = 0, name=""):
        super().__init__(coefficient, offset)
        self.name = name

    def feed(self, feed_dict):
        """为占位符号赋值, 并返回赋值后的新表达式对象

        Args:
            feed_dict(dict): 需要赋值的占位符的值

        Examples:
            >>> import kaiwu_community as kw
            >>> p = kw.core.Placeholder('p')
            >>> a = kw.core.Binary('a')
            >>> y = p * a
            >>> str(y)  # doctest: +NORMALIZE_WHITESPACE
            '(p)*a'
            >>> y= y.feed({'p': 2})
            >>> str(y)  # doctest: +NORMALIZE_WHITESPACE
            '2*a'
        """
        ret = copy.deepcopy(self)
        for expr_vars in ret.coefficient:
            if not isinstance(ret.coefficient[expr_vars], numbers.Number):
                ret.coefficient[expr_vars] = ret.coefficient[expr_vars].feed(feed_dict)
        if not isinstance(ret.offset, numbers.Number):
            ret.offset = ret.offset.feed(feed_dict)
        return ret

    def __repr__(self):
        return self.__str__()

    def __radd__(self, other):
        return self.__add__(other)

    def __add__(self, other):
        if isinstance(other, np.ndarray):
            return other.__add__(self)
        if other is None:
            ret = copy.deepcopy(self)
            return ret
        result = BinaryExpression()
        expr_add(self, other, result)
        return result

    def __rsub__(self, other):
        return (-self).__add__(other)

    def __sub__(self, other):
        result = self.__add__(-other)
        return result

    def __neg__(self):
        result = BinaryExpression()
        expr_neg(self, result)
        return result

    def __rmul__(self, other):
        return self.__mul__(other)

    def __mul__(self, other):
        if other is None:
            return copy.deepcopy(self)
        result = BinaryExpression()
        expr_mul(self, other, result)
        return result

    def __pow__(self, other):
        result = BinaryExpression()
        expr_pow(self, other, result)
        return result


class Binary(BinaryExpression):
    """二进制变量, 只保存变量名，不继承 QuboExpression"""

    def __init__(self, name: str = ""):
        super().__init__({("b" + name,): 1}, 0, name="b" + name)

    def clear(self):
        """初始化所有属性"""
        self.name = ""
        self.coefficient = {}
        self.offset = 0


class Integer(BinaryExpression):
    """整数变量, 只保存变量名和范围，不继承 QuboExpression"""

    def __init__(self, name: str = "", min_value=0, max_value=127):
        super().__init__()
        self.offset = min_value
        if max_value <= min_value:
            raise KaiwuError("max_value must be larger than min_value")
        num_bits = int(math.log2(max_value - min_value))
        self.coefficient = {}
        for j in range(num_bits):
            self.coefficient[(f"b{name}[{j}]",)] = 2 ** j
        self.coefficient[(f"b{name}[{num_bits}]",)] = max_value - min_value - 2 ** (num_bits) + 1


class Placeholder(BinaryExpression):
    """占位符变量, 只保存变量名, 对决策"""

    def __init__(self, name: str = ""):
        super().__init__()
        self.name = "p" + name
        name = "p" + name
        self.coefficient = {}
        self.offset = _Placeholder({tuple({name}): 1}, 0)

    def get_placeholder_set(self):
        """获取占位符集合"""
        placeholder_set = set()
        for var_tuple in self.coefficient:
            for var in var_tuple:
                placeholder_set.add(var)
        return placeholder_set


class _Placeholder(Expression):
    """占位符的底层实现，实际在QuboExpression的dict结构的参数位置"""

    def feed(self, feed_dict):
        """为占位符赋值"""
        placeholder_value = 0
        for placeholder_vars in self.coefficient:
            p_value = self.coefficient[placeholder_vars]
            for p_var in placeholder_vars:
                p_value *= feed_dict[p_var[1:]]
            placeholder_value += p_value
        placeholder_value += self.offset
        return placeholder_value


def quicksum(qubo_expr_list: list):
    """高性能的QUBO求和器.

    Args:
        qubo_expr_list (QUBO列表): 用于求和的QUBO表达式的列表.

    Returns:
        BinaryExpression: 约束QUBO.

    Examples:
        >>> import kaiwu_community as kw
        >>> qubo_list = [kw.core.Binary("b"+str(i)) for i in range(10)] # Variables are also QUBO
        >>> output = kw.core.quicksum(qubo_list)
        >>> str(output)
        'b0+b1+b2+b3+b4+b5+b6+b7+b8+b9'
    """
    qsum = BinaryExpression()
    for single_q in qubo_expr_list:
        if isinstance(single_q, numbers.Number):
            qsum.offset += single_q
            continue
        if not isinstance(single_q, dict):
            raise KaiwuError("qubo_expr_list should be a list of QUBO Expression")

        update_constraint(single_q, qsum)

        qsum.offset += single_q.offset
        for ele in single_q.coefficient.keys():
            if ele in qsum.coefficient:
                qsum.coefficient[ele] += single_q.coefficient[ele]
            else:
                qsum.coefficient[ele] = single_q.coefficient[ele]
            if qsum.coefficient[ele] == 0:
                qsum.coefficient.pop(ele)
    return qsum


if __name__ == '__main__':
    import doctest
    doctest.testmod()

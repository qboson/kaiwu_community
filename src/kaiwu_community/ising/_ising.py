# -*- coding: utf-8 -*-
"""
模块: cim

功能: ising模型及其转化
"""
from kaiwu_community.core import Expression


def _dict_variables(var_dict):
    var_list = [0] * len(var_dict)
    for var in var_dict:
        var_list[var_dict[var]] = var[1:]
    return str(tuple(var_list)).replace("\'", "")[1:-1]


class IsingModel(dict):
    """ising模型"""

    def __init__(self, variables, ising_matrix, bias):
        super().__init__()
        self.variables = variables
        self.matrix = ising_matrix
        self.bias = bias

    def __repr__(self):
        return f"{self.__class__.__name__}({vars(self)!r})"

    def __str__(self):
        """返回ising模型的细节信息.

        Returns:
            序列化后的模型(字符串形式）
        """
        print_data = ""
        print_data += "CIM Ising Details:\n"
        print_data += "  CIM Ising Matrix:\n"
        print_data += "    " + str(self.matrix).replace("\n", "\n    ") + "\n"
        print_data += "  CIM Ising Bias: " + str(self.bias) + "\n"
        print_data += "  CIM Ising Variables" + ": " + \
                      _dict_variables(self.variables) + "\n"

        return print_data

    def get_variables(self):
        """获取模型中的变量"""
        return dict(zip((key[1:] for key in self.variables), self.variables.values()))

    def get_matrix(self):
        """获取Ising矩阵"""
        return self.matrix

    def get_bias(self):
        """获取QUBO转化时得到的常数偏置"""
        return self.bias


class IsingExpression(Expression):
    """Ising 表达式基类，直接继承 Expression，保留扩展点。"""

    def __init__(self, variables=None, quadratic=None, linear=None, bias=0):
        if quadratic is None:
            quadratic = {}
        if linear is None:
            linear = {}
        super().__init__({**quadratic, **linear}, bias)
        self.variables = variables
        self.quadratics = quadratic
        self.linear = linear
        self.bias = bias


class Spin(IsingExpression):
    """自旋变量, 可能的取值只有-1,1.

    Args:
        name (str): 变量的唯一标识.

    Returns:
        dict: 名称为name的自旋变量.

    Examples:
        >>> import kaiwu_community as kw
        >>> s = kw.ising.Spin("s")
        >>> s
        2*s-1
    """

    def __init__(self, name: str = ""):
        name = "s" + name
        super().__init__(linear={tuple({name}): 2}, bias=-1)
        self.name = name


if __name__ == '__main__':
    import doctest

    doctest.testmod()

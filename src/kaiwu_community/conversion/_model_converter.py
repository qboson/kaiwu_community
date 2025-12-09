# -*- coding: utf-8 -*-
"""
模块: qubo

功能: QUBO模型和Ising模型转换
"""
import numpy as np
from kaiwu_community.ising import IsingModel, IsingExpression



def _to_ising(qubo_expr):
    """QUBO表达式转化为Ising模型"""
    variables_set = set()
    quadratic = {}
    linear = {}
    bias = 0
    for key in qubo_expr.coefficient:
        variables_set.add(key[0])
        if len(key) == 2:
            variables_set.add(key[1])
            coefficient = qubo_expr.coefficient[key] / 4
            quadratic[key] = coefficient
            if key[0] in linear:
                linear[key[0]] += coefficient
            else:
                linear[key[0]] = coefficient
            if key[1] in linear:
                linear[key[1]] += coefficient
            else:
                linear[key[1]] = coefficient
            bias += coefficient
        else:
            coefficient = qubo_expr.coefficient[key] / 2
            if key[0] in linear:
                linear[key[0]] += coefficient
            else:
                linear[key[0]] = coefficient
            bias += coefficient
    bias += qubo_expr.offset

    variables_set = list(variables_set)
    variables_set.sort()
    variables_set = tuple(variables_set)

    return IsingExpression(variables_set, quadratic, linear, bias)


def qubo_model_to_ising_model(qubo_model):
    """QUBO转CIM Ising模型.

    Args:
        qubo_model (QuboModel): QUBO Model.

    Returns:
        CimIsing: CIM Ising模型.

    Examples:
        >>> import kaiwu_community as kw
        >>> b1, b2 = kw.core.Binary("b1"), kw.core.Binary("b2")
        >>> q = b1 + b2 + b1*b2
        >>> q_model = kw.qubo.QuboModel(q)
        >>> ci = kw.conversion.qubo_model_to_ising_model(q_model)
        >>> print(str(ci))
        CIM Ising Details:
          CIM Ising Matrix:
            [[-0.    -0.125 -0.375]
             [-0.125 -0.    -0.375]
             [-0.375 -0.375 -0.   ]]
          CIM Ising Bias: 1.25
          CIM Ising Variables: b1, b2, __spin__
        <BLANKLINE>
    """
    qubo_model.compile_constraints()
    qubo_expr = qubo_model.make()
    ising_expression = _to_ising(qubo_expr)
    variable_index = dict(zip(ising_expression.variables, range(len(ising_expression.variables))))
    variable_index["a__spin__"] = len(ising_expression.variables)
    cim_matrix = np.zeros((len(ising_expression.variables) + 1, len(ising_expression.variables) + 1))
    for key in ising_expression.quadratics:
        cim_matrix[variable_index[key[0]], variable_index[key[1]]] = ising_expression.quadratics[key]

    for key in ising_expression.linear:
        cim_matrix[variable_index[key], len(ising_expression.variables)] = ising_expression.linear[key]

    cim_matrix = cim_matrix + cim_matrix.T

    return IsingModel(variable_index, -0.5 * cim_matrix, ising_expression.bias)


if __name__ == '__main__':
    import doctest
    doctest.testmod()

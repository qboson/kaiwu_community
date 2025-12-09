# -*- coding: utf-8 -*-
"""
模块: qubo

功能: 提供QUBO相关类的字符串转化
"""
import numbers
import logging
from kaiwu_community.qubo._error import QuboError

logger = logging.getLogger(__name__)


def _qubo_check(variables_tuple, quadratic):
    if not variables_tuple:
        return
    var_type = variables_tuple[0][0]
    for var in variables_tuple:
        if var[0] != var_type:
            raise QuboError("Conflicting variable types, the QUBO expression contains "
                            "both \"binary\" and \"spin\".")
    for key in quadratic:
        if len(key) > 2:
            raise QuboError("Items higher than quadratic.")


def _get_placeholder(expr):
    placeholders_set = set()
    for value in expr.coefficient.values():
        if not isinstance(value, numbers.Number):
            for placeholder_tuple in value.coefficient:
                for var_p in placeholder_tuple:
                    placeholders_set.add(var_p)
    return tuple(sorted(list(placeholders_set)))


def _qubo_sketch(qubo_expr, q_check=True):
    variables_set = qubo_expr.get_variables()
    placeholders_set = _get_placeholder(qubo_expr)
    var_type = "unknown"
    if len(variables_set) == 0:
        logger.warning("Empty QUBO, the objective function is constant 0 (QUBO = 0).")
    else:
        var_type = variables_set[0][0]
        if q_check:
            _qubo_check(variables_set, qubo_expr.coefficient)
    return {"variable": variables_set, "placeholder": placeholders_set, "vtype": var_type}


def _expression_repr(expr):
    var_tuple_len = 0
    quadratic = {}
    print_data = ""
    for var_tuple, value in expr.coefficient.items():
        var_tuple_str = str(var_tuple)[1:-1]
        var_tuple_str = var_tuple_str.replace('\'b', '').replace('\'s', '').replace('\'', '')
        var_tuple_len = max(var_tuple_len, len(var_tuple_str))
        quadratic[var_tuple_str] = str(value)
    offset_str = str(expr.offset)

    sketch_dict = _qubo_sketch(expr)
    variables = sketch_dict["variable"]
    variables_str = ", ".join([var_x[1:] for var_x in variables])
    if sketch_dict["vtype"] == "s":
        var_type = "Spin):  "
    else:
        var_type = "Binary):"

    print_data += "  Variables(" + var_type
    print_data += variables_str + "\n"

    placeholders = sketch_dict["placeholder"]
    placeholders_str = ", ".join([var_x[1:] for var_x in placeholders])
    if placeholders_str != "":
        print_data += "  Placeholders:" + " "
        print_data += "    " + placeholders_str + "\n"

    print_data += "  QUBO offset:" + " "
    print_data += "     " + offset_str + "\n"

    print_data += "  QUBO coefficients:" + "\n"
    for key, value in quadratic.items():
        print_data += "    " + key.ljust(var_tuple_len + 1) + ": " + value + "\n"
    return print_data


def _qubo_details(expr):
    output_str = "QUBO Details:\n"
    output_str += _expression_repr(expr)
    return output_str

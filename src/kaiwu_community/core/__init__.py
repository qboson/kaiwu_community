# -*- coding: utf-8 -*-
"""
模块: core

功能: 基础类的定义

"""

from kaiwu_community.core._optimizer_base import OptimizerBase
from kaiwu_community.core._solver_base import SolverBase
from kaiwu_community.core._error import KaiwuError

from kaiwu_community.core._constraint import (ConstraintDefinition, get_min_penalty, get_min_penalty_from_min_diff,
                                              get_min_penalty_for_equal_constraint, get_min_penalty_from_deltas)
from kaiwu_community.core._penalty_method_constraint import PenaltyMethodConstraint
from kaiwu_community.core._get_val import get_sol_dict, get_array_val, get_val
from kaiwu_community.core._expression import update_constraint, Expression, expr_add, expr_mul, expr_neg, expr_pow
from kaiwu_community.core._binary_model import BinaryModel
from kaiwu_community.core._binary_expression import (BinaryExpression, Binary, quicksum, Placeholder, Integer)
from kaiwu_community.core._matrix import ndarray, dot, BinaryExpressionNDArray

__all__ = [
    "OptimizerBase",
    "SolverBase",
    "KaiwuError",
    "ConstraintDefinition","get_min_penalty","get_min_penalty_from_min_diff",
    "get_min_penalty_for_equal_constraint","get_min_penalty_from_deltas",
    "PenaltyMethodConstraint",
    "get_sol_dict",
    "get_array_val",
    "get_val",
    "update_constraint","Expression","expr_add","expr_mul","expr_neg","expr_pow",
    "BinaryModel",
    "BinaryExpression", "Binary", "quicksum", "Placeholder", "Integer",
    "ndarray", "dot", "BinaryExpressionNDArray"
]

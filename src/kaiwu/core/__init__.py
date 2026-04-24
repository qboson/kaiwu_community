# -*- coding: utf-8 -*-
"""
模块: core

功能: 基础类的定义

"""

from kaiwu.core._base_solver import IsingSolver, QuboSolver, get_sorted_solutions
from kaiwu.core._error import KaiwuError

from kaiwu.core._constraint import (
    get_min_penalty,
    get_min_penalty_from_min_diff,
    get_min_penalty_for_equal_constraint,
    get_min_penalty_from_deltas,
)
from kaiwu.core._penalty_method_constraint import PenaltyMethodConstraint
from kaiwu.core._get_val import get_sol_dict, get_val
from kaiwu.core._expression import Expression

from kaiwu.core._binary_model import BinaryModel
from kaiwu.core._binary_expression import (
    BinaryExpression,
    Binary,
    quicksum,
    Placeholder,
    Integer,
)
from kaiwu.core._matrix import ndarray, zeros, dot, BinaryExpressionNDArray
from kaiwu.core._ising import IsingModel, Spin, IsingExpression
from kaiwu.core._qubo_model import (
    QuboModel,
    calculate_qubo_value,
    qubo_matrix_to_qubo_model,
)
from kaiwu.core._matrix_converter import (
    ising_matrix_to_qubo_matrix,
    qubo_matrix_to_ising_matrix,
)
from kaiwu.core._model_converter import qubo_model_to_ising_model


__all__ = [
    "IsingSolver",
    "QuboSolver",
    "get_sorted_solutions",
    "KaiwuError",
    "get_min_penalty",
    "get_min_penalty_from_min_diff",
    "get_min_penalty_for_equal_constraint",
    "get_min_penalty_from_deltas",
    "PenaltyMethodConstraint",
    "get_sol_dict",
    "get_val",
    "Expression",
    "BinaryModel",
    "BinaryExpression",
    "Binary",
    "quicksum",
    "Placeholder",
    "Integer",
    "ndarray",
    "zeros",
    "dot",
    "BinaryExpressionNDArray",
    "IsingModel",
    "IsingExpression",
    "Spin",
    "QuboModel",
    "calculate_qubo_value",
    "qubo_matrix_to_qubo_model",
    "ising_matrix_to_qubo_matrix",
    "qubo_matrix_to_ising_matrix",
    "qubo_model_to_ising_model",
]

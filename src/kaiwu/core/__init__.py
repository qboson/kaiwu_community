# -*- coding: utf-8 -*-
"""
模块: core

功能: 基础类的定义

"""

from ._base_solver import IsingSolver, QuboSolver
from ._error import KaiwuError

from ._constraint import (
    get_min_penalty,
    get_min_penalty_from_min_diff,
    get_min_penalty_for_equal_constraint,
    get_min_penalty_from_deltas,
)
from ._penalty_method_constraint import PenaltyMethodConstraint
from ._get_val import get_sol_dict, get_val
from ._expression import Expression

from ._binary_model import BinaryModel
from ._binary_expression import (
    BinaryExpression,
    Binary,
    quicksum,
    Placeholder,
    Integer,
)
from ._matrix import ndarray, zeros, dot, BinaryExpressionNDArray
from ._ising import IsingModel, Spin, IsingExpression
from ._qubo_model import (
    QuboModel,
    calculate_qubo_value,
    qubo_matrix_to_qubo_model,
)
from ._matrix_converter import (
    ising_matrix_to_qubo_matrix,
    qubo_matrix_to_ising_matrix,
)
from ._model_converter import qubo_model_to_ising_model


__all__ = [
    "IsingSolver",
    "QuboSolver",
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

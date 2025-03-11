# -*- coding: utf-8 -*-
"""
模块: qubo

功能: QUBO建模工具
"""


from kaiwu.qubo._precision import check_qubo_matrix_bit_width, adjust_qubo_matrix_precision
from kaiwu.qubo._qubo_model import QuboModel, calculate_qubo_value, qubo_matrix_to_qubo_model
from kaiwu.qubo._error import QuboError


__all__ = [
    "check_qubo_matrix_bit_width",
    "adjust_qubo_matrix_precision",
    "QuboModel",
    "calculate_qubo_value",
    "qubo_matrix_to_qubo_model",
    "QuboError"
]

# -*- coding: utf-8 -*-
"""
模块: qubo

功能: QUBO相关的错误处理
"""
from kaiwu_community.core import KaiwuError


class QuboError(KaiwuError):
    """Exceptions in qubo module."""

    def __init__(self, error_info):
        self.error_info = error_info

    def __str__(self):
        return self.error_info

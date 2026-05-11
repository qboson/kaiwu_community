# -*- coding: utf-8 -*-
"""
kaiwu-community: 基础版 SDK
"""

import pkgutil
import importlib

# 支持跨目录加载 kaiwu 命名空间下的其他包 (如 enterprise 中的 cim, classical 等)
__path__ = pkgutil.extend_path(__path__, __name__)

__version__ = "1.0.4"

# 1. 加载 Community 自身的基础模块 (由 Enterprise 同步而来)
from .core import *
from .common import *

# 2. 显式尝试加载 Enterprise 的扩展模块
_EXT_MODULES = [
    "cim",
    "classical",
    "hobo",
    "hybrid",
    "license",
    "preprocess",
    "sampler",
]

for _mod_name in _EXT_MODULES:
    try:
        # 使用绝对导入触发命名空间查找
        _mod = importlib.import_module(f"kaiwu.{_mod_name}")
        # 关键修复：确保 kaiwu.classical 这种属性访问在 kw.classical 中生效
        globals()[_mod_name] = _mod
        # 同时将非私有成员提取到顶层命名空间 (保持扁平化访问支持)
        for _k, _v in _mod.__dict__.items():
            if not _k.startswith("_"):
                globals()[_k] = _v
    except ImportError:
        pass

# 清理临时变量
del _mod_name, _EXT_MODULES

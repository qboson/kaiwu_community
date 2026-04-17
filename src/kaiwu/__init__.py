# -*- coding: utf-8 -*-
"""
kaiwu-community: 基础版 SDK
"""

__version__ = "1.0.0"

from .core import *
from .common import *

try:
    # pylint: disable=import-self
    from . import enterprise_features
    _injected = []
    for _attr in dir(enterprise_features):
        if not _attr.startswith('_'):
            globals()[_attr] = getattr(enterprise_features, _attr)
            _injected.append(_attr)
except ImportError:
    pass
else:
    del _injected

# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

import os, sys

sys.path.insert(0, os.path.abspath("../src"))
from kaiwu_community import __version__

project = 'Kaiwu Community'
release = __version__
version = __version__
copyright = '2022 Beijing QBoson Quantum Technology Co., Ltd'
author = 'QBoson Inc'

# language 默认语言
language = 'zh_CN'

# 启用 gettext
locale_dirs = ['locale/']
gettext_compact = False

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    'sphinx.ext.autodoc',
    "sphinxcontrib.jquery",
    'sphinx.ext.mathjax',
    'myst_parser'
]

templates_path = ['_templates']
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'pydata_sphinx_theme'
html_static_path = ['_static']

# Theme options
html_theme_options = {
    # 顶部导航栏配置
    'navbar_start': ['navbar-logo'],
    'navbar_center': ['navbar-nav'],
    'navbar_end': ['theme-switcher', 'navbar-icon-links'],  # 删除搜索框
    # 始终显示所有顶部导航项
    'navbar_align': 'left',
    # 确保面包屑导航正常显示
    'show_prev_next': False,
    # 确保所有toctree项都显示
    'collapse_navigation': False,
    # 显示章节导航，不显示目录
    'show_nav_level': 2,
}

# 只显示章节导航，不显示目录
html_sidebars = {
    '**': [
        'sidebar-nav-bs',  # 只显示整个文档的结构，即章节导航
    ],
}

# 隐藏当前页面的目录
html_show_copyright = False
html_show_sphinx = False
html_show_sourcelink = False

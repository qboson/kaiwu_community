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
    'sphinx.ext.imgmath',
    'myst_parser'
]

templates_path = ['_templates']
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'pydata_sphinx_theme'
html_static_path = ['_static']
html_logo = "_static/sdk-logo.png"
html_favicon = "_static/sdk-logo.png"

html_theme_options = {
    "show_nav_level": 2,
    "logo": {
        "text": project,
        "image_dark": "",
        "image_light": ""
    },
    # 导航栏配置
    # "navbar_start": ["navbar-logo", ],    # 左侧元素
    "navbar_center": ["navbar-nav"],    # 中间导航链接
    # "navbar_end": ["theme-switcher", "navbar-icon-links"],  # 右侧元素
    "navbar_persistent": ["search-button"],  # 常驻元素（如搜索按钮）
    # "navbar_align": "left",
    # 页脚配置
    "footer_start": ["copyright"],      # 页脚开头
    "footer_end": ["theme-version"],     # 页脚结尾
    "show_toc_level": 2,               # 侧边栏目录显示层级
}

html_show_sourcelink = False
html_css_files = ['custom.css']

source_suffix = {
    '.rst': 'restructuredtext',
    '.txt': 'markdown',
    '.md': 'markdown',
}
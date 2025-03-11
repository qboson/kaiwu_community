# -*- coding: utf-8 -*-
"""
Created on Thu Mar 10 14:45:34 2022

@author: Wang
"""
from setuptools import setup, find_packages

from common.config import SDK_RELEASE_VERSION


def get_install_requires():
    requires = []
    for line in open('requirements.txt', 'r'):
        line = line.strip()
        if not line.startswith('#'):
            parts = line.split('#egg=')
            if len(parts) == 2:
                requires.append(parts[1])
            else:
                requires.append(line)
    return requires


install_requires = get_install_requires()

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="kaiwu",
    version=SDK_RELEASE_VERSION,
    author="Qboson Inc",
    description="An SDK for CIM or QUBO.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    # url="https://github.com/*",
    # project_urls={
    #     "Bug Tracker": "https://github.com/*",
    # },
    package_dir={"": "src/com/qboson"},
    packages=find_packages(where='src/com/qboson'),
    python_requires='>=3.10',
    install_requires=install_requires,
    classifiers=[
        "Programming Language :: Python :: 3",
        #    "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)

# 开发模式: python setup.py develop
# 开发模式: python setup.py develop --uninstall

# 构建.whl: python setup.py bdist_wheel
# 安装.whl: pip install *.whl

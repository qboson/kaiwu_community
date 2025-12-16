概述
====

Kaiwu SDK 社区版
-----------------

Kaiwu SDK 社区版是一套开源的软件开发套件，专为QUBO（二次无约束二进制优化）问题求解而设计。该套件致力于为开发者提供一个便捷的Python环境，以构建QUBO模型并使用内置或自定义的求解器进行高效求解。

Kaiwu SDK 社区版包含以下核心模块：

* **qubo**: 提供QUBO模型的构建和管理功能
* **ising**: 支持Ising模型的表示和转换
* **classical**: 包含经典优化算法，如BruteForceOptimizer
* **solver**: 提供求解器框架，支持调用不同的优化器
* **core**: 提供核心数据结构和数学运算支持
* **common**: 提供通用工具和配置管理

在典型应用场景中，用户首先利用qubo模块进行问题建模，随后借助solver模块对构建的QUBO模型进行高效求解。solver模块负责管理QUBO模型的系数，并支持调用用户指定的optimizer对模型进行求解。

我们将模型求解功能定义为optimizer。目前社区版中包含基于经典计算实现的optimizer，如BruteForceOptimizer。用户也可以通过继承OptimizerBase类来实现自定义的优化器。

典型的使用方式
------------------

.. image:: images/Sequence_Diagram.png

预备知识
----------

Ising模型
^^^^^^^^^^^^

伊辛模型(Ising Model)，是一类描述物质相变的随机过程模型。抽象为数学形式为：

.. math:: H(\sigma)=-\sum_{i,j}J_{ij}\sigma_i\sigma_j-\mu\sum_ih_i\sigma_i

其中\ :math:`\sigma`\ 为待求自旋变量，取值为\ :math:`\{-1,1\}`\ ， \ :math:`H`\ 为哈密顿量， \ :math:`J`\为二次项系数，\ :math:`\mu`\和\ :math:`h`\ 为线性项系数，是已知量。

QUBO
^^^^^^

二次无约束二值优化问题(Quadratic unconstrained binary optimization，简称QUBO)，其数学形式如下：

.. math:: f_Q(x)=\sum_{i\leqslant j}q_{ij}x_ix_j

其中\ :math:`x`\ 为待求二进制变量, 取值为\ :math:`\{0,1\}`\ , \ :math:`f`\ 为目标函数, \ :math:`q`\ 为二次项系数, 是已知量.
写成线性代数的形式:

.. math:: f_Q(\pmb x)=\pmb x^T\pmb Q\pmb x

其中, \ :math:`\pmb x`\ 为二进制向量, \ :math:`\pmb Q`\ 为QUBO矩阵, QUBO目标是找到使得\ :math:`f`\ 最小或最大的\ :math:`\pmb x`\ , 即:

.. math:: \pmb x^*=\mathop{\arg\min}\limits_{\pmb x}f_Q(\pmb x)

在Kaiwu SDK中，通过查看QUBO模型细节会显示offset和coefficients信息。其中offset表示QUBO模型中的常数项，与变量无关。coefficients表示QUBO模型中每个二值变量的系数取值，以及它们的交互项的系数取值。

Citing Kaiwu SDK Community Edition
-----------------------------------

如果Kaiwu SDK 社区版对您的学术研究有帮助，欢迎引用：

.. code:: python

    @software{KaiwuSDKCommunity,
    title = {Kaiwu SDK Community Edition for QUBO problem solving},
    author = {{QBoson Inc.}},
    year = {2023},
    url = {https://github.com/qbosontech/kaiwu_community}
    }

或者

.. code:: python

    @misc{KaiwuSDKCommunity,
    title = {Kaiwu SDK Community Edition for QUBO problem solving},
    author = {{QBoson Inc.}},
    year = {2023},
    url = {https://github.com/qbosontech/kaiwu_community}
    }

概述
====

Kaiwu SDK
---------

Kaiwu SDK是一套软件开发套件，专为基于相干光量子计算机的QUBO问题求解而设计。该套件致力于为开发者提供一个便捷的Python环境，以构建适用于相干光量子计算机的软件算法，并直接通过物理接口（目前支持Ising矩阵）调用量子计算机真机进行计算。

Kaiwu SDK目前包含以下核心模块：qubo、cim、ising、preprocess、classical、sampler、solver和utils。在典型应用场景中，用户首先利用qubo模块进行问题建模，随后借助solver模块对构建的QUBO模型进行高效求解。solver模块不仅负责管理QUBO模型的系数，还支持调用用户指定的optimizer对最终的Ising模型矩阵进行深度求解。

我们特别将Ising模型矩阵的求解功能定义为optimizer。其中，基于经典计算实现的optimizer，如SA、tabu等经典模拟求解器，均集成在classical模块中；而直接对接真机的optimizer则位于cim模块。此外，其他辅助模块提供了日志记录、降阶处理和降精度处理等实用功能，为用户提供全方位的支持。

典型的使用方式
------------------

.. image:: images/Sequence_Diagram.png

预备知识
----------

CIM
^^^^^^

相干伊辛机(Coherent Ising Machine，简称CIM)，是目前玻色量子重点研发的一项量子计算机技术。CIM是一种基于简并光学参量振荡器(DOPO)的光量子计算机。在数学实践中，我们可以将其抽象为优化Ising模型的专用计算机。

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

在Kaiwu SDK中，通过kw.qubo.details查看QUBO模型细节会显示offset和coefficients信息。其中offset表示QUBO模型中的常数项，与变量无关。coefficients表示QUBO模型中每个二值变量的系数取值，以及它们的交互项的系数取值。

CIM求解模型
-----------

CIM求解QUBO或优化Ising模型的过程就是，将QUBO中的\ :math:`q_{ij}`\ 或Ising模型中的\ :math:`J_{ij}`\ 输入CIM，CIM返回\ :math:`\pmb x`\ 或\ :math:`\sigma`\ 的过程。

Citing Kaiwu SDK
---------------------------

如果Kaiwu SDK对您的学术研究有帮助，玻色量子感谢您做如下引用。

.. code:: python

    @software{KaiwuSDK,
    title = {Kaiwu SDK for development and research on coherent ising machine},
    author = {{QBoson Inc.}},
    year = {2022},
    url = {https://www.qboson.com/}
    }

或者

.. code:: python

    @misc{KaiwuSDK,
    title = {Kaiwu SDK for development and research on coherent ising machine},
    author = {{QBoson Inc.}},
    year = {2022},
    url = {https://www.qboson.com/}
    }

常见问题
========

本章节整理了使用Kaiwu SDK社区版过程中常见的问题和解决方案。

Q1: Kaiwu SDK社区版支持哪些Python版本？
----------------------------------------
A1: Kaiwu SDK社区版仅支持Python 3.10的所有小版本，不支持Python 3.11及以上版本。

Q2: 如何安装Kaiwu SDK社区版？
--------------------------------
A2: 您可以通过以下两种方式安装Kaiwu SDK社区版：

1. 从源码安装：

       git clone <repository-url>
       cd kaiwu_community
       pip install -e .

2. 从PyPI安装：

       pip install kaiwu-community

Q3: Kaiwu SDK社区版包含哪些核心模块？
----------------------------------------
A3: Kaiwu SDK社区版包含以下核心模块：

- qubo: 提供QUBO模型的构建和管理功能
- ising: 支持Ising模型的表示和转换
- classical: 包含经典优化算法，如BruteForceOptimizer
- solver: 提供求解器框架，支持调用不同的优化器
- core: 提供核心数据结构和数学运算支持
- common: 提供通用工具和配置管理

Q4: 如何构建QUBO模型？
------------------------
A4: 您可以使用qubo模块构建QUBO模型，具体步骤请参考：
- `TSP示例 <../getting_started/tsp.html>`_
- `MaxCut示例 <../getting_started/max_cut.html>`_

Q5: 如何创建自定义求解器和优化器？
------------------------------------
A5: 您可以通过继承OptimizerBase类创建自定义优化器，然后将其与求解器一起使用。具体请参考：
- `如何制作求解器和优化器 <../advanced/custom_solver_optimizer.html>`_

Q6: 遇到问题如何获取帮助？
----------------------------
A6: 您可以通过以下方式获取帮助：

1. 查看文档：
   - `快速开始 <../getting_started/index.html>`_
   - `安装说明 <../getting_started/sdk_installation_instructions.html>`_
   - `API文档 <../modules/index.html>`_

2. 提交Issue：
   - GitHub仓库：https://github.com/qbosontech/kaiwu_community

3. 加入社区：
   - 社区论坛：https://kaiwu.qboson.com/portal.php

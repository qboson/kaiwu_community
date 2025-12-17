发行说明
====================

1.0.0 (2025-12-17)
-------------------

发布日期
^^^^^^^^
2023年12月17日

主要功能
^^^^^^^^

- 提供完整的QUBO模型构建和管理功能
- 支持Ising模型的表示和转换
- 内置经典优化算法，如BruteForceOptimizer
- 提供灵活的求解器框架，支持调用不同的优化器
- 包含高效的核心数据结构和数学运算支持
- 提供通用工具和配置管理功能

核心模块
^^^^^^^^

Kaiwu SDK 社区版采用模块化设计，包含以下核心模块：

.. list-table:: 
   :widths: 20 40 40
   :header-rows: 1

   * - 模块名称
     - 主要功能
     - 价值
   * - **qubo**
     - 提供QUBO模型的构建和管理功能
     - 帮助用户快速构建QUBO模型
   * - **ising**
     - 支持Ising模型的表示和转换
     - 方便用户在QUBO和Ising模型之间转换
   * - **classical**
     - 包含经典优化算法，如BruteForceOptimizer
     - 提供基础求解能力，支持快速验证模型
   * - **solver**
     - 提供求解器框架，支持调用不同的优化器
     - 简化求解器调用流程，支持灵活扩展
   * - **core**
     - 提供核心数据结构和数学运算支持
     - 提供高效的底层计算能力
   * - **common**
     - 提供通用工具和配置管理
     - 简化开发流程，提高开发效率

版本兼容性
^^^^^^^^^^

- **Python版本**：仅支持Python 3.10的所有小版本，不支持Python 3.11及以上版本
- **操作系统**：支持Windows、Linux和macOS

安装方式
^^^^^^^^

- 从源码安装：

      git clone <repository-url>
      cd kaiwu_community
      pip install -e .

- 从PyPI安装：

      pip install kaiwu-community

已知问题
^^^^^^^^

- 暂无重大已知问题
- 如有问题，请在GitHub仓库提交Issue

联系方式
^^^^^^^^

- GitHub仓库：https://github.com/qbosontech/kaiwu_community
- 社区论坛：https://kaiwu.qboson.com/portal.php
- 技术支持：通过GitHub Issues提交问题
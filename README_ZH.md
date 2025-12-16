# Kaiwu SDK 社区版

<img src="https://img.shields.io/badge/Python-3.10%2B-blue" alt="Python Version"> <img src="https://img.shields.io/badge/License-Apache%202.0-green" alt="License">

**语言版本**: [中文](README_ZH.md) | [English](README.md)

## 📖 项目简介

**Kaiwu SDK 社区版** 是一款专为 QUBO（二次无约束二进制优化）问题设计的 Python 开发工具包。它提供了底层的数据结构实现和建模框架，帮助开发者快速构建自定义模型和求解器，实现高效的 QUBO 问题建模与求解。

### 🎯 核心价值

- **快速建模**：提供简洁易用的 API，支持快速构建复杂的 QUBO 模型
- **灵活扩展**：模块化设计，允许开发者轻松扩展新的求解器和优化算法
- **内置工具**：包含基础求解器和优化器，支持快速验证模型效果
- **开源自由**：基于 Apache 2.0 许可证，完全开源，支持商业和非商业使用

### 📋 应用场景

Kaiwu SDK 社区版适用于以下场景：
- 研究人员探索 QUBO 问题建模和求解算法
- 开发者构建自定义 QUBO 求解器和优化器
- 学生学习量子计算和组合优化问题
- 企业开发基于 QUBO 的解决方案原型

---

## 🚀 前置条件

在使用本 SDK 前，请确保已安装以下环境：

* **Python** ≥ 3.10
* **Make**（用于构建与测试命令）
* **Virtualenv**（可选，用于隔离环境：`pip install virtualenv`）

---

## 🛠 快速开始

请参考 [SDK 文档](https://kaiwu-sdk-docs.qboson.com/en/) 了解详细使用方法。

### 1. 克隆仓库

```bash
git clone <repository-url>
cd kaiwu_community
```

### 2. 配置环境

创建虚拟环境并安装依赖，同时运行代码检查与测试：

```bash
make all_tests
```

---

## 📘 示例程序

### 旅行商问题 (TSP) 示例

旅行商问题是组合优化中的经典问题，目标是找到一条访问所有城市并回到起点的最短路径。

Kaiwu SDK 社区版提供了一个完整的 TSP 求解示例，展示了如何使用 QUBO 模型建模和求解该问题：

* **文件路径**：[example/tsp\_sdk\_1\_2\_doc\_example.py](example/tsp_sdk_1_2_doc_example.py)
* **示例内容**：
  - 使用距离矩阵构建 TSP 问题模型
  - 定义 QUBO 目标函数和约束条件
  - 使用内置求解器求解模型
  - 验证求解结果的有效性

该示例展示了 Kaiwu SDK 的核心功能，包括 QUBO 模型构建、约束添加、模型求解和结果验证。

---

## 🤝 技术支持

* 加入 [Kaiwu 用户社区](https://kaiwu.qboson.com/portal.php)，与其他用户交流
* 访问 [Kaiwu SDK 帮助中心](https://kaiwu-sdk-docs.qboson.com/en/)，获取教程与知识库
* 在 **SDK GitHub 仓库** 提交 Issue 或功能请求

---

## 🔧 如何贡献

欢迎社区贡献！🎉

你可以扩展 SDK 功能，例如：

* 新的求解器实现
* 经典优化算法
* 模型转换工具
* 示例程序和文档

### 贡献示例

通过继承 `OptimizerBase` 创建自定义优化器：

```python
class NewOptimizer(OptimizerBase):
    ...
```

将自定义优化器与求解器一起使用：

```python
solver = kaiwu.solver.SimpleSolver(NewOptimizer())
```

➡️ 详细贡献指南请参考 [Contributing Guide](CONTRIBUTING.md)。

---

## 📜 许可证

本项目基于 **Apache License 2.0** 许可证开源。详情请参见 [LICENSE](LICENSE) 文件。

---

## 🏗 SDK 架构

Kaiwu SDK 社区版采用模块化设计，包含以下核心模块：

* **QUBO 模型**：提供 QUBO 问题建模功能
* **求解器框架**：支持多种求解器和优化器
* **经典优化器**：包含基础的经典求解算法
* **核心数据结构**：提供高效的数学运算支持

架构总览：

![Kaiwu SDK 架构](SDD/architecture.png)

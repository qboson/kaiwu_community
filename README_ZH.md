# Kaiwu SDK 社区版

<img src="https://img.shields.io/badge/Python-3.10%2B-blue" alt="Python Version"> <img src="https://img.shields.io/badge/License-Apache%202.0-green" alt="License">

**语言版本**: [中文](README_ZH.md) | [English](README.md)

**Kaiwu SDK 社区版** 是 Kaiwu SDK 的开源子集。它可以帮助用户快速构建 **QUBO（二次无约束二进制优化）模型**，并提供内置的求解器与优化器，用于解决 QUBO 问题。

---

## 🚀 前置条件

在使用本 SDK 前，请确保已安装以下环境：

* **Python** ≥ 3.8
* **Make**（用于构建与测试命令）
* **Virtualenv**（可选，用于隔离环境：`pip install virtualenv`）

---

## 🛠 快速开始

学习如何使用 **CIM（相干伊辛机）**，请参考 [SDK 文档](https://kaiwu-sdk-docs.qboson.com/en/)。

> ⚠️ 注意：此社区版仅包含 Kaiwu SDK 的部分功能子集。

### 1. 克隆仓库

```bash
git clone <repository-url>
cd kaiwu_community-sdk-community
```

### 2. 配置环境

创建虚拟环境并安装依赖，同时运行代码检查与测试：

```bash
make all_tests
```

---

## 📘 量子程序示例

查看如何使用 Kaiwu SDK 解决 **旅行商问题 (TSP)**，请参考：
[example/tsp\_sdk\_1\_2\_doc\_example.py](example/tsp_sdk_1_2_doc_example.py)

---

## 🤝 技术支持

* 加入 [Kaiwu 用户社区](https://kaiwu.qboson.com/portal.php)，与其他 CIM 用户交流
* 访问 [Kaiwu SDK 帮助中心](https://kaiwu-sdk-docs.qboson.com/en/)，获取教程与知识库
* 在 **SDK GitHub 仓库** 提交 Issue 或功能请求（📌 链接即将上线）

---

## 🔧 如何贡献

欢迎社区贡献！🎉

你可以扩展 SDK 功能，例如：

* 新的求解器
* 经典优化器
* 使用 **CIM 机器** 的实现

示例：通过继承 `OptimizerBase` 创建自定义优化器：

```python
class NewOptimizer(OptimizerBase):
    ...
```

如 [BruteForceOptimizer](src/kaiwu_community/classical/_simulated_annealing.py) 所示，可以将其与求解器一起使用：

```python
solver = kaiwu.solver.SimpleSolver(NewOptimizer())
```

➡️ 详细贡献指南请参考 [Contributing Guide](CONTRIBUTING.md)。

---

## 📜 许可证

本项目基于 **Apache License 2.0** 许可证开源。详情请参见 [LICENSE](LICENSE) 文件。

---

## 🏗 SDK 架构

本社区开源版本包含以下功能模块代码：

* **QUBO 模型**
* **SimpleSolver**
* **BruteForceOptimizer**

架构总览(绿框部分开源）：

![Kaiwu SDK 架构](SDD/architecture.png)

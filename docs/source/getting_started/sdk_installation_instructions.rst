安装说明
========

Kaiwu SDK 社区版提供多种安装方式，您可以根据自己的需求选择合适的安装方法。

1. 环境准备
-----------

   安装Python 3.10（不区分小版本），暂不支持Python其它版本。

   - 检查Python版本：

         python --version
         # 或
         python3 --version

   - 如果需要安装Python 3.10，请访问 `Python 3.10 下载页面 <https://www.python.org/downloads/release/python-31011/>`_。

2. 安装方式
-----------

以下是三种常用的安装方式：

2.1 从源码安装（推荐用于开发）
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

- 克隆仓库：

      git clone <repository-url>
      cd kaiwu_community

- 安装开发依赖：

      pip install -r requirements.txt

- 以可编辑模式安装SDK：

      pip install -e .

2.2 从PyPI安装（推荐用于使用）
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. note::
   该方式将在项目正式发布后可用。

    pip install kaiwu-community

2.3 直接使用源码
~~~~~~~~~~~~~~~~~

如果您不想安装SDK，也可以直接将源码目录添加到Python路径中使用：

    export PYTHONPATH=$PYTHONPATH:/path/to/kaiwu_community/src

3. 验证安装
-----------

   安装完成后，您可以通过以下方式验证SDK是否安装成功：

   .. code:: python

       import kaiwu_community as kw
       print("Kaiwu SDK Community Edition installed successfully!")

4. 开发环境设置
---------------

   如果您计划参与SDK的开发，可以使用以下命令运行所有测试和代码检查：

       make all_tests

   这将运行：
   - 代码风格检查（pylint）
   - 单元测试（pytest）
   - 文档测试（doctest）

5. 卸载SDK
-----------

   如果您需要卸载SDK，可以使用以下命令：

       pip uninstall kaiwu-community

   或者如果是从源码安装：

       pip uninstall kaiwu-community

   然后删除克隆的仓库目录。

安装说明
========

1. 安装Python3.10（不区分小版本），暂不支持Python其它版本，Python安装请自行搜索相关教程。

2. 创建虚拟环境，激活虚拟环境在命令行输入: python --version, 检查python版本是否为3.10。

   `python 3.10 下载 <https://www.python.org/downloads/release/python-31011/>`_。

3. 登录网站 (https://platform.qboson.com/) 获取用户ID和SDK授权码。

4. 根据个人电脑操作系统在官网下载对应的SDK，文件命名如：kaiwu-sdk.linux.1.2.0.zip(mac有intel和m两个版本，
   使用过程中如提醒架构有问题，请尝试不同的版本，如果两个版本都不行请联系相关人员)。

5. 解压下载的SDK安装包，解压后会有一个whl文件。

6. 安装SDK，使用pip安装时注意whl文件路径和系统版本。

    .. code:: python

        pip3 install kaiwu-1.2.0-cp310-none-win_amd64.whl -i https://pypi.tuna.tsinghua.edu.cn/simple

7. 建模代码开头增加授权初始化代码，如果初始化错误请校验用户ID和SDK授权码或清除kaiwu/license.lic文件，然后重新初始化。

    .. code:: python

       import kaiwu as kw
       kw.license.init(user_id="123456", sdk_code="AjUvlTvWrWeidADu5Vbf6pceVmuX")

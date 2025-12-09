"""
日志
"""
import logging
import sys

# 模块级单例初始化（Python保证模块导入时只执行一次）
_root_logger = logging.getLogger("kaiwu_community")
_root_logger.setLevel(logging.INFO)
_root_logger.propagate = False  # 禁止向上传播

# 统一配置控制台Handler
_console_handler = logging.StreamHandler(sys.stdout)
_console_handler.setLevel(logging.NOTSET)  # 处理所有级别

# 标准化格式
_formatter = logging.Formatter(
    '[%(asctime)s] [%(levelname)-8s] [%(name)s:%(lineno)d] - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
_console_handler.setFormatter(_formatter)

# 确保只添加一次Handler
if not _root_logger.handlers:
    _root_logger.addHandler(_console_handler)


def set_log_level(level):
    """设置SDK日志输出级别

    SDK默认输出INFO级别以上的日志，可通过此函数修改输出级别

    Args:
        level (str or int): 支持传入 logging.ERROR， logging.INFO、... 、logging.ERROR或字符串ERROR、INFO、... 、ERROR

    Examples:
        >>> import kaiwu_community as kw
        >>> kw.common.set_log_level(level="DEBUG")  # doctest: +SKIP
    """
    level = level.upper() if isinstance(level, str) else level
    _root_logger.setLevel(level)


def set_log_path(path="/tmp/output.log"):
    """设置SDK日志输出文件路径, 需要绝对路径.

    Args:
        path (str): 自定义日志文件输出路径

    Examples:
        >>> import kaiwu_community as kw
        >>> kw.common.set_log_path("/tmp/output.log")  # doctest: +SKIP
    """
    file_handler = logging.FileHandler(path)
    file_handler.setFormatter(_formatter)
    _root_logger.addHandler(file_handler)

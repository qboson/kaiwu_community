import os

# 项目根路径
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# SDK路径 项目根路径下
SDK_DIR = os.path.join(BASE_DIR, "src/com/qboson/kaiwu")
# SDK 编译后保存目录
TARGET_PATH = os.path.join(BASE_DIR, 'target/kaiwu')
# 临时文件存放路径
MEDIA_ROOT = os.path.join(BASE_DIR, "media/files")
if not os.path.exists(MEDIA_ROOT):
    os.makedirs(MEDIA_ROOT)
# SDK 版本
SDK_RELEASE_VERSION = os.getenv("SDK_RELEASE_VERSION", "1.3.0")

try:
    from config_local import *  # noqa
except ImportError:
    pass

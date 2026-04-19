import os
from datetime import timedelta
from dotenv import load_dotenv

# 强制加载当前目录下的 .env 文件到系统环境变量中
load_dotenv()

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'matrix_pilot_super_secret_key')
    PERMANENT_SESSION_LIFETIME = timedelta(days=30)

    # 强制清除末尾可能混入的空格、\r 或 \n 换行符
    APP_PIN = os.environ.get('APP_PIN', '').strip()
    API_KEY = os.environ.get('API_KEY', '').strip()

    if not API_KEY or not APP_PIN:
        raise ValueError("🚨 启动失败：未在环境中检测到 API_KEY 或 APP_PIN！请在 .env 文件中正确配置它们。")

    # 目录配置
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))
    INSTANCE_PATH = os.path.join(BASE_DIR, 'db')
    
    if not os.path.exists(INSTANCE_PATH):
        os.makedirs(INSTANCE_PATH)

    # MatrixPilot 主数据库配置 (ORM)
    SQLALCHEMY_DATABASE_URI = f"sqlite:///{os.path.join(INSTANCE_PATH, 'matrix_pilot.db')}"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # 🌟 新增：SQLAlchemy 并发引擎安全配置
    SQLALCHEMY_ENGINE_OPTIONS = {
        "connect_args": {
            "timeout": 15,              # 延长锁等待时间
            "check_same_thread": False  # 允许多线程安全共享连接
        }
    }

    # LittlePilot 数据库及文件路径
    LP_DB_PATH = os.path.join(INSTANCE_PATH, 'log.db')
    ROUND_SETTINGS_FILE = os.path.join(INSTANCE_PATH, 'round_settings.json')
    
    # 安装包目录
    FILE_DIRECTORY = os.path.join(BASE_DIR, 'file')
    if not os.path.exists(FILE_DIRECTORY):
        os.makedirs(FILE_DIRECTORY)
    
    # ============================================================
    # 缓存配置（用于替代全局状态）
    # ============================================================
    CACHE_TYPE = 'SimpleCache'  # 开发环境使用内存缓存
    CACHE_DEFAULT_TIMEOUT = 300  # 默认缓存5分钟
    # 生产环境可切换为 Redis:
    # CACHE_TYPE = 'RedisCache'
    # CACHE_REDIS_URL = 'redis://localhost:6379/0'
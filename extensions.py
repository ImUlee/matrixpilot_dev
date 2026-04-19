"""
Flask扩展模块

集中管理Flask扩展实例
"""
from flask_sqlalchemy import SQLAlchemy
from flask_caching import Cache
from apscheduler.schedulers.background import BackgroundScheduler
from functools import wraps

# 数据库ORM
db = SQLAlchemy()

# 缓存实例（用于替代全局状态）
cache = Cache()

# 定时任务调度器
scheduler = BackgroundScheduler()


def cached_query(timeout: int = 60, key_prefix: str = None):
    """查询缓存装饰器
    
    用于缓存数据库查询结果，减少数据库访问
    
    Args:
        timeout: 缓存超时时间（秒）
        key_prefix: 缓存键前缀
        
    Usage:
        @cached_query(timeout=120, key_prefix='user_stats')
        def get_user_stats(user_id):
            return db.session.query(User).filter_by(id=user_id).first()
    """
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            # 生成缓存键
            cache_key = f"{key_prefix or f.__name__}:{args}:{kwargs}"
            
            # 尝试从缓存获取
            result = cache.get(cache_key)
            if result is not None:
                return result
            
            # 执行函数并缓存结果
            result = f(*args, **kwargs)
            cache.set(cache_key, result, timeout=timeout)
            
            return result
        return decorated_function
    return decorator

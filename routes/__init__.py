"""
路由蓝图注册中心

所有子蓝图在此统一注册到主应用，实现路由模块化管理
"""
from flask import Flask

from .auth import auth_bp
from .health import health_bp
from .nodes import nodes_bp
from .records import records_bp
from .stats import stats_bp
from .settings import settings_bp
from .upload import upload_bp
from .search import search_bp
from .api import docs_bp


def register_blueprints(app: Flask) -> None:
    """注册所有蓝图到Flask应用
    
    Args:
        app: Flask应用实例
        
    Note:
        每个蓝图的url_prefix已在各模块中定义
        注册顺序不影响路由匹配
    """
    app.register_blueprint(auth_bp)
    app.register_blueprint(health_bp)
    app.register_blueprint(nodes_bp)
    app.register_blueprint(records_bp)
    app.register_blueprint(stats_bp)
    app.register_blueprint(settings_bp)
    app.register_blueprint(upload_bp)
    app.register_blueprint(search_bp)
    
    # 注册API文档
    from api_docs import api
    api.init_app(app)


__all__ = ['register_blueprints']

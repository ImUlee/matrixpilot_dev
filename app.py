"""
MatrixPilot 主应用入口

Flask应用工厂模式，支持灵活的配置和扩展
"""
import logging
from logging.handlers import RotatingFileHandler
import os
import urllib.parse
from datetime import datetime
from flask import Flask, g
import requests

from config import Config
from extensions import db, scheduler, cache
from models import Settings, Record
from services.db_utils import init_mp_db, init_lp_db
from routes import register_blueprints
from constants import BarkSound, BarkGroup
from self_check import require_self_check


def setup_logging(app):
    """配置日志系统
    
    设置文件日志和控制台日志
    """
    # 确保日志目录存在
    log_dir = os.path.join(os.path.dirname(__file__), 'logs')
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)
    
    formatter = logging.Formatter(
        '%(asctime)s %(levelname)s [%(name)s] %(message)s'
    )
    
    # 文件处理器 - 10MB轮转，保留5个备份
    file_handler = RotatingFileHandler(
        os.path.join(log_dir, 'matrixpilot.log'),
        maxBytes=10 * 1024 * 1024,
        backupCount=5,
        encoding='utf-8'
    )
    file_handler.setFormatter(formatter)
    file_handler.setLevel(logging.INFO)
    
    # 控制台处理器
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    console_handler.setLevel(logging.INFO)
    
    # 应用日志器
    app.logger.addHandler(file_handler)
    app.logger.addHandler(console_handler)
    app.logger.setLevel(logging.INFO)


def check_notifications(app):
    """定时任务：检查是否有需要推送的轮次提醒
    
    每分钟执行一次，检查是否有到期的轮次需要通知
    """
    try:
        with app.app_context():
            settings = Settings.query.first()
            # 检查是否启用 Bark 通知
            if not settings or not getattr(settings, 'bark_enabled', False):
                return
            if not settings.bark_url:
                return
            
            now_str = datetime.now().strftime('%Y-%m-%d %H:%M')
            pending_records = Record.query.filter(
                Record.next_time != '--',
                Record.next_time != None,
                Record.notified == False
            ).all()
            
            base_url = settings.bark_url.rstrip('/')
            
            for r in pending_records:
                if now_str >= r.next_time:
                    # 原子更新，防止重复通知
                    updated = Record.query.filter_by(
                        id=r.id, 
                        notified=False
                    ).update({'notified': True})
                    db.session.commit()
                    
                    if updated > 0:
                        group_name = list(r.data.keys())[0]
                        raw_title = settings.bark_title.replace(
                            "{group}", group_name
                        ).replace("{time}", r.next_time)
                        raw_body = settings.bark_body.replace(
                            "{group}", group_name
                        ).replace("{time}", r.next_time)
                        
                        t_enc = urllib.parse.quote(raw_title, safe='')
                        b_enc = urllib.parse.quote(raw_body, safe='')
                        api_url = f"{base_url}/{t_enc}/{b_enc}"
                        
                        params = {
                            "sound": BarkSound.MINUET.value,
                            "group": BarkGroup.MAIN.value,
                            "isArchive": "1"
                        }
                        if settings.bark_icon:
                            params["icon"] = settings.bark_icon
                        
                        try:
                            requests.get(api_url, params=params, timeout=10)
                            app.logger.info(f"轮次通知已发送: {group_name}")
                        except Exception as e:
                            app.logger.error(f"Bark通知发送失败: {e}")
                            
    except Exception as e:
        app.logger.error(f"通知线程监测异常: {e}")


def create_app():
    """应用工厂函数
    
    创建并配置Flask应用实例
    
    Returns:
        配置完成的Flask应用
    """
    # 获取项目根目录
    import pathlib
    base_dir = pathlib.Path(__file__).parent.resolve()
    
    # 1. 实例化核心 - 配置静态文件路径
    app = Flask(
        __name__,
        static_folder=str(base_dir / 'static' / 'dist'),
        static_url_path='/'  # 根路径，这样 /manifest.json 等可访问
    )
    app.config.from_object(Config)

    # 2. 配置日志
    setup_logging(app)
    app.logger.info("MatrixPilot 启动中...")
    
    # 2.1 启动自检
    require_self_check()

    # 3. 初始化插件
    db.init_app(app)
    cache.init_app(app)  # 初始化缓存
    app.logger.info("缓存初始化完成")
    
    # 4. 注册所有蓝图
    register_blueprints(app)
    app.logger.info("路由蓝图注册完成")
    
    # 4.1 Vue SPA 路由配置
    @app.route('/')
    def spa_root():
        from flask import send_from_directory
        return send_from_directory('static/dist', 'index.html')
    
    # Vue 编译后的 assets 路由（JS/CSS）
    @app.route('/assets/<path:filename>')
    def serve_vue_assets(filename):
        from flask import send_from_directory
        return send_from_directory('static/dist/assets', filename)

    # 5. 数据库初始化
    init_mp_db(app)
    init_lp_db()
    app.logger.info("数据库初始化完成")

    # 6. 定时任务
    scheduler.add_job(
        func=lambda: check_notifications(app), 
        trigger="interval", 
        seconds=60
    )
    
    # 7. 请求结束后清理数据库连接
    @app.teardown_appcontext
    def close_db_connection(exception):
        lp_db = getattr(g, 'lp_db', None)
        if lp_db is not None:
            lp_db.close()
    
    app.logger.info("MatrixPilot 启动完成")
    return app


# ==========================================
# 启动配置
# ==========================================
app = create_app()
APP_DEBUG_MODE = True

# 避免在Flask debug自动重载时重复启动调度器
if not APP_DEBUG_MODE or os.environ.get('WERKZEUG_RUN_MAIN') == 'true':
    scheduler.start()

if __name__ == '__main__':
    app.run(debug=APP_DEBUG_MODE, host='0.0.0.0', port=5000)

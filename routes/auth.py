"""认证相关路由

处理用户登录、登出等认证功能
"""
from functools import wraps
from flask import Blueprint, request, redirect, url_for, session, jsonify, send_from_directory

from config import Config

auth_bp = Blueprint('auth', __name__)


def login_required(f):
    """登录验证装饰器
    
    用于保护需要认证的路由
    
    Args:
        f: 被装饰的视图函数
        
    Returns:
        如果已登录则执行原函数，否则重定向到登录页
        
    Usage:
        @auth_bp.route('/protected')
        @login_required
        def protected_view():
            return "Protected content"
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get('logged_in'):
            return redirect('/#/login')
        return f(*args, **kwargs)
    return decorated_function


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    """登录API
    
    GET: 返回Vue SPA入口（前端路由处理登录页）
    POST: 验证PIN码并建立会话
    
    Returns:
        GET: Vue SPA入口HTML
        POST: JSON响应
    """
    if request.method == 'POST':
        # 支持 JSON 和表单两种方式
        if request.is_json:
            pin = request.json.get('pin', '')
        else:
            pin = request.form.get('pin', '')
        
        if pin == Config.APP_PIN:
            session.permanent = True
            session['logged_in'] = True
            return jsonify({'success': True, 'message': '登录成功'})
        else:
            return jsonify({'success': False, 'error': '访问密码错误'}), 401
    
    # GET请求返回Vue SPA入口
    return send_from_directory('static/dist', 'index.html')


@auth_bp.route('/logout')
def logout():
    """登出
    
    清除会话并重定向到登录页
    """
    session.pop('logged_in', None)
    return redirect(url_for('auth.login'))


@auth_bp.route('/check_auth')
def check_auth():
    """检查认证状态
    
    返回当前用户的登录状态
    """
    return jsonify({'logged_in': session.get('logged_in', False)})


# 注意：/manifest.json, /icon-*.png 等静态文件由 Flask 的 static 自动服务（static_url_path='/'）

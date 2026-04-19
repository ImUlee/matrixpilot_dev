"""API文档路由

使用Flask-RESTX提供Swagger文档
"""
from flask import Blueprint
from flask_restx import Resource

from api_docs import api, ns_auth, ns_stats, ns_nodes, ns_search
from api_docs import login_model, login_response, auth_status, stats_model
from api_docs import nodes_response, search_result, faq_response, error_model
from routes.auth import login_required


# 创建蓝图
docs_bp = Blueprint('api_docs', __name__, url_prefix='/api')


# ==================== 认证接口 ====================

@ns_auth.route('/login')
class Login(Resource):
    @ns_auth.doc('login')
    @ns_auth.expect(login_model)
    @ns_auth.response(200, '成功', login_response)
    @ns_auth.response(401, '认证失败', error_model)
    def post(self):
        """用户登录
        
        使用PIN码进行身份验证
        """
        from flask import request, session, jsonify
        from config import Config
        
        data = request.get_json() or {}
        pin = data.get('pin', '')
        
        if pin == Config.APP_PIN:
            session.permanent = True
            session['logged_in'] = True
            return {'success': True, 'message': '登录成功'}
        
        return {'success': False, 'error': '访问密码错误'}, 401


@ns_auth.route('/check_auth')
class CheckAuth(Resource):
    @ns_auth.doc('check_auth')
    @ns_auth.response(200, '成功', auth_status)
    def get(self):
        """检查登录状态
        
        返回当前用户的认证状态
        """
        from flask import session
        return {'logged_in': session.get('logged_in', False)}


@ns_auth.route('/logout')
class Logout(Resource):
    @ns_auth.doc('logout')
    @ns_auth.response(200, '成功', login_response)
    def get(self):
        """用户登出
        
        清除当前会话
        """
        from flask import session
        session.pop('logged_in', None)
        return {'success': True, 'message': '已登出'}


# ==================== 统计接口 ====================

@ns_stats.route('/stats')
class Stats(Resource):
    @ns_stats.doc('get_stats')
    @ns_stats.param('device_id', '设备ID筛选', default='ALL')
    @ns_stats.response(200, '成功', stats_model)
    @ns_stats.response(401, '未授权')
    def get(self):
        """获取统计数据
        
        返回排行榜、详细数据等统计信息
        """
        from flask import request
        from services.db_utils import get_lp_db
        from services.round_state import get_round_times
        
        device_id = request.args.get('device_id', 'ALL')
        conn = get_lp_db()
        c = conn.cursor()
        
        # 获取统计数据
        c.execute('''
            SELECT COUNT(DISTINCT nickname) as total_users,
                   COUNT(*) as total_wins
            FROM logs
        ''')
        row = c.fetchone()
        
        return {
            'total_users': row['total_users'] if row else 0,
            'total_wins': row['total_wins'] if row else 0,
            'total_physical_wins': 0,
            'rank_list': [],
            'details': [],
            'round_times': get_round_times()
        }


# ==================== 节点接口 ====================

@ns_nodes.route('/manage_nodes')
class ManageNodes(Resource):
    @ns_nodes.doc('get_nodes')
    @ns_nodes.response(200, '成功', nodes_response)
    @ns_nodes.response(401, '未授权')
    def get(self):
        """获取节点列表
        
        返回所有节点及其状态
        """
        from services.db_utils import get_lp_db
        from constants import Message
        
        conn = get_lp_db()
        c = conn.cursor()
        
        c.execute('''
            SELECT 
                l.device_id, 
                COUNT(l.id) as log_count, 
                MAX(l.log_time) as last_log_time, 
                d.nickname 
            FROM logs l 
            LEFT JOIN devices d ON l.device_id = d.device_id 
            GROUP BY l.device_id 
            ORDER BY last_log_time DESC
        ''')
        
        nodes = []
        for r in c.fetchall():
            nodes.append({
                'device_id': r['device_id'],
                'nickname': r['nickname'] if r['nickname'] else '已离线历史节点',
                'log_count': r['log_count'],
                'last_log_time': r['last_log_time'],
                'is_active': bool(r['nickname'])
            })
        
        return {'status': Message.Common.SUCCESS, 'nodes': nodes}


# ==================== 搜索接口 ====================

@ns_search.route('/public_search')
class PublicSearch(Resource):
    @ns_search.doc('public_search')
    @ns_search.param('nickname', '用户昵称', required=True)
    @ns_search.param('start_date', '开始日期')
    @ns_search.param('end_date', '结束日期')
    @ns_search.response(200, '成功', search_result)
    def get(self):
        """公开搜索
        
        根据昵称搜索用户数据
        """
        from flask import request
        from services.db_utils import get_lp_db
        
        nickname = request.args.get('nickname', '').strip()
        
        if not nickname:
            return {'found': False}
        
        conn = get_lp_db()
        c = conn.cursor()
        
        c.execute(
            "SELECT nickname FROM logs WHERE nickname = ? COLLATE NOCASE LIMIT 1",
            (nickname,)
        )
        user = c.fetchone()
        
        if not user:
            return {'found': False, 'has_suggestion': False}
        
        return {'found': True, 'display_nickname': user['nickname']}


@ns_search.route('/faq')
class FAQ(Resource):
    @ns_search.doc('get_faq')
    @ns_search.response(200, '成功', faq_response)
    def get(self):
        """获取FAQ
        
        返回常见问题列表
        """
        from models import Settings
        import json
        
        settings = Settings.query.first()
        try:
            faq_list = json.loads(settings.faq_json) if settings and settings.faq_json else []
        except:
            faq_list = []
        
        return {'faq': faq_list}

"""搜索查询路由

处理公共搜索、历史管理等
"""
from flask import Blueprint, request, jsonify, send_from_directory

from .auth import login_required
from models import Settings
from services.db_utils import get_lp_db
from utils import format_datetime_param
from constants import Message

search_bp = Blueprint('search', __name__)


@search_bp.route('/query')
def public_search_page():
    """公共搜索页面 - 返回Vue SPA入口"""
    return send_from_directory('static/dist', 'index.html')


@search_bp.route('/api/faq')
def api_faq():
    """获取FAQ数据
    
    返回系统配置的FAQ列表
    """
    settings = Settings.query.first()
    try:
        faq_list = settings.faq_json if settings and settings.faq_json else '[]'
        import json
        faq_data = json.loads(faq_list)
    except:
        faq_data = []
    
    return jsonify({'faq': faq_data})


@search_bp.route('/api/public_search')
def api_public_search():
    """公共搜索API
    
    根据昵称查询用户数据
    """
    query_name = request.args.get('nickname', '').strip()
    start_date = request.args.get('start_date', '').strip()
    end_date = request.args.get('end_date', '').strip()
    
    if not query_name:
        return jsonify({"found": False})
    
    conn = get_lp_db()
    c = conn.cursor()
    
    try:
        # 精确匹配
        c.execute(
            "SELECT nickname FROM logs WHERE nickname = ? COLLATE NOCASE LIMIT 1", 
            (query_name,)
        )
        exact_user = c.fetchone()
        
        if not exact_user:
            # 模糊匹配建议
            c.execute(
                "SELECT DISTINCT nickname FROM logs WHERE nickname LIKE '%' || ? || '%' LIMIT 10", 
                (query_name,)
            )
            fuzzy_users = c.fetchall()
            if fuzzy_users:
                return jsonify({
                    "found": False, 
                    "has_suggestion": True, 
                    "suggestions": [row['nickname'] for row in fuzzy_users]
                })
            else:
                return jsonify({"found": False, "has_suggestion": False})
        
        real_name = exact_user['nickname']
        
        # 构建查询
        query_diamond = '''
            SELECT SUM(quantity) as total_sum, MAX(quantity) as max_win 
            FROM logs 
            WHERE nickname = ? AND (item_type = '钻石' OR item_type = '动态')
        '''
        query_physical = '''
            SELECT COUNT(*) as physical_count 
            FROM logs 
            WHERE nickname = ? AND item_type != '钻石' AND item_type != '动态'
        '''
        query_times = "SELECT COUNT(*) as win_times FROM logs WHERE nickname = ?"
        query_logs = '''
            SELECT 
                l.log_time as date, l.quantity, l.item_type, 
                COALESCE(d.nickname, '已离线历史节点') as node 
            FROM logs l 
            LEFT JOIN devices d ON l.device_id = d.device_id 
            WHERE l.nickname = ?
        '''
        
        base_params = [real_name]
        time_params = []
        
        if start_date:
            time_filter = " AND log_time >= ?"
            query_diamond += time_filter
            query_physical += time_filter
            query_times += time_filter
            query_logs += time_filter
            time_params.append(format_datetime_param(start_date, is_end=False))
            
        if end_date:
            time_filter = " AND log_time <= ?"
            query_diamond += time_filter
            query_physical += time_filter
            query_times += time_filter
            query_logs += time_filter
            time_params.append(format_datetime_param(end_date, is_end=True))
        
        query_logs += " ORDER BY l.log_time DESC LIMIT 50"
        full_params = base_params + time_params
        
        # 执行查询
        c.execute(query_diamond, full_params)
        diamond_stats = c.fetchone()
        
        c.execute(query_physical, full_params)
        physical_stats = c.fetchone()
        
        c.execute(query_times, full_params)
        total_times_stats = c.fetchone()
        
        c.execute(query_logs, full_params)
        logs = [dict(row) for row in c.fetchall()]
        
        return jsonify({
            "found": True,
            "real_nickname": real_name,
            "total_sum": diamond_stats['total_sum'] or 0,
            "max_win": diamond_stats['max_win'] or 0,
            "physical_count": physical_stats['physical_count'] or 0,
            "win_times": total_times_stats['win_times'] or 0,
            "logs": logs
        })
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@search_bp.route('/api/manage_history', methods=['POST'])
@login_required
def manage_history():
    """历史记录管理
    
    支持合并和删除操作
    """
    data = request.json
    action = data.get('action')
    target_nickname = data.get('nickname')
    
    if not target_nickname:
        return jsonify({
            "status": Message.Common.ERROR, 
            "message": Message.History.INVALID_NICKNAME
        }), 400
    
    conn = get_lp_db()
    cursor = conn.cursor()
    
    try:
        if action == 'merge':
            new_nickname = data.get('new_nickname', '').strip()
            if not new_nickname or new_nickname == target_nickname:
                return jsonify({
                    "status": Message.Common.ERROR, 
                    "message": Message.History.INVALID_NEW_NICKNAME
                }), 400
            
            cursor.execute(
                "UPDATE logs SET nickname = ? WHERE nickname = ?", 
                (new_nickname, target_nickname)
            )
            conn.commit()
            
            return jsonify({
                "status": Message.Common.SUCCESS, 
                "message": Message.History.MERGE_SUCCESS.format(
                    old=target_nickname, 
                    new=new_nickname
                )
            })
            
        elif action == 'delete':
            cursor.execute("DELETE FROM logs WHERE nickname = ?", (target_nickname,))
            conn.commit()
            
            return jsonify({
                "status": Message.Common.SUCCESS, 
                "message": Message.History.DELETE_SUCCESS.format(nickname=target_nickname)
            })
            
    except Exception as e:
        return jsonify({
            "status": Message.Common.ERROR, 
            "message": str(e)
        }), 500


@search_bp.route('/api/templates', methods=['GET'])
@login_required
def get_templates():
    """获取模板列表"""
    return jsonify({"templates": []})

"""节点管理路由

处理节点的查询、删除等操作
"""
from flask import Blueprint, request, jsonify

from .auth import login_required
from services.db_utils import get_lp_db
from constants import Message

nodes_bp = Blueprint('nodes', __name__)


# 兼容路由：前端调用 /api/nodes，后端提供 /api/manage_nodes
@nodes_bp.route('/api/nodes', methods=['GET'])
@login_required
def nodes_list():
    """节点列表兼容接口
    
    前端调用的路由，后端实际指向 manage_nodes
    """
    conn = get_lp_db()
    c = conn.cursor()
    return _get_nodes_list(c)


@nodes_bp.route('/api/manage_nodes', methods=['GET', 'POST'])
@login_required
def manage_nodes():
    """节点管理接口
    
    GET: 获取所有节点列表
    POST: 执行节点操作 (删除等)
    
    Returns:
        JSON格式的节点数据或操作结果
    """
    conn = get_lp_db()
    c = conn.cursor()
    
    if request.method == 'GET':
        return _get_nodes_list(c)
    else:
        return _handle_node_action(conn, c, request.json)


def _get_nodes_list(cursor):
    """获取节点列表
    
    Args:
        cursor: 数据库游标
        
    Returns:
        JSON响应，包含节点列表
    """
    cursor.execute('''
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
    
    nodes_data = []
    for r in cursor.fetchall():
        nodes_data.append({
            "device_id": r['device_id'],
            "nickname": r['nickname'] if r['nickname'] else "已离线历史节点",
            "log_count": r['log_count'],
            "last_log_time": r['last_log_time'],
            "is_active": bool(r['nickname'])
        })
    
    return jsonify({
        "status": Message.Common.SUCCESS, 
        "nodes": nodes_data
    })


def _handle_node_action(conn, cursor, data):
    """处理节点操作
    
    Args:
        conn: 数据库连接
        cursor: 数据库游标
        data: 请求数据
        
    Returns:
        JSON响应，包含操作结果
    """
    action = data.get('action')
    
    try:
        if action == 'delete':
            target_id = data.get('target_id')
            if not target_id:
                return jsonify({
                    "status": Message.Common.ERROR, 
                    "message": Message.Node.INVALID_PARAM
                }), 400
            
            cursor.execute(
                "DELETE FROM devices WHERE device_id = ?", 
                (target_id,)
            )
            conn.commit()
            
            return jsonify({
                "status": Message.Common.SUCCESS, 
                "message": Message.Node.DELETE_SUCCESS
            })
        else:
            return jsonify({
                "status": Message.Common.ERROR, 
                "message": f"未知操作: {action}"
            }), 400
            
    except Exception as e:
        return jsonify({
            "status": Message.Common.ERROR, 
            "message": str(e)
        }), 500


@nodes_bp.route('/api/clear_unparsed', methods=['POST'])
@login_required
def clear_unparsed():
    """清除未解析日志
    
    删除所有未解析的日志记录，并重置设备状态
    """
    conn = get_lp_db()
    c = conn.cursor()
    
    c.execute("DELETE FROM unparsed_logs")
    c.execute("UPDATE devices SET last_msg = '正常'")
    conn.commit()
    
    return jsonify({"status": Message.Common.SUCCESS})

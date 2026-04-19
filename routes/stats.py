"""统计数据路由

处理大屏统计、排行榜等数据查询
"""
import time
from datetime import datetime, timedelta
from flask import Blueprint, request, jsonify, session

from .auth import login_required
from services.db_utils import get_lp_db
from services.round_state import (
    get_round_times, 
    set_round_times, 
    reset_all_to_global,
    update_round_time
)
from constants import ItemType, Message

stats_bp = Blueprint('stats', __name__)


@stats_bp.route('/api/data', methods=['GET'])
@login_required
def get_data():
    """获取MatrixPilot主数据
    
    返回设置、物品列表、记录列表
    """
    from extensions import db
    from models import Settings, Item, Record
    
    settings = Settings.query.first()
    if not settings:
        settings = Settings(
            interval_hours=72,
            bark_enabled=False,
            bark_url='',
            bark_title='MatrixPilot 提醒',
            bark_body='分组【{group}】预计下轮时间已到！',
            bark_icon='',
            bark_notify_physical=False,
            bark_physical_title='🎁 实物掉落提醒',
            bark_physical_body='【{nickname}】抽中 {item} x{quantity}',
            faq_json='[]',
            parsers_json='[]'
        )
        db.session.add(settings)
        db.session.commit()
    
    items = Item.query.order_by(Item.sort_order.asc(), Item.id.asc()).all()
    records = Record.query.order_by(Record.date.desc()).all()
    
    return jsonify({
        'settings': {
            'interval_hours': settings.interval_hours,
            'bark_enabled': bool(settings.bark_enabled),
            'bark_url': settings.bark_url or '',
            'bark_title': settings.bark_title or '',
            'bark_body': settings.bark_body or '',
            'bark_icon': settings.bark_icon or '',
            'bark_notify_physical': bool(settings.bark_notify_physical),
            'bark_physical_title': settings.bark_physical_title or '',
            'bark_physical_body': settings.bark_physical_body or '',
            'faq_json': settings.faq_json or '[]',
            'parsers_json': settings.parsers_json or '[]'
        },
        'items': [{'id': i.id, 'name': i.name} for i in items],
        'records': [
            {
                'id': r.id,
                'date': r.date,
                'next_time': r.next_time,
                'group': list(r.data.keys())[0] if r.data else '',
                'quantity': list(r.data.values())[0] if r.data else 0
            } 
            for r in records
        ]
    })


@stats_bp.route('/api/stats')
@login_required
def get_stats():
    """获取大屏统计数据
    
    核心统计接口，返回排行榜、详情等
    """
    conn = get_lp_db()
    c = conn.cursor()
    device_filter = request.args.get('device_id', 'ALL')
    
    try:
        # 获取未解析日志数量
        c.execute("SELECT COUNT(*) as uc FROM unparsed_logs")
        unparsed_count = c.fetchone()['uc']
        
        # 获取最新未解析样例
        latest_unparsed_sample = ""
        if unparsed_count > 0:
            c.execute("SELECT raw_content FROM unparsed_logs ORDER BY id DESC LIMIT 1")
            u_row = c.fetchone()
            if u_row and u_row['raw_content']:
                latest_unparsed_sample = u_row['raw_content'][:500]
        
        # 获取轮次时间配置
        current_times = get_round_times()
        global_time = current_times.get('GLOBAL')
        
        if not global_time:
            c.execute("SELECT MIN(log_time) as min_t FROM logs")
            min_row = c.fetchone()
            global_time = min_row['min_t'] if min_row and min_row['min_t'] else "2000-01-01 00:00:00"
        
        # 获取节点映射
        c.execute("SELECT device_id, nickname FROM devices")
        node_map = {row['device_id']: row['nickname'] for row in c.fetchall()}
        node_map['GLOBAL'] = "ALL"
        
        # 过滤已删除节点
        valid_times = {
            did: t_str 
            for did, t_str in current_times.items()
            if did == 'GLOBAL' or did in node_map
        }
        
        # 构建时间范围显示
        all_ranges_list = [
            {
                "nick": node_map.get(did, "ALL"),
                "time": t_str,
                "formatted": f"{node_map.get(did, 'ALL')} RE: {t_str[5:16]}"
            }
            for did, t_str in valid_times.items()
        ]
        all_ranges_list.sort(key=lambda x: x['time'], reverse=True)
        
        if device_filter != 'ALL':
            t = valid_times.get(device_filter, valid_times.get('GLOBAL', global_time))
            n = node_map.get(device_filter, "未知节点")
            date_range_str = f"{n} RE: {t[5:16]}"
        else:
            date_range_str = all_ranges_list[0]['formatted'] if all_ranges_list else f"ALL RE: {global_time[5:16]}"
        
        # 构建时间过滤条件
        params = []
        has_specific = any(k != 'GLOBAL' for k in valid_times.keys())
        
        if has_specific:
            case_sql = "CASE l.device_id "
            for dev_id, t_str in valid_times.items():
                if dev_id != 'GLOBAL':
                    case_sql += "WHEN ? THEN ? "
                    params.extend([dev_id, t_str])
            case_sql += "ELSE ? END"
            params.append(global_time)
            time_filter = f"l.log_time >= {case_sql}"
        else:
            time_filter = "l.log_time >= ?"
            params.append(global_time)
        
        if device_filter != 'ALL':
            time_filter += " AND l.device_id = ?"
            params.append(device_filter)
        
        # 查询统计数据
        c.execute(f'''
            SELECT 
                COUNT(DISTINCT l.nickname) as total_users,
                SUM(CASE WHEN l.item_type IN ('钻石', '动态') THEN l.quantity ELSE 0 END) as total_wins,
                SUM(CASE WHEN l.item_type NOT IN ('钻石', '动态') THEN l.quantity ELSE 0 END) as total_physical_wins
            FROM logs l WHERE {time_filter}
        ''', params)
        stats_row = c.fetchone()
        
        # 查询排行榜
        c.execute(f'''
            SELECT 
                l.nickname, 
                COALESCE(d.nickname, '未知节点') as node_name, 
                l.device_id, 
                COUNT(*) as win_times, 
                SUM(CASE WHEN l.item_type IN ('钻石', '动态') THEN l.quantity ELSE 0 END) as win_sum
            FROM logs l 
            LEFT JOIN devices d ON l.device_id = d.device_id
            WHERE {time_filter}
            GROUP BY l.nickname, l.device_id 
            ORDER BY win_sum DESC
        ''', params)
        rank_list = [dict(row) for row in c.fetchall()]
        
        # 查询详情列表
        c.execute(f'''
            SELECT 
                l.id, l.nickname, l.item_type, l.quantity, l.log_time, 
                COALESCE(d.nickname, '未知节点') as node_name, l.device_id 
            FROM logs l 
            LEFT JOIN devices d ON l.device_id = d.device_id
            WHERE {time_filter} 
            ORDER BY l.log_time DESC 
            LIMIT 5000
        ''', params)
        details_formatted = [dict(row) for row in c.fetchall()]
        
        if not details_formatted:
            date_range_str = "本轮暂无数据产出"
        
        # 查询历史数据
        c.execute('''
            SELECT 
                SUBSTR(log_time, 1, 10) as date, 
                COUNT(DISTINCT nickname) as user_count, 
                SUM(CASE WHEN item_type IN ('钻石', '动态') THEN quantity ELSE 0 END) as daily_sum
            FROM logs 
            GROUP BY SUBSTR(log_time, 1, 10) 
            ORDER BY date DESC
        ''')
        history_list = [
            {
                "date": row['date'],
                "user_count": row['user_count'],
                "daily_sum": row['daily_sum'] or 0,
                "is_manual": False,
                "sort_key": row['date']
            }
            for row in c.fetchall()
        ]
        
    except Exception as e:
        print(f"[Stats DB Error] 大屏统计计算严重错误: {e}")
        return jsonify({"status": Message.Common.ERROR, "message": str(e)}), 500
    
    return jsonify({
        "status": Message.Common.SUCCESS,
        "date_range": date_range_str,
        "all_ranges": [r['formatted'] for r in all_ranges_list],
        "total_users": stats_row['total_users'] or 0 if stats_row else 0,
        "total_wins": stats_row['total_wins'] or 0 if stats_row else 0,
        "total_physical_wins": stats_row['total_physical_wins'] or 0 if stats_row else 0,
        "rank_list": rank_list,
        "details": details_formatted,
        "history": history_list,
        "unparsed_count": unparsed_count,
        "unparsed_sample": latest_unparsed_sample
    })


@stats_bp.route('/api/reset_round', methods=['POST'])
@login_required
def reset_round():
    """重置轮次"""
    data = request.json or {}
    device_id = data.get('device_id', 'ALL')
    custom_date = data.get('date')
    
    conn = get_lp_db()
    c = conn.cursor()
    
    try:
        if custom_date:
            now_str = custom_date.replace('T', ' ')
            if len(now_str) == 16:
                now_str += ':00'
        else:
            if device_id == 'ALL' or not device_id:
                c.execute("SELECT MAX(log_time) as max_t FROM logs")
            else:
                c.execute("SELECT MAX(log_time) as max_t FROM logs WHERE device_id = ?", (device_id,))
            max_row = c.fetchone()
            
            if max_row and max_row['max_t']:
                dt = datetime.strptime(max_row['max_t'], '%Y-%m-%d %H:%M:%S')
                dt += timedelta(seconds=1)
                now_str = dt.strftime('%Y-%m-%d %H:%M:%S')
            else:
                now_str = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    except Exception:
        now_str = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    current_times = get_round_times()
    
    if device_id == 'ALL' or not device_id:
        reset_all_to_global(now_str)
    else:
        update_round_time(device_id, now_str)
    
    return jsonify({"status": Message.Common.SUCCESS, "round_start_time": now_str})


@stats_bp.route('/api/logs/<int:log_id>', methods=['PUT'])
@login_required
def update_single_log(log_id):
    """更新单条日志"""
    data = request.json
    new_quantity = data.get('quantity')
    
    conn = get_lp_db()
    c = conn.cursor()
    
    try:
        c.execute("UPDATE logs SET quantity = ? WHERE id = ?", (new_quantity, log_id))
        conn.commit()
        return jsonify({"status": Message.Common.SUCCESS})
    except Exception as e:
        return jsonify({"status": Message.Common.ERROR, "msg": str(e)}), 500


@stats_bp.route('/api/nodes_online', methods=['GET'])
@login_required
def get_nodes_online():
    """获取在线节点列表"""
    if not session.get('logged_in'):
        return jsonify({"status": Message.Common.ERROR, "message": "需要登录"}), 401
    
    conn = get_lp_db()
    c = conn.cursor()
    c.execute("SELECT * FROM devices ORDER BY first_seen ASC")
    rows = c.fetchall()
    
    nodes = []
    now = time.time()
    for r in rows:
        nodes.append({
            "device_id": r['device_id'],
            "nickname": r['nickname'],
            "is_online": (now - r['last_seen']) < 15,
            "process_running": bool(r['process_running'])
        })
    
    return jsonify({"nodes": nodes})

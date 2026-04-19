"""设置管理路由

处理系统设置、物品分组、Bark配置等
"""
import json
from datetime import datetime
from flask import Blueprint, request, jsonify
import requests
import urllib.parse

from .auth import login_required
from extensions import db
from models import Settings, Item, Record
from services.parser import process_unparsed_logs
from constants import Message, Defaults

settings_bp = Blueprint('settings', __name__)


@settings_bp.route('/api/settings', methods=['POST'])
@login_required
def save_settings():
    """保存设置
    
    支持多种操作:
    - add_item: 添加物品分组
    - edit_item: 编辑物品分组
    - delete_item: 删除物品分组
    - update_interval: 更新间隔时间
    - update_bark: 更新Bark配置
    - update_faq: 更新FAQ
    - save_parsers: 保存解析器配置
    - reorder_items: 重排物品顺序
    """
    try:
        data = request.json or {}
        action = data.get('action')
        
        # 安全读取配置
        settings = Settings.query.first()
        if not settings:
            settings = Settings(parsers_json="[]")
            db.session.add(settings)
        
        if action == 'add_item':
            name = data.get('name')
            if name and not Item.query.filter_by(name=name).first():
                max_order = db.session.query(db.func.max(Item.sort_order)).scalar() or 0
                db.session.add(Item(name=name, sort_order=max_order + 1))
                
        elif action == 'edit_item':
            item = Item.query.get(data.get('id'))
            new_name = data.get('name')
            if item and new_name and item.name != new_name:
                if not Item.query.filter_by(name=new_name).first():
                    old_name = item.name
                    item.name = new_name
                    # 更新关联记录
                    for r in Record.query.all():
                        if r.data and old_name in r.data:
                            new_data = dict(r.data)
                            new_data[new_name] = new_data.pop(old_name)
                            r.data = new_data
                            
        elif action == 'delete_item':
            item = Item.query.get(data.get('id'))
            if item:
                db.session.delete(item)
                
        elif action == 'update_interval':
            settings.interval_hours = int(data.get('interval_hours', Defaults.INTERVAL_HOURS))
            
        elif action == 'update_bark':
            settings.bark_enabled = data.get('bark_enabled', False)
            settings.bark_url = data.get('bark_url', '')
            settings.bark_title = data.get('bark_title', Defaults.BARK_TITLE)
            settings.bark_body = data.get('bark_body', Defaults.BARK_BODY)
            settings.bark_icon = data.get('bark_icon', '')
            settings.bark_notify_physical = data.get('bark_notify_physical', False)
            settings.bark_physical_title = data.get('bark_physical_title', Defaults.BARK_PHYSICAL_TITLE)
            settings.bark_physical_body = data.get('bark_physical_body', Defaults.BARK_PHYSICAL_BODY)
            
        elif action == 'update_faq':
            settings.faq_json = json.dumps(data.get('faq_list', []), ensure_ascii=False)
            
        elif action == 'save_parsers':
            parsers_data = data.get('parsers_json', [])
            settings.parsers_json = json.dumps(parsers_data, ensure_ascii=False)
            db.session.commit()
            try:
                process_unparsed_logs(parsers_data, settings)
            except Exception as e:
                print(f"[Parser Update Error] 隔离区重新解析失败: {e}")
            return jsonify({'success': True})
            
        elif action == 'reorder_items':
            ids = data.get('ids', [])
            for index, item_id in enumerate(ids):
                item = Item.query.get(item_id)
                if item:
                    item.sort_order = index
        
        db.session.commit()
        return jsonify({'success': True})
        
    except Exception as e:
        db.session.rollback()
        print(f"[Settings API Error] 保存失败: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500


@settings_bp.route('/api/test_bark', methods=['POST'])
@login_required
def test_bark():
    """测试Bark通知"""
    data = request.json
    url = data.get('bark_url')
    
    if not url:
        return jsonify({'error': '请先填写 Bark URL'}), 400
    
    base_url = url.rstrip('/')
    raw_title = data.get('bark_title', '测试').replace("{group}", "通道测试").replace("{time}", datetime.now().strftime('%H:%M'))
    raw_body = data.get('bark_body', '成功连通！').replace("{group}", "通道测试").replace("{time}", datetime.now().strftime('%H:%M'))
    
    t_enc = urllib.parse.quote(raw_title, safe='')
    b_enc = urllib.parse.quote(raw_body, safe='')
    api_url = f"{base_url}/{t_enc}/{b_enc}"
    
    params = {
        "sound": "minuet",
        "group": "MatrixPilot",
        "isArchive": "1"
    }
    
    icon = data.get('bark_icon')
    if icon:
        params["icon"] = icon
    
    try:
        r = requests.get(api_url, params=params, timeout=5)
        if r.status_code == 200:
            return jsonify({'msg': '测试推送成功，请查看手机！'})
        return jsonify({'error': f'接口拒绝请求 (HTTP {r.status_code})'}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 400

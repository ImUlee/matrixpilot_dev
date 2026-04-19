"""文件上传路由

处理日志文件上传、解析、客户端文件管理等
"""
import os
import re
import time
import json
from datetime import datetime
from flask import Blueprint, request, jsonify, send_from_directory

from .auth import login_required
from extensions import db
from models import Settings
from config import Config
from services.db_utils import get_lp_db, update_device_status
from services.parser import parse_file_content
from services.notification import trigger_physical_notifications
from constants import Message

upload_bp = Blueprint('upload', __name__)


@upload_bp.route('/upload', methods=['POST'])
def upload_file():
    """上传日志文件
    
    接收客户端上传的日志文件，解析并存储
    """
    file = request.files.get('file')
    device_id = request.form.get('device_id')
    nickname = request.form.get('nickname', 'Unknown')
    process_running = 1 if request.form.get('process_running', 'False') == 'True' else 0
    
    if not file or not device_id:
        return jsonify({"status": Message.Common.ERROR}), 400
    
    # 更新设备状态
    update_device_status(device_id, nickname, process_running)
    
    conn = get_lp_db()
    c = conn.cursor()
    
    # 获取解析器配置
    settings = Settings.query.first()
    all_parsers = []
    if settings and settings.parsers_json:
        try:
            all_parsers = json.loads(settings.parsers_json)
        except Exception as e:
            print(f"[Parser Error] JSON解析失败: {e}")
    
    # 读取文件内容
    raw_data = file.read()
    try:
        content = raw_data.decode('gb18030')
    except:
        content = raw_data.decode('utf-8', errors='ignore')
    lines = content.split('\n')
    
    # 无解析器时存入隔离区
    if not all_parsers:
        c.execute(
            "UPDATE devices SET last_msg = '格式未识别' WHERE device_id = ?", 
            (device_id,)
        )
        c.execute(
            "INSERT INTO unparsed_logs (device_id, raw_content, add_time) VALUES (?, ?, ?)",
            (device_id, content, time.time())
        )
        conn.commit()
        return jsonify({
            "status": Message.Common.SUCCESS, 
            "msg": "已存入云端隔离区等待新规则解析"
        })
    
    # 解析文件
    new_count, matched_any, new_physicals = parse_file_content(lines, all_parsers, device_id, c)
    
    # 无匹配时检查是否需要存入隔离区
    if not matched_any:
        has_data_signature = any('----' in l or re.search(r'\d', l) for l in lines[:50])
        if has_data_signature:
            c.execute(
                "UPDATE devices SET last_msg = '格式未识别' WHERE device_id = ?", 
                (device_id,)
            )
            c.execute(
                "INSERT INTO unparsed_logs (device_id, raw_content, add_time) VALUES (?, ?, ?)",
                (device_id, content, time.time())
            )
            conn.commit()
            return jsonify({
                "status": Message.Common.SUCCESS, 
                "msg": "已存入云端隔离区等待新规则解析"
            })
    
    # 更新设备状态
    if matched_any:
        c.execute("UPDATE devices SET last_msg = '正常' WHERE device_id = ?", (device_id,))
    
    conn.commit()
    
    # 触发实物通知
    trigger_physical_notifications(new_physicals, settings)
    
    return jsonify({
        "status": Message.Common.SUCCESS, 
        "new_entries": new_count
    })


@upload_bp.route('/api/client_files')
@login_required
def list_client_files():
    """获取客户端文件列表"""
    try:
        files = []
        for filename in os.listdir(Config.FILE_DIRECTORY):
            path = os.path.join(Config.FILE_DIRECTORY, filename)
            if os.path.isfile(path):
                stats = os.stat(path)
                files.append({
                    "name": filename,
                    "size": f"{round(stats.st_size / (1024 * 1024), 2)} MB",
                    "mtime": datetime.fromtimestamp(stats.st_mtime).strftime('%Y-%m-%d %H:%M')
                })
        files.sort(key=lambda x: x['mtime'], reverse=True)
        return jsonify({"status": Message.Common.SUCCESS, "files": files})
    except Exception as e:
        return jsonify({"status": Message.Common.ERROR, "message": str(e)}), 500


@upload_bp.route('/download/client/<filename>')
@login_required
def download_client_file(filename):
    """下载客户端文件"""
    return send_from_directory(Config.FILE_DIRECTORY, filename, as_attachment=True)

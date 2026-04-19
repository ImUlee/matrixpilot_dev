"""记录管理路由

处理MatrixPilot主记录的CRUD操作
"""
from datetime import datetime, timedelta
from flask import Blueprint, request, jsonify

from .auth import login_required
from extensions import db
from models import Record, Settings

records_bp = Blueprint('records', __name__)


@records_bp.route('/api/record', methods=['POST'])
@login_required
def add_record():
    """添加新记录
    
    创建新的轮次记录，自动计算下次预计时间
    """
    data = request.json
    settings = Settings.query.first()
    
    date_str = data.get('date', '').replace('T', ' ')
    dt_obj = datetime.strptime(date_str, '%Y-%m-%d %H:%M')
    
    interval = settings.interval_hours if settings else 72
    next_dt = dt_obj + timedelta(hours=interval)
    
    new_record = Record(
        date=date_str, 
        next_time=next_dt.strftime('%Y-%m-%d %H:%M'), 
        data={data.get('group'): data.get('quantity')}, 
        notified=False
    )
    
    db.session.add(new_record)
    db.session.commit()
    
    return jsonify({'success': True})


@records_bp.route('/api/record/<int:id>', methods=['PUT', 'DELETE'])
@login_required
def modify_record(id):
    """修改或删除记录
    
    PUT: 更新记录信息
    DELETE: 删除记录
    """
    record = Record.query.get_or_404(id)
    
    if request.method == 'DELETE':
        db.session.delete(record)
    elif request.method == 'PUT':
        data = request.json
        settings = Settings.query.first()
        
        new_date = data.get('date', '').replace('T', ' ')
        record.date = new_date
        
        interval = settings.interval_hours if settings else 72
        record.next_time = (
            datetime.strptime(new_date, '%Y-%m-%d %H:%M') + 
            timedelta(hours=interval)
        ).strftime('%Y-%m-%d %H:%M')
        
        record.notified = False
        old_key = list(record.data.keys())[0]
        record.data = {old_key: data.get('value')}
    
    db.session.commit()
    return jsonify({'success': True})

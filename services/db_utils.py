"""
数据库工具模块

提供数据库初始化、连接管理、表结构自愈等功能
"""
import sqlite3
import time
from typing import Dict, Any
from flask import g
from sqlalchemy import event
from sqlalchemy.engine import Engine

from extensions import db
from models import Settings
from config import Config
from constants import DeviceStatus, Defaults


# ============================================================
# SQLite性能优化配置
# ============================================================
@event.listens_for(Engine, "connect")
def set_sqlite_pragma(dbapi_connection, connection_record):
    """为SQLAlchemy连接注入高并发PRAGMA配置
    
    自动应用于所有SQLite连接，提升并发性能
    """
    if type(dbapi_connection) is sqlite3.Connection:
        cursor = dbapi_connection.cursor()
        cursor.execute("PRAGMA journal_mode=WAL")      # 预写日志，解决读写互斥
        cursor.execute("PRAGMA synchronous=NORMAL")    # 配合WAL提升写入性能
        cursor.execute("PRAGMA cache_size=-64000")     # 64MB内存缓存
        cursor.execute("PRAGMA busy_timeout=15000")    # 15秒锁等待
        cursor.execute("PRAGMA temp_store=MEMORY")     # 临时表放内存
        cursor.close()


def _apply_pragma_for_connection(conn: sqlite3.Connection) -> None:
    """为原生SQLite连接应用性能优化
    
    Args:
        conn: SQLite连接对象
    """
    conn.execute('PRAGMA journal_mode=WAL')
    conn.execute('PRAGMA synchronous=NORMAL')
    conn.execute('PRAGMA cache_size=-64000')
    conn.execute('PRAGMA busy_timeout=15000')
    conn.execute('PRAGMA temp_store=MEMORY')


# ============================================================
# 表结构自愈工具
# ============================================================
def ensure_columns(
    cursor: sqlite3.Cursor, 
    table_name: str, 
    columns_dict: Dict[str, str]
) -> None:
    """安全地添加表字段（幂等操作）
    
    检查表结构，自动添加缺失的字段
    
    Args:
        cursor: 数据库游标
        table_name: 表名
        columns_dict: 字段定义字典 {字段名: 字段类型定义}
    """
    cursor.execute(f"PRAGMA table_info({table_name})")
    rows = cursor.fetchall()
    
    # 提取已有字段名
    existing_cols = set()
    for row in rows:
        col_name = row[1] if isinstance(row, tuple) else row['name']
        existing_cols.add(col_name)
    
    # 添加缺失字段
    for col_name, col_def in columns_dict.items():
        if col_name not in existing_cols:
            try:
                cursor.execute(
                    f"ALTER TABLE {table_name} ADD COLUMN {col_name} {col_def}"
                )
            except Exception as e:
                print(f"[DB Auto-Migrate] 字段 {col_name} 附加失败: {e}")


# ============================================================
# 数据库初始化
# ============================================================
def init_mp_db(app) -> None:
    """初始化MatrixPilot主数据库
    
    创建表结构，执行自愈迁移，插入默认数据
    
    Args:
        app: Flask应用实例
    """
    with app.app_context():
        # 创建所有表
        db.create_all()
        
        try:
            conn = db.engine.raw_connection()
            cursor = conn.cursor()
            
            # 自愈迁移：添加新字段
            ensure_columns(cursor, 'settings', {
                'bark_enabled': "BOOLEAN DEFAULT 0",
                'bark_title': f"VARCHAR(100) DEFAULT '{Defaults.BARK_TITLE}'",
                'bark_body': f"VARCHAR(255) DEFAULT '{Defaults.BARK_BODY}'",
                'bark_icon': "VARCHAR(255) DEFAULT ''",
                'bark_notify_physical': "BOOLEAN DEFAULT 0",
                'bark_physical_title': f"VARCHAR(100) DEFAULT '{Defaults.BARK_PHYSICAL_TITLE}'",
                'bark_physical_body': f"VARCHAR(255) DEFAULT '{Defaults.BARK_PHYSICAL_BODY}'",
                'faq_json': "TEXT",
                'parsers_json': "TEXT DEFAULT '[]'"
            })
            ensure_columns(cursor, 'record', {'notified': "BOOLEAN DEFAULT 0"})
            ensure_columns(cursor, 'item', {'sort_order': "INTEGER DEFAULT 0"})
            
            conn.commit()
            cursor.close()
        except Exception as e:
            print(f"[DB Init Error] MatrixPilot 数据库热更新异常: {e}")
        
        # 确保存在默认设置
        if not Settings.query.first():
            db.session.add(Settings(parsers_json="[]"))
            db.session.commit()


def init_lp_db() -> None:
    """初始化LittlePilot日志数据库
    
    创建日志表、设备表、未解析日志表等
    """
    conn = sqlite3.connect(Config.LP_DB_PATH, timeout=15)
    conn.row_factory = sqlite3.Row
    _apply_pragma_for_connection(conn)
    
    cursor = conn.cursor()
    
    # 创建索引
    cursor.execute(
        'CREATE INDEX IF NOT EXISTS idx_logs_time_dev ON logs(log_time, device_id)'
    )
    cursor.execute(
        'CREATE INDEX IF NOT EXISTS idx_logs_nickname ON logs(nickname)'
    )
    
    # 创建设备表
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS devices (
            device_id TEXT PRIMARY KEY, 
            nickname TEXT, 
            last_seen REAL, 
            process_running INTEGER, 
            first_seen REAL
        )
    ''')
    
    # 创建每日覆盖表
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS daily_overrides (
            date TEXT, 
            device_id TEXT, 
            manual_users INTEGER, 
            manual_sum INTEGER, 
            PRIMARY KEY (date, device_id)
        )
    ''')
    
    # 创建未解析日志表
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS unparsed_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT, 
            device_id TEXT, 
            raw_content TEXT, 
            add_time REAL
        )
    ''')
    
    # 自愈迁移
    ensure_columns(cursor, 'devices', {
        'template_id': "TEXT DEFAULT ''",
        'last_msg': f"TEXT DEFAULT '{DeviceStatus.NORMAL.value}'",
        'detected_template': "TEXT DEFAULT ''"
    })
    ensure_columns(cursor, 'logs', {'template_id': "TEXT DEFAULT 'default'"})
    
    # 修复旧表主键结构（如果需要）
    cursor.execute("PRAGMA table_info(daily_overrides)")
    columns = [col['name'] for col in cursor.fetchall()]
    
    if 'template_id' not in columns:
        # 重建表结构
        cursor.execute("ALTER TABLE daily_overrides RENAME TO daily_overrides_old")
        cursor.execute('''
            CREATE TABLE daily_overrides (
                date TEXT, 
                device_id TEXT, 
                manual_users INTEGER, 
                manual_sum INTEGER, 
                PRIMARY KEY (date, device_id)
            )
        ''')
        try:
            cursor.execute('''
                INSERT OR IGNORE INTO daily_overrides 
                (date, device_id, manual_users, manual_sum) 
                SELECT date, device_id, MAX(manual_users), MAX(manual_sum) 
                FROM daily_overrides_old 
                GROUP BY date, device_id
            ''')
        except Exception:
            pass
        cursor.execute("DROP TABLE IF EXISTS daily_overrides_old")
    
    conn.commit()
    conn.close()


# ============================================================
# 连接管理
# ============================================================
def get_lp_db() -> sqlite3.Connection:
    """获取LittlePilot数据库连接
    
    连接挂载在Flask请求上下文，请求结束自动关闭
    
    Returns:
        SQLite连接对象
    """
    if 'lp_db' not in g:
        g.lp_db = sqlite3.connect(Config.LP_DB_PATH, timeout=15)
        g.lp_db.row_factory = sqlite3.Row
        _apply_pragma_for_connection(g.lp_db)
    return g.lp_db


def update_device_status(
    device_id: str, 
    nickname: str, 
    process_running: int
) -> None:
    """更新设备心跳状态
    
    插入或更新设备记录，记录心跳时间
    
    Args:
        device_id: 设备唯一标识
        nickname: 设备昵称
        process_running: 进程是否运行 (0/1)
    """
    conn = get_lp_db()
    cursor = conn.cursor()
    now = time.time()
    
    cursor.execute('''
        INSERT INTO devices 
        (device_id, nickname, last_seen, process_running, first_seen, 
         template_id, last_msg, detected_template) 
        VALUES (?, ?, ?, ?, ?, 'default', ?, '')
        ON CONFLICT(device_id) DO UPDATE SET 
        nickname=excluded.nickname, 
        last_seen=excluded.last_seen, 
        process_running=excluded.process_running
    ''', (
        device_id, nickname, now, process_running, now,
        DeviceStatus.NORMAL.value
    ))
    
    conn.commit()

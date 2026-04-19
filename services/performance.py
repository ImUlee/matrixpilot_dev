"""性能优化模块

提供数据库索引优化、查询缓存等功能
"""
import sqlite3
from typing import List, Tuple
from flask import current_app


def create_optimized_indexes(conn: sqlite3.Connection) -> List[str]:
    """创建优化的数据库索引
    
    为常用查询添加复合索引，提升查询性能
    
    Args:
        conn: SQLite数据库连接
        
    Returns:
        创建的索引列表
    """
    indexes = [
        # logs表索引 - 按时间查询
        ("idx_logs_log_time", "logs(log_time DESC)"),
        
        # logs表索引 - 按昵称和时间查询（复合索引）
        ("idx_logs_nickname_time", "logs(nickname COLLATE NOCASE, log_time DESC)"),
        
        # logs表索引 - 按设备ID和时间查询
        ("idx_logs_device_time", "logs(device_id, log_time DESC)"),
        
        # logs表索引 - 按物品类型统计
        ("idx_logs_item_type", "logs(item_type)"),
        
        # devices表索引 - 按设备ID查询昵称
        ("idx_devices_device_id", "devices(device_id)"),
    ]
    
    created = []
    cursor = conn.cursor()
    
    for idx_name, idx_def in indexes:
        try:
            cursor.execute(f"CREATE INDEX IF NOT EXISTS {idx_name} ON {idx_def}")
            created.append(idx_name)
        except sqlite3.Error as e:
            current_app.logger.warning(f"创建索引失败 {idx_name}: {e}")
    
    conn.commit()
    return created


def analyze_query_performance(conn: sqlite3.Connection, query: str) -> dict:
    """分析查询性能
    
    使用EXPLAIN QUERY ANALYZE分析查询执行计划
    
    Args:
        conn: 数据库连接
        query: 要分析的SQL查询
        
    Returns:
        包含分析结果的字典
    """
    cursor = conn.cursor()
    
    # 获取查询计划
    cursor.execute(f"EXPLAIN QUERY PLAN {query}")
    plan = cursor.fetchall()
    
    return {
        "query": query,
        "plan": [str(row) for row in plan],
        "uses_index": any("INDEX" in str(row) for row in plan),
        "uses_scan": any("SCAN" in str(row) for row in plan)
    }


def get_table_stats(conn: sqlite3.Connection, table_name: str) -> dict:
    """获取表统计信息
    
    Args:
        conn: 数据库连接
        table_name: 表名
        
    Returns:
        表统计信息字典
    """
    cursor = conn.cursor()
    
    # 记录数
    cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
    row_count = cursor.fetchone()[0]
    
    # 表大小（页数）
    cursor.execute(f"SELECT COUNT(*) FROM dbstat WHERE name=?", (table_name,))
    pages = cursor.fetchone()[0] if cursor.fetchall() else 0
    
    return {
        "table": table_name,
        "row_count": row_count,
        "pages": pages
    }


def vacuum_database(conn: sqlite3.Connection) -> None:
    """整理数据库碎片
    
    执行VACUUM操作，回收空间，优化性能
    """
    conn.execute("VACUUM")
    conn.commit()


def optimize_database(conn: sqlite3.Connection) -> dict:
    """执行完整的数据库优化
    
    Args:
        conn: 数据库连接
        
    Returns:
        优化结果字典
    """
    results = {
        "indexes_created": [],
        "vacuum_executed": False
    }
    
    # 创建索引
    results["indexes_created"] = create_optimized_indexes(conn)
    
    # 分析统计信息
    conn.execute("ANALYZE")
    conn.commit()
    results["analyze_executed"] = True
    
    return results

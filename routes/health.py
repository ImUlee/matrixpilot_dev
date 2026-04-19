"""健康检查路由

提供服务状态检查和静态资源
"""
import time
import sqlite3
from flask import Blueprint, jsonify, send_from_directory, current_app

from extensions import cache

health_bp = Blueprint('health', __name__)


@health_bp.route('/sw.js')
def serve_sw():
    """Service Worker
    
    返回PWA的Service Worker脚本
    """
    return send_from_directory(
        current_app.static_folder, 
        'sw.js', 
        mimetype='application/javascript'
    )


@health_bp.route('/health')
@health_bp.route('/api/health', methods=['GET'])
def health_check():
    """健康检查接口
    
    用于负载均衡器或监控系统检测服务状态
    
    Returns:
        JSON响应，包含状态信息
    """
    return jsonify({
        "status": "ok", 
        "message": "MatrixPilot Gateway is running.",
        "timestamp": time.time()
    })


@health_bp.route('/health/detailed')
def detailed_health():
    """详细健康检查
    
    返回数据库、缓存等组件状态
    """
    start_time = time.time()
    
    # 检查缓存
    cache_status = "healthy"
    cache_latency = 0
    try:
        cache_start = time.time()
        cache.set("health_check", "ok", timeout=10)
        result = cache.get("health_check")
        cache_latency = round((time.time() - cache_start) * 1000, 2)
        if result != "ok":
            cache_status = "error: cache read/write mismatch"
    except Exception as e:
        cache_status = f"error: {str(e)}"
    
    # 检查SQLite数据库
    lp_db_status = "healthy"
    lp_db_size = 0
    try:
        import os
        from config import Config
        if os.path.exists(Config.LP_DB_PATH):
            lp_db_size = os.path.getsize(Config.LP_DB_PATH)
            conn = sqlite3.connect(Config.LP_DB_PATH)
            conn.execute("SELECT 1")
            conn.close()
    except Exception as e:
        lp_db_status = f"error: {str(e)}"
    
    total_latency = round((time.time() - start_time) * 1000, 2)
    
    return jsonify({
        "status": "healthy" if cache_status == "healthy" else "degraded",
        "timestamp": time.time(),
        "latency_ms": total_latency,
        "components": {
            "cache": {
                "status": cache_status,
                "latency_ms": cache_latency
            },
            "lp_database": {
                "status": lp_db_status,
                "size_kb": round(lp_db_size / 1024, 2)
            }
        }
    })


@health_bp.route('/health/metrics')
def performance_metrics():
    """性能指标
    
    返回应用性能统计数据
    """
    from services.db_utils import get_lp_db
    
    metrics = {
        "database": {},
        "cache": {}
    }
    
    # 数据库统计
    try:
        conn = get_lp_db()
        c = conn.cursor()
        
        # 日志数量
        c.execute("SELECT COUNT(*) FROM logs")
        metrics["database"]["logs_count"] = c.fetchone()[0]
        
        # 设备数量
        c.execute("SELECT COUNT(*) FROM devices")
        metrics["database"]["devices_count"] = c.fetchone()[0]
        
        # 用户数量
        c.execute("SELECT COUNT(DISTINCT nickname) FROM logs")
        metrics["database"]["unique_users"] = c.fetchone()[0]
        
    except Exception as e:
        metrics["database"]["error"] = str(e)
    
    # 缓存统计
    try:
        cache.set("metrics_test", 1, timeout=10)
        metrics["cache"]["working"] = cache.get("metrics_test") == 1
    except Exception as e:
        metrics["cache"]["error"] = str(e)
    
    return jsonify(metrics)

"""
MatrixPilot 启动自检模块

在服务启动前验证所有组件是否正常
"""
import os
import sqlite3
from pathlib import Path


def run_self_check():
    """运行自检，返回 (是否通过, 错误信息列表)"""
    errors = []
    
    print("=" * 50)
    print("🔍 MatrixPilot 自检中...")
    print("=" * 50)
    
    # 1. 检查应用目录
    app_dir = Path(__file__).parent
    print(f"✅ 应用目录: {app_dir}")
    
    # 2. 检查关键目录和文件
    required_paths = {
        'static': app_dir / 'static',
        'templates': app_dir / 'templates',
        'routes': app_dir / 'routes',
        'services': app_dir / 'services',
        'config.py': app_dir / 'config.py',
        'app.py': app_dir / 'app.py',
        'extensions.py': app_dir / 'extensions.py',
    }
    
    for name, path in required_paths.items():
        if path.exists():
            print(f"✅ {name}: {path}")
        else:
            errors.append(f"❌ 缺失: {name} -> {path}")
    
    # 3. 检查静态文件
    static_dist = app_dir / 'static' / 'dist'
    if static_dist.exists():
        print(f"✅ 静态文件目录: {static_dist}")
        
        # 检查 index.html
        index_html = static_dist / 'index.html'
        if index_html.exists():
            print(f"✅ index.html 存在 ({index_html.stat().st_size} bytes)")
        else:
            errors.append(f"❌ 缺失 index.html")
        
        # 检查 assets 目录
        assets_dir = static_dist / 'assets'
        if assets_dir.exists():
            js_files = list(assets_dir.glob('*.js'))
            css_files = list(assets_dir.glob('*.css'))
            print(f"✅ 静态资源: {len(js_files)} JS, {len(css_files)} CSS")
            
            if not js_files:
                errors.append("❌ 没有找到 JS 文件")
            if not css_files:
                errors.append("❌ 没有找到 CSS 文件")
        else:
            errors.append(f"❌ 缺失 assets 目录")
    else:
        errors.append(f"❌ 缺失 static/dist 目录")
    
    # 4. 检查数据库目录
    db_dir = app_dir / 'db'
    if not db_dir.exists():
        try:
            db_dir.mkdir(parents=True, exist_ok=True)
            print(f"✅ 创建数据库目录: {db_dir}")
        except Exception as e:
            errors.append(f"❌ 无法创建数据库目录: {e}")
    
    # 5. 检查环境配置
    env_file = app_dir / '.env'
    if env_file.exists():
        print(f"✅ .env 文件存在")
    else:
        print(f"⚠️  .env 文件不存在 (可选)")
    
    # 6. 尝试初始化数据库（如果存在）
    lp_db_path = app_dir / 'db' / 'lp_logs.db'
    mp_db_path = app_dir / 'db' / 'matrixpilot.db'
    
    for db_path in [lp_db_path, mp_db_path]:
        if db_path.exists():
            try:
                conn = sqlite3.connect(str(db_path))
                conn.execute("SELECT 1").fetchone()
                conn.close()
                print(f"✅ 数据库正常: {db_path.name}")
            except Exception as e:
                errors.append(f"❌ 数据库错误 {db_path.name}: {e}")
    
    # 7. 检查端口可用性
    import socket
    test_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    port_available = test_socket.connect_ex(('127.0.0.1', 5000)) != 0
    test_socket.close()
    
    if port_available:
        print(f"✅ 端口 5000 可用")
    else:
        print(f"⚠️  端口 5000 已被占用")
    
    # 总结
    print("=" * 50)
    if errors:
        print("❌ 自检未通过，以下问题需要处理:")
        for error in errors:
            print(f"   {error}")
    else:
        print("✅ 自检通过！所有组件正常")
    print("=" * 50)
    
    return len(errors) == 0, errors


def require_self_check():
    """强制自检，如果失败则退出程序"""
    passed, errors = run_self_check()
    if not passed:
        print("\n❌ 启动失败！请修复上述问题后重试。")
        import sys
        sys.exit(1)


if __name__ == '__main__':
    # 直接运行此文件进行测试
    run_self_check()

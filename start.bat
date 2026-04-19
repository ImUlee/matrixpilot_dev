@echo off
echo ========================================
echo MatrixPilot 生产环境启动
echo ========================================
echo.

REM 检查Python
python --version >nul 2>&1
if errorlevel 1 (
    echo [错误] 未找到Python，请先安装Python 3.10+
    pause
    exit /b 1
)

REM 检查依赖
echo [1/3] 检查依赖...
pip show flask >nul 2>&1
if errorlevel 1 (
    echo [安装] 正在安装依赖...
    pip install -r requirements.txt -q
)

REM 检查.env文件
if not exist .env (
    echo [警告] 未找到.env配置文件
    echo 请复制.env.example并配置
    pause
    exit /b 1
)

REM 启动应用
echo [2/3] 启动应用...
echo [3/3] 访问地址: http://localhost:5000
echo.
python app.py

pause

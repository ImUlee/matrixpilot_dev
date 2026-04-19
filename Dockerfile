# MatrixPilot - 生产环境 Dockerfile
# 多阶段构建，优化镜像大小

# ============================================
# Stage 1: 前端构建
# ============================================
FROM node:20-alpine AS frontend-builder

WORKDIR /app/frontend

# 复制前端依赖文件
COPY frontend/package*.json ./

# 安装依赖
RUN npm ci

# 复制前端源码
COPY frontend/ ./

# 构建
RUN npm run build

# ============================================
# Stage 2: Python 运行环境
# ============================================
FROM python:3.11-slim

# 设置环境变量
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

# 安装系统依赖
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# 创建非root用户
RUN useradd --create-home --shell /bin/bash app

WORKDIR /app

# 复制依赖文件
COPY requirements.txt ./

# 安装Python依赖
RUN pip install --no-cache-dir -r requirements.txt \
    && pip install gunicorn

# 复制应用代码
COPY --chown=app:app . .

# 复制前端构建产物
COPY --from=frontend-builder --chown=app:app /app/static/dist ./static/dist

# 创建必要目录
RUN mkdir -p db logs file \
    && chown -R app:app db logs file

# 切换到非root用户
USER app

# 暴露端口
EXPOSE 5000

# 健康检查
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import requests; requests.get('http://localhost:5000/health')" || exit 1

# 启动命令
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "2", "--threads", "4", "app:app"]

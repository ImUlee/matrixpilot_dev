# MatrixPilot

一个简洁高效的日志管理与分析平台。

## 快速开始

### 使用 Docker Compose（推荐）

```bash
# 创建配置文件
cat > .env << EOF
APP_PIN=your_secure_pin_here
SECRET_KEY=your_random_secret_key_at_least_32_characters_long
API_KEY=your_api_key_here
TZ=Asia/Shanghai
EOF

# 启动服务
docker-compose up -d

# 查看日志
docker-compose logs -f
```

### 使用 Docker 命令

```bash
# 拉取镜像
docker pull leeone/matrixpilot:latest

# 运行容器
docker run -d \
  --name matrixpilot \
  -p 5000:5000 \
  -v matrixpilot_db:/app/db \
  -v matrixpilot_logs:/app/logs \
  -v matrixpilot_files:/app/file \
  --env-file .env \
  --restart unless-stopped \
  leeone/matrixpilot:latest
```

### 访问应用

浏览器打开：http://localhost:5000

## 环境变量

| 变量 | 说明 | 必填 |
|------|------|------|
| `APP_PIN` | 登录 PIN 码 | ✅ |
| `SECRET_KEY` | Flask 会话密钥（至少32位） | ✅ |
| `API_KEY` | API 认证密钥 | ✅ |
| `TZ` | 时区设置，默认 `Asia/Shanghai` | ❌ |

## 常用命令

```bash
# 启动服务
docker-compose up -d

# 停止服务
docker-compose down

# 重启服务
docker-compose restart

# 查看日志
docker-compose logs -f

# 重新构建并启动
docker-compose up -d --build
```

## 技术栈

- **后端**: Flask + SQLAlchemy
- **前端**: Vue.js 3 + Vite
- **数据库**: SQLite
- **容器化**: Docker

## License

MIT

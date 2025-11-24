# TrendRadar 部署指南

## 概述

TrendRadar 支持多种部署方式，从本地开发到生产环境都有相应的解决方案。本指南将详细介绍各种部署场景和最佳实践。

## 系统要求

### 最低要求
- **Python**: 3.10 或更高版本
- **内存**: 512MB 可用内存
- **存储**: 100MB 可用磁盘空间
- **网络**: 稳定的互联网连接

### 推荐配置
- **Python**: 3.11+
- **内存**: 2GB 可用内存
- **存储**: 1GB 可用磁盘空间
- **CPU**: 多核处理器（用于并发爬取）

## 快速开始

### 一键部署（推荐）

#### macOS/Linux
```bash
# 克隆项目
git clone https://github.com/sansan0/TrendRadar.git
cd TrendRadar

# 一键部署
./setup-mac.sh
```

#### Windows
```batch
# 克隆项目
git clone https://github.com/sansan0/TrendRadar.git
cd TrendRadar

# 一键部署（中文版）
setup-windows.bat

# 或使用英文版
setup-windows-en.bat
```

### 手动部署

#### 1. 安装UV包管理器

**macOS/Linux**:
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

**Windows**:
```powershell
powershell -ExecutionPolicy Bypass -Command "irm https://astral.sh/uv/install.ps1 | iex"
```

#### 2. 创建虚拟环境
```bash
uv sync
```

#### 3. 验证安装
```bash
# 检查MCP服务器
uv run python -m mcp_server.server --help

# 检查爬虫功能
uv run python main.py --help
```

## MCP服务器部署

### STDIO模式部署

STDIO模式适用于本地AI客户端连接，是推荐的部署方式。

#### 启动服务器
```bash
uv run python -m mcp_server.server
```

#### 客户端配置

**Cherry Studio**:
1. 打开设置 > MCP Servers > 添加服务器
2. 填入以下配置：
   ```
   名称: TrendRadar
   描述: 新闻热点聚合分析工具
   类型: STDIO
   命令: uv
   参数:
     --directory /path/to/TrendRadar
     run
     python
     -m
     mcp_server.server
   ```

**Claude Desktop**:
编辑 `~/.claude_desktop_config.json`:
```json
{
  "mcpServers": {
    "trendradar": {
      "command": "uv",
      "args": [
        "--directory", "/path/to/TrendRadar",
        "run", "python", "-m", "mcp_server.server"
      ]
    }
  }
}
```

### HTTP模式部署

HTTP模式适用于远程访问和多客户端共享。

#### 启动HTTP服务器
```bash
# 基本启动
uv run python -m mcp_server.server --transport http --port 3333

# 或使用便捷脚本
./start-http.sh  # Linux/macOS
start-http.bat   # Windows
```

#### Nginx反向代理配置

创建 `/etc/nginx/sites-available/trendradar`:
```nginx
server {
    listen 80;
    server_name your-domain.com;

    location /mcp {
        proxy_pass http://localhost:3333;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_cache_bypass $http_upgrade;
    }
}
```

启用站点：
```bash
sudo ln -s /etc/nginx/sites-available/trendradar /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl reload nginx
```

## Docker部署

### 构建镜像
```bash
cd docker
docker build -t trendradar:latest .
```

### 运行容器

#### 单次运行
```bash
docker run --rm \
  -v /path/to/TrendRadar/output:/app/output \
  -v /path/to/TrendRadar/config:/app/config \
  trendradar:latest
```

#### 后台运行
```bash
docker run -d \
  --name trendradar \
  -v /path/to/TrendRadar/output:/app/output \
  -v /path/to/TrendRadar/config:/app/config \
  -p 3333:3333 \
  trendradar:latest
```

### Docker Compose部署

创建 `docker-compose.yml`:
```yaml
version: '3.8'

services:
  trendradar:
    build: ./docker
    container_name: trendradar
    restart: unless-stopped
    ports:
      - "3333:3333"
    volumes:
      - ./output:/app/output
      - ./config:/app/config
      - ./logs:/app/logs
    environment:
      - TZ=Asia/Shanghai
      - PYTHONUNBUFFERED=1
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:3333/health"]
      interval: 30s
      timeout: 10s
      retries: 3
```

启动服务：
```bash
docker-compose up -d
```

## 定时任务部署

### 使用Cron（Linux/macOS）

编辑crontab：
```bash
crontab -e
```

添加定时任务：
```bash
# 每小时运行一次爬虫
0 * * * * cd /path/to/TrendRadar && uv run python main.py

# 每天凌晨2点生成摘要报告
0 2 * * * cd /path/to/TrendRadar && uv run python -c "
from mcp_server.tools.analytics import AnalyticsTools
tools = AnalyticsTools()
result = tools.generate_summary_report('daily')
print(result['markdown_report'])
" > /path/to/TrendRadar/reports/daily_$(date +\%Y\%m\%d).md
```

### 使用Task Scheduler（Windows）

1. 打开"任务计划程序"
2. 创建基本任务
3. 设置触发器（如每小时）
4. 设置操作：
   - 程序/脚本: `uv`
   - 参数: `run python main.py`
   - 起始位置: `C:\path\to\TrendRadar`

## 云平台部署

### VPS部署

#### 准备工作
```bash
# 更新系统
sudo apt update && sudo apt upgrade -y

# 安装必要软件
sudo apt install -y python3 python3-pip git nginx

# 安装UV
curl -LsSf https://astral.sh/uv/install.sh | sh
source ~/.bashrc
```

#### 部署应用
```bash
# 克隆项目
git clone https://github.com/sansan0/TrendRadar.git
cd TrendRadar

# 创建虚拟环境
uv sync

# 创建systemd服务
sudo tee /etc/systemd/system/trendradar.service > /dev/null <<EOF
[Unit]
Description=TrendRadar MCP Server
After=network.target

[Service]
Type=simple
User=ubuntu
WorkingDirectory=/home/ubuntu/TrendRadar
Environment=PATH=/home/ubuntu/.local/bin:/usr/local/bin:/usr/bin:/bin
ExecStart=/home/ubuntu/.local/bin/uv run python -m mcp_server.server --transport http --host 0.0.0.0 --port 3333
Restart=always
RestartSec=5

[Install]
WantedBy=multi-user.target
EOF

# 启用并启动服务
sudo systemctl enable trendradar
sudo systemctl start trendradar
```

### Docker Cloud部署

#### AWS ECS
1. 创建ECR仓库
2. 推送镜像：
```bash
aws ecr get-login-password --region us-west-2 | docker login --username AWS --password-stdin account.dkr.ecr.us-west-2.amazonaws.com
docker tag trendradar:latest account.dkr.ecr.us-west-2.amazonaws.com/trendradar:latest
docker push account.dkr.ecr.us-west-2.amazonaws.com/trendradar:latest
```

3. 创建ECS任务定义和service

#### Google Cloud Run
```bash
# 构建并推送镜像
gcloud builds submit --tag gcr.io/PROJECT_ID/trendradar

# 部署到Cloud Run
gcloud run deploy trendradar \
  --image gcr.io/PROJECT_ID/trendradar \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --port 3333
```

## 监控和维护

### 日志管理

#### 应用日志
```bash
# 查看实时日志
tail -f logs/trendradar.log

# 查看错误日志
grep ERROR logs/trendradar.log

# 日志轮转配置
sudo tee /etc/logrotate.d/trendradar > /dev/null <<EOF
/path/to/TrendRadar/logs/*.log {
    daily
    missingok
    rotate 30
    compress
    delaycompress
    notifempty
    create 644 ubuntu ubuntu
}
EOF
```

#### Docker日志
```bash
# 查看容器日志
docker logs trendradar

# 实时跟踪日志
docker logs -f trendradar
```

### 性能监控

#### 系统监控脚本
```bash
#!/bin/bash
# monitor.sh

# 检查服务状态
if ! systemctl is-active --quiet trendradar; then
    echo "TrendRadar service is not running"
    systemctl restart trendradar
fi

# 检查磁盘空间
DISK_USAGE=$(df /path/to/TrendRadar/output | tail -1 | awk '{print $5}' | sed 's/%//')
if [ $DISK_USAGE -gt 80 ]; then
    echo "Disk usage is high: ${DISK_USAGE}%"
    # 清理30天前的数据
    find /path/to/TrendRadar/output -type f -mtime +30 -delete
fi

# 检查内存使用
MEMORY_USAGE=$(ps aux | grep 'mcp_server.server' | grep -v grep | awk '{sum+=$6} END {print sum/1024}')
echo "Memory usage: ${MEMORY_USAGE} MB"
```

### 健康检查

#### HTTP健康检查端点
```bash
# 检查服务状态
curl http://localhost:3333/health

# 返回示例
{
  "status": "healthy",
  "version": "3.3.0",
  "uptime": "2 days, 14 hours"
}
```

#### 系统健康检查脚本
```bash
#!/bin/bash
# health_check.sh

# 检查MCP服务器
curl -f http://localhost:3333/health || {
    echo "MCP server health check failed"
    exit 1
}

# 检查数据更新
LATEST_DATA=$(find /path/to/TrendRadar/output -name "*.txt" -mmin -60 | wc -l)
if [ $LATEST_DATA -eq 0 ]; then
    echo "No data updates in the last hour"
    exit 1
fi

echo "All health checks passed"
```

## 故障排除

### 常见问题

#### 1. UV安装失败
**症状**: `uv: command not found`

**解决方案**:
```bash
# 手动添加到PATH
export PATH="$HOME/.cargo/bin:$PATH"
echo 'export PATH="$HOME/.cargo/bin:$PATH"' >> ~/.bashrc

# 或使用pip安装
pip install uv
```

#### 2. MCP连接失败
**症状**: 客户端无法连接到MCP服务器

**解决方案**:
```bash
# 检查服务状态
systemctl status trendradar

# 检查端口占用
netstat -tlnp | grep 3333

# 查看详细日志
journalctl -u trendradar -f
```

#### 3. 爬虫数据为空
**症状**: output目录没有数据文件

**解决方案**:
```bash
# 检查配置文件
cat config/config.yaml

# 手动运行爬虫
uv run python main.py

# 检查网络连接
curl -I https://newsnow.busiyi.world/api/s?id=zhihu&latest
```

#### 4. 内存不足
**症状**: 系统内存使用过高

**解决方案**:
```bash
# 检查内存使用
free -h

# 限制Python内存使用
ulimit -v 1048576  # 限制为1GB

# 在代码中优化内存使用
export PYTHONMALLOC=malloc
```

### 日志分析

#### 错误日志模式
```bash
# 查看常见错误
grep -E "(ERROR|Exception|Failed)" logs/trendradar.log | tail -20

# 统计错误类型
grep ERROR logs/trendradar.log | awk '{print $3}' | sort | uniq -c

# 查看性能瓶颈
grep -E "(slow|timeout)" logs/trendradar.log
```

## 安全配置

### 网络安全

#### 防火墙配置
```bash
# UFW配置
sudo ufw allow ssh
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp
sudo ufw allow 3333/tcp  # MCP HTTP端口
sudo ufw enable
```

#### HTTPS配置（使用Let's Encrypt）
```bash
# 安装Certbot
sudo apt install certbot python3-certbot-nginx

# 获取SSL证书
sudo certbot --nginx -d your-domain.com

# 自动续期
sudo crontab -e
# 添加: 0 12 * * * /usr/bin/certbot renew --quiet
```

### 访问控制

#### API密钥认证
```python
# 在MCP服务器中添加认证中间件
import os
from fastapi import HTTPException

API_KEY = os.getenv("MCP_API_KEY")

async def auth_middleware(request):
    auth_header = request.headers.get("Authorization")
    if not auth_header or auth_header != f"Bearer {API_KEY}":
        raise HTTPException(status_code=401, detail="Unauthorized")
```

## 备份和恢复

### 数据备份

#### 自动备份脚本
```bash
#!/bin/bash
# backup.sh

BACKUP_DIR="/backup/trendradar"
DATE=$(date +%Y%m%d_%H%M%S)

# 创建备份目录
mkdir -p $BACKUP_DIR

# 备份配置和数据
tar -czf $BACKUP_DIR/config_$DATE.tar.gz config/
tar -czf $BACKUP_DIR/data_$DATE.tar.gz output/

# 备份数据库（如果使用）
mysqldump -u user -p trendradar > $BACKUP_DIR/db_$DATE.sql

# 清理30天前的备份
find $BACKUP_DIR -name "*.tar.gz" -mtime +30 -delete
find $BACKUP_DIR -name "*.sql" -mtime +30 -delete
```

#### 定时备份
```bash
# 添加到crontab
0 3 * * * /path/to/TrendRadar/scripts/backup.sh
```

### 数据恢复

#### 恢复配置
```bash
tar -xzf /backup/trendradar/config_20250117_030000.tar.gz -C /
```

#### 恢复数据
```bash
tar -xzf /backup/trendradar/data_20250117_030000.tar.gz -C /
```

## 升级指南

### 应用升级

#### 1. 备份当前版本
```bash
cp -r /path/to/TrendRadar /path/to/TrendRadar.backup
```

#### 2. 更新代码
```bash
cd /path/to/TrendRadar
git pull origin main
```

#### 3. 更新依赖
```bash
uv sync
```

#### 4. 重启服务
```bash
sudo systemctl restart trendradar
```

#### 5. 验证升级
```bash
# 检查版本
curl http://localhost:3333/health

# 测试基本功能
curl -X POST http://localhost:3333/mcp \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc": "2.0", "method": "tools/call", "params": {"name": "get_system_status", "arguments": {}}, "id": 1}'
```

### 数据迁移

#### 版本兼容性
- 配置文件格式向后兼容
- 数据文件格式保持稳定
- 如有重大变更，会提供迁移脚本

## 性能调优

### 系统优化

#### 内核参数调优
```bash
# 编辑 /etc/sysctl.conf
echo "net.core.somaxconn = 65535" >> /etc/sysctl.conf
echo "net.ipv4.tcp_max_syn_backlog = 65535" >> /etc/sysctl.conf
echo "vm.swappiness = 10" >> /etc/sysctl.conf

# 应用配置
sudo sysctl -p
```

#### Python优化
```bash
# 环境变量优化
export PYTHONUNBUFFERED=1
export PYTHONDONTWRITEBYTECODE=1
export PYTHONMALLOC=malloc
```

### 应用优化

#### 数据库优化（如果使用）
```sql
-- 添加索引
CREATE INDEX idx_news_title ON news(title);
CREATE INDEX idx_news_date ON news(created_at);

-- 优化查询
EXPLAIN SELECT * FROM news WHERE title LIKE '%人工智能%';
```

#### 缓存优化
```python
# 在配置中调整缓存设置
CACHE_CONFIG = {
    'ttl': 900,  # 15分钟
    'max_size': 1000,
    'cleanup_interval': 300  # 5分钟清理一次
}
```

## 联系支持

如果在部署过程中遇到问题，可以通过以下方式获取帮助：

1. **GitHub Issues**: https://github.com/sansan0/TrendRadar/issues
2. **文档**: 查看项目README和FAQ
3. **社区**: 参与讨论和交流

---

*最后更新: 2025-01-17*
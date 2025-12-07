[根目录](../../CLAUDE.md) > [docker](../) > **Docker部署模块**

# Docker部署模块

## 模块职责

提供TrendRadar项目的完整容器化解决方案，包括Docker镜像构建、多架构支持、环境变量配置、定时任务管理等，支持快速部署和弹性扩容。

## 入口与启动

### Docker快速启动
```bash
# 方式一：一行命令快速启动
docker run -d --name trend-radar \
  -v ./config:/app/config:ro \
  -v ./output:/app/output \
  -e FEISHU_WEBHOOK_URL="你的飞书webhook" \
  wantcat/trendradar:latest

# 方式二：docker-compose启动（推荐）
cd docker
docker-compose up -d
```

### 入口文件
- **Dockerfile**: 主应用镜像构建配置
- **Dockerfile.mcp**: MCP服务独立镜像配置（v3.5.0新增）
- **docker-compose.yml**: 服务编排配置
- **docker-compose-build.yml**: 本地构建编排（v3.5.0新增）
- **entrypoint.sh**: 容器启动脚本
- **manage.py**: 容器管理工具
- **.env**: 环境变量配置

## 对外接口

### Docker管理接口
```bash
# 查看运行状态
docker exec -it trend-radar python manage.py status

# 手动执行爬虫
docker exec -it trend-radar python manage.py run

# 查看实时日志
docker exec -it trend-radar python manage.py logs

# 显示当前配置
docker exec -it trend-radar python manage.py config

# 显示输出文件
docker exec -it trend-radar python manage.py files

# v3.5.0 新增：启动 Web 服务器
docker exec -it trend-radar python manage.py --webserver

# v3.5.0 新增：启动 MCP 服务
docker-compose -f docker-compose-build.yml up mcp
```

### 容器服务接口
- **Web服务**: v3.5.0新增内置Web服务器（默认端口8080）
- **MCP服务**: 可选启用HTTP模式，端口3333
- **定时任务**: SuperCronic管理cron任务
- **日志输出**: 标准输出和文件日志

### MCP服务部署（v3.5.0新增）
```bash
# 方法一：使用独立镜像
docker run -d --name trendradar-mcp \
  -p 3333:3333 \
  -v ./output:/app/output:ro \
  wantcat/trendradar-mcp:latest

# 方法二：使用docker-compose
docker-compose -f docker-compose-build.yml up -d mcp

# MCP服务API测试
curl http://localhost:3333/tools/list
```

## 关键依赖与配置

### 基础镜像
```dockerfile
FROM python:3.10-slim
```

### 核心依赖
- **SuperCronic**: 定时任务管理器
- **Python 3.10**: 运行环境
- **项目依赖**: requirements.txt中的所有包

### 多架构支持
- **amd64**: x86_64架构，主流服务器
- **arm64**: ARM架构，树莓派等设备
- **自动检测**: 基于TARGETARCH构建对应架构

### 环境变量配置
```bash
# 核心功能配置
ENABLE_CRAWLER=true
ENABLE_NOTIFICATION=true
REPORT_MODE=daily

# 推送时间窗口
PUSH_WINDOW_ENABLED=true
PUSH_WINDOW_START=08:00
PUSH_WINDOW_END=22:00

# 通知配置（v3.5.0 支持多账号）
FEISHU_WEBHOOK_URL=url1;url2;url3
DINGTALK_WEBHOOK_URL=url1;url2
WEWORK_WEBHOOK_URL=url1
TELEGRAM_BOT_TOKEN=token1;token2;token3
TELEGRAM_CHAT_ID=id1;id2;id3

# 定时任务配置
CRON_SCHEDULE=*/30 * * * *
RUN_MODE=cron
IMMEDIATE_RUN=true

# v3.5.0 新增配置
REVERSE_CONTENT_ORDER=false        # 内容顺序控制
MAX_ACCOUNTS_PER_CHANNEL=3          # 每个渠道最大账号数
ENABLE_WEBSERVER=false              # Web服务器开关
WEBSERVER_PORT=8080                 # Web服务器端口
MAX_NEWS_PER_PLATFORM=30            # 每个平台最大新闻数
CRAWL_INTERVAL=30                   # 爬取间隔（分钟）
```

## 数据模型

### 镜像分层结构
```
1. Base Layer: python:3.10-slim
2. System Packages: curl, ca-certificates
3. SuperCronic: 定时任务管理器
4. Python Dependencies: pip install requirements.txt
5. Application Code: 项目代码复制
6. Configuration: 配置文件设置
7. Entrypoint: 启动脚本设置
```

### 容器数据结构
```
/app/
├── main.py              # 主程序
├── mcp_server/          # MCP服务模块
├── config/              # 配置文件（只读挂载）
├── output/              # 输出数据（持久化挂载）
├── requirements.txt     # Python依赖
├── manage.py           # 管理工具
└── entrypoint.sh       # 启动脚本
```

### 挂载卷结构
```yaml
volumes:
  ./config:/app/config:ro      # 配置文件只读挂载
  ./output:/app/output         # 输出数据持久化
  # 可选：日志目录挂载
  # ./logs:/app/logs
```

## 测试与质量

### 镜像构建测试
- **多架构构建**: 自动构建amd64和arm64镜像
- **分层优化**: 优化Dockerfile层数减少镜像大小
- **安全扫描**: 使用docker scout进行安全扫描
- **版本标签**: 严格的版本标签管理

### 容器运行测试
- **启动测试**: 验证容器正常启动和初始化
- **配置测试**: 验证环境变量配置生效
- **功能测试**: 验证爬虫和推送功能正常
- **持久化测试**: 验证数据正确持久化

### 性能优化
- **镜像大小**: 基于slim镜像减少体积
- **启动速度**: 优化启动脚本减少启动时间
- **内存使用**: 优化Python代码减少内存占用
- **网络优化**: 配置代理和连接池

## 常见问题 (FAQ)

### Q1: 配置文件修改不生效？
**A**:
1. 确认使用环境变量覆盖: `-e REPORT_MODE=daily`
2. 重启容器: `docker-compose restart`
3. 检查挂载路径: 确保config目录正确挂载

### Q2: 如何查看运行日志？
**A**:
```bash
# 查看容器日志
docker logs -f trend-radar

# 使用管理工具
docker exec -it trend-radar python manage.py logs
```

### Q3: 如何备份和恢复数据？
**A**:
```bash
# 备份output目录
tar -czf backup-$(date +%Y%m%d).tar.gz output/

# 恢复数据
tar -xzf backup-20251124.tar.gz
```

### Q4: 如何自定义定时任务？
**A**:
1. 修改环境变量: `-e CRON_SCHEDULE="0 */2 * * *"`
2. 或编辑docker-compose.yml中的cron配置
3. 重启容器生效

### Q5: 容器内如何调试？
**A**:
```bash
# 进入容器
docker exec -it trend-radar /bin/bash

# 测试配置
python manage.py config

# 手动运行
python manage.py run
```

## 相关文件清单

| 文件路径 | 描述 | 重要性 |
|---------|------|-------|
| `docker/Dockerfile` | 主应用镜像构建配置 | ⭐⭐⭐ |
| `docker/Dockerfile.mcp` | MCP服务独立镜像配置（v3.5.0新增） | ⭐⭐⭐ |
| `docker/docker-compose.yml` | 服务编排配置 | ⭐⭐⭐ |
| `docker/docker-compose-build.yml` | 本地构建编排配置（v3.5.0新增） | ⭐⭐ |
| `docker/.env` | 环境变量配置 | ⭐⭐ |
| `docker/entrypoint.sh` | 容器启动脚本 | ⭐⭐ |
| `docker/manage.py` | 容器管理工具 | ⭐⭐ |

## 变更记录 (Changelog)

**2025-12-07**: v3.5.0重大更新
- 新增Dockerfile.mcp独立MCP服务镜像
- 新增docker-compose-build.yml构建编排
- 新增Web服务器支持
- 新增多账号推送支持
- 更新环境变量配置项
- 添加MCP服务HTTP模式部署说明

**2025-11-24**: 创建Docker部署模块文档，详细说明容器化部署方案和管理工具
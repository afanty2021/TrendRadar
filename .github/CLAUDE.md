[根目录](../../CLAUDE.md) > [.github](../) > **CI/CD自动化模块**

# CI/CD自动化模块

## 模块职责

提供基于GitHub Actions的完整CI/CD解决方案，包括定时爬取任务、Docker镜像自动构建、多架构支持、以及自动化测试和部署流程。

## 入口与启动

### 主要工作流
- **crawler.yml**: 定时爬取任务，每小时执行一次
- **docker.yml**: Docker镜像构建和发布

### 触发方式
```yaml
# 定时触发（每小时执行）
schedule:
  - cron: "0 * * * *"

# 手动触发
workflow_dispatch:

# 代码更新触发
push:
  branches: [ master ]
pull_request:
  branches: [ master ]
```

## 对外接口

### 爬虫工作流接口
```yaml
name: Hot News Crawler

on:
  schedule:
    - cron: "0 * * * *"  # 每小时整点运行
  workflow_dispatch:     # 支持手动触发

jobs:
  crawl:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout repository
      - name: Set up Python
      - name: Install dependencies
      - name: Run crawler
      - name: Generate report
      - name: Send notifications
```

### Docker构建接口
```yaml
name: Build and Push Docker Image

on:
  push:
    tags: [ 'v*' ]  # 标签推送时构建
  workflow_dispatch:

jobs:
  build:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        platform: [linux/amd64, linux/arm64]
```

### 权限配置
```yaml
permissions:
  contents: write    # 允许写入内容
  packages: write    # 允许发布包
```

## 关键依赖与配置

### GitHub Actions依赖
```yaml
actions:
  - actions/checkout@v3           # 代码检出
  - actions/setup-python@v4       # Python环境设置
  - docker/setup-buildx-action@v2 # Docker构建设置
  - docker/login-action@v2        # Docker登录
  - docker/build-push-action@v4   # Docker构建推送
```

### 环境依赖
- **Python 3.10**: 运行环境
- **Docker Buildx**: 多架构构建
- **Ubuntu Latest**: 运行环境

### Secret配置
```yaml
# 通知相关Secrets
FEISHU_WEBHOOK_URL: ${{ secrets.FEISHU_WEBHOOK_URL }}
DINGTALK_WEBHOOK_URL: ${{ secrets.DINGTALK_WEBHOOK_URL }}
WEWORK_WEBHOOK_URL: ${{ secrets.WEWORK_WEBHOOK_URL }}
TELEGRAM_BOT_TOKEN: ${{ secrets.TELEGRAM_BOT_TOKEN }}
TELEGRAM_CHAT_ID: ${{ secrets.TELEGRAM_CHAT_ID }}

# Docker相关Secrets
DOCKER_USERNAME: ${{ secrets.DOCKER_USERNAME }}
DOCKER_PASSWORD: ${{ secrets.DOCKER_PASSWORD }}
```

## 数据模型

### 工作流数据模型
```yaml
workflow:
  name: string              # 工作流名称
  on:                     # 触发条件
    schedule:              # 定时触发
      - cron: string
    workflow_dispatch:     # 手动触发
    push:                  # 推送触发
      branches: [string]
  jobs:                   # 任务列表
    job_id:               # 任务ID
      runs-on: string     # 运行环境
      strategy:           # 策略配置
        matrix:           # 矩阵配置
      steps:              # 步骤列表
```

### 构建数据模型
```yaml
build:
  context: string          # 构建上下文
  file: string            # Dockerfile路径
  platforms: [string]     # 目标架构
  tags: [string]          # 镜像标签
  push: boolean           # 是否推送
  cache-from:             # 缓存源
  cache-to:               # 缓存目标
```

## 测试与质量

### 工作流测试
- **本地测试**: 使用act工具本地运行工作流
- **分支测试**: 在feature分支测试工作流
- **手动触发**: 通过workflow_dispatch测试
- **日志分析**: 分析运行日志和错误信息

### 构建质量
- **多架构构建**: 同时构建amd64和arm64镜像
- **缓存优化**: 使用GitHub Actions缓存加速构建
- **安全扫描**: 集成安全扫描工具
- **版本管理**: 严格的标签版本管理

### 性能优化
- **并行构建**: 多架构并行构建
- **增量构建**: 基于变更的增量构建
- **缓存策略**: 多层缓存优化
- **资源限制**: 合理配置资源使用

## 常见问题 (FAQ)

### Q1: 定时任务没有执行？
**A**:
1. 检查cron表达式格式
2. 确认仓库为活跃状态
3. 检查Actions权限配置
4. 查看工作流历史记录

### Q2: Docker构建失败？
**A**:
1. 检查Docker Hub权限
2. 验证Dockerfile语法
3. 查看构建日志错误信息
4. 确认多架构构建配置

### Q3: 如何修改执行频率？
**A**: 修改crawler.yml中的cron表达式:
```yaml
# 每小时执行
- cron: "0 * * * *"
# 每半小时执行
- cron: "*/30 * * * *"
# 每天特定时间执行
- cron: "0 8,20 * * *"
```

### Q4: 如何调试工作流？
**A**:
1. 使用workflow_dispatch手动触发
2. 查看详细执行日志
3. 添加debug输出步骤
4. 使用act工具本地测试

### Q5: Secret配置不生效？
**A**:
1. 检查Secret名称是否正确
2. 确认Secret权限设置
3. 验证环境变量引用格式
4. 重新设置Secret值

## 相关文件清单

| 文件路径 | 描述 | 重要性 |
|---------|------|-------|
| `.github/workflows/crawler.yml` | 定时爬取工作流 | ⭐⭐⭐ |
| `.github/workflows/docker.yml` | Docker构建工作流 | ⭐⭐⭐ |
| `.github/ISSUE_TEMPLATE/` | Issue模板 | ⭐⭐ |
| `requirements.txt` | Python依赖 | ⭐⭐ |

## 变更记录 (Changelog)

**2025-11-24**: 创建CI/CD自动化模块文档，详细说明工作流配置和最佳实践
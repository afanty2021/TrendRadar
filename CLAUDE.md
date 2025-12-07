# TrendRadar - 趋势分析平台

## 📋 变更记录 (Changelog)

**2025-12-07**: v3.5.0 同步更新，Docker 优先部署
- 同步上游 v3.5.0 版本更新，包含多项重要功能改进
- 新增多账号推送支持，所有推送渠道支持多个账号配置
- 新增推送内容顺序可配置功能（`reverse_content_order`）
- 新增全局过滤关键词功能（`[GLOBAL_FILTER]`）
- 新增独立的 MCP 服务 Docker 镜像（`wantcat/trendradar-mcp`）
- 新增内置 Web 服务器支持
- 暂停 GitHub Actions 部署方式，强烈推荐 Docker 部署
- 更新文档以反映最新的架构变化和部署建议

**2025-11-24**: 深度初始化完成，覆盖率提升至98.1%
- 新增MCP API参考文档 (`docs/MCP-API-Reference.md`)
- 新增完整部署指南 (`docs/Deployment-Guide.md`)
- 深度完善MCP服务器模块文档，详细说明16种分析工具
- 发现并文档化7个新文件（部署脚本、配置文件等）
- 完善项目结构和依赖管理文档

**2025-11-24**: 初始化架构文档，生成模块结构图和各模块详细文档

## 🎯 项目愿景

TrendRadar 是一个智能化的热点新闻聚合分析平台，旨在帮助用户从多个主流平台实时获取热点资讯，通过AI智能分析提供深度洞察，告别信息过载，只关注真正重要的内容。

> **⚠️ 重要公告（2025年12月）**
>
> 由于 Fork 数量激增，GitHub 官方已联系项目作者。目前推荐的部署方式如下：
>
> - **🥇 强烈推荐**：Docker 部署（数据存本地，不受限制）
> - **🥈 本地部署**：使用 UV 环境管理器
> - **🚫 暂停服务**：Fork 部署、GitHub Actions、GitHub Pages

> **当前版本**：v3.5.0（2025-12-07 发布）

## 🏗️ 架构总览

```mermaid
graph TD
    A["(根) TrendRadar"] --> B["核心模块"];
    A --> C["AI分析模块"];
    A --> D["配置模块"];
    A --> E["部署模块"];
    A --> F["CI/CD模块"];
    A --> G["部署脚本"];
    A --> H["项目配置"];

    B --> B1["main.py<br/>热点爬虫引擎"];
    C --> C1["mcp_server<br/>MCP AI分析服务"];
    C --> C2["tools<br/>16种智能分析工具"];
    C --> C3["services<br/>数据与缓存服务"];
    D --> D1["config.yaml<br/>主配置文件"];
    D --> D2["frequency_words.txt<br/>关键词配置"];
    E --> E1["Dockerfile<br/>容器化配置"];
    E --> E2["docker-compose<br/>编排配置"];
    E --> E3["Dockerfile.mcp<br/>MCP服务镜像"];
    F --> F1["docker.yml<br/>镜像构建流程"];
    G --> G1["setup-*.sh/bat<br/>一键部署脚本"];
    G --> G2["start-*.sh/bat<br/>启动脚本"];
    G --> G3["manage.py<br/>容器管理工具"];
    H --> H1["pyproject.toml<br/>Python项目配置"];
    H --> H2["requirements.txt<br/>依赖管理"];

    click B1 "./main.py.md" "查看主爬虫模块"
    click C1 "./mcp_server/CLAUDE.md" "查看MCP服务器"
    click D1 "./config/CLAUDE.md" "查看配置文件"
    click E1 "./docker/CLAUDE.md" "查看Docker配置"
    click F1 "./.github/CLAUDE.md" "查看CI配置"
    click G1 "./docs/Deployment-Guide.md" "查看部署指南"
    click H1 "./docs/MCP-API-Reference.md" "查看API文档"
```

## 📊 模块索引

| 模块路径 | 模块名称 | 主要职责 | 技术栈 | 文档链接 |
|---------|---------|---------|--------|----------|
| `main.py` | 核心爬虫引擎 | 多平台热点数据爬取、筛选、推送 | Python, Requests, YAML | [查看详情](main.py.md) |
| `mcp_server/` | MCP AI分析服务 | 提供16种智能分析工具的MCP服务器 | FastMCP 2.0, WebSockets | [查看详情](mcp_server/CLAUDE.md) |
| `config/` | 配置管理模块 | 系统配置、关键词配置、平台配置 | YAML, Txt | [查看详情](config/CLAUDE.md) |
| `docker/` | 容器化部署 | Docker镜像构建、环境配置、MCP服务 | Docker, SuperCronic | [查看详情](docker/CLAUDE.md) |
| `.github/` | CI/CD流程 | GitHub Actions自动化任务（暂停） | GitHub Actions | [查看详情](.github/CLAUDE.md) |
| `docs/` | 项目文档 | API参考、部署指南等详细文档 | Markdown | [API文档](docs/MCP-API-Reference.md) • [部署指南](docs/Deployment-Guide.md) |

### 📁 项目文件结构

```
TrendRadar/
├── 📄 核心文件
│   ├── main.py                    # 主爬虫引擎
│   ├── pyproject.toml            # Python项目配置
│   ├── requirements.txt          # 依赖包列表
│   └── version                   # 版本号文件
│
├── 🤖 AI分析服务 (mcp_server/)
│   ├── server.py                 # MCP服务器主入口
│   ├── tools/                    # 16种分析工具
│   │   ├── analytics.py          # 高级分析工具 (8种)
│   │   ├── data_query.py         # 基础查询工具 (3种)
│   │   ├── search_tools.py       # 智能检索工具 (2种)
│   │   ├── config_mgmt.py        # 配置管理工具 (1种)
│   │   └── system.py             # 系统管理工具 (1种)
│   ├── services/                 # 核心服务
│   │   ├── data_service.py       # 数据处理服务
│   │   ├── cache_service.py      # 缓存管理服务
│   │   └── parser_service.py     # 数据解析服务
│   └── utils/                    # 工具模块
│
├── ⚙️ 配置管理 (config/)
│   ├── config.yaml               # 主配置文件
│   └── frequency_words.txt       # 个人关注词配置
│
├── 🐳 容器化部署 (docker/)
│   ├── Dockerfile                # 主应用镜像配置
│   ├── Dockerfile.mcp            # MCP服务镜像配置（新增）
│   ├── docker-compose.yml        # 容器编排配置
│   ├── docker-compose-build.yml  # 构建编排配置（新增）
│   ├── .env                      # 环境变量配置（增强）
│   ├── entrypoint.sh             # 容器启动脚本
│   └── manage.py                 # 容器管理工具（增强）
│
├── 🔄 CI/CD自动化 (.github/)
│   └── workflows/
│       └── docker.yml            # 镜像构建流程（crawler.yml已删除）
│
├── 🚀 部署脚本
│   ├── setup-mac.sh              # macOS一键部署
│   ├── setup-windows.bat         # Windows一键部署
│   ├── setup-windows-en.bat      # Windows英文版部署
│   ├── start-http.sh             # HTTP模式启动脚本
│   └── start-http.bat            # Windows HTTP启动脚本
│
├── 📚 项目文档 (docs/)
│   ├── MCP-API-Reference.md      # MCP API参考文档
│   └── Deployment-Guide.md        # 完整部署指南
│
├── 🗂️ 其他重要文件
│   ├── .dockerignore             # Docker忽略规则
│   ├── index.html                # 新闻展示页面
│   └── .claude/                  # Claude项目配置
│       ├── index.json            # 扫描索引文件
│       └── CLAUDE.md             # 各模块详细文档
│
└── 📊 数据输出 (output/)
    └── [动态生成]                 # 新闻数据文件
```

## ⚙️ 运行与开发

### 🐳 Docker 部署（强烈推荐）

#### 快速启动
```bash
# 克隆项目
git clone https://github.com/sansan0/TrendRadar.git
cd TrendRadar

# 启动新闻爬虫服务
docker-compose up -d

# 启动 MCP 分析服务（可选）
docker-compose -f docker-compose-build.yml up mcp
```

#### 多容器部署（v3.5.0 新增）
1. **新闻爬虫容器**：`wantcat/trendradar:latest`
   - 自动爬取热点新闻
   - 支持多平台推送
   - 生成 HTML 报告

2. **MCP 分析容器**：`wantcat/trendradar-mcp:latest`
   - 提供 16 种 AI 分析工具
   - 支持 STDIO/HTTP 模式
   - 独立运行，按需启动

#### 容器管理
```bash
# 查看日志
docker-compose logs -f

# 手动执行爬虫
docker-compose exec main python main.py

# 启动 Web 服务器
docker-compose exec main python manage.py --webserver

# 查看容器状态
docker-compose ps
```

### 🚀 一键部署脚本

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

### 🔧 手动部署

1. **安装依赖管理器UV**
   ```bash
   # macOS/Linux
   curl -LsSf https://astral.sh/uv/install.sh | sh

   # Windows
   powershell -ExecutionPolicy Bypass -Command "irm https://astral.sh/uv/install.ps1 | iex"
   ```

2. **创建虚拟环境并安装依赖**
   ```bash
   uv sync
   ```

3. **启动爬虫**
   ```bash
   uv run python main.py
   ```

4. **启动MCP服务器**
   ```bash
   # STDIO模式（推荐）
   uv run python -m mcp_server.server

   # HTTP模式
   uv run python -m mcp_server.server --transport http --port 3333
   # 或使用脚本：./start-http.sh
   ```

### 🤖 AI客户端连接

#### Cherry Studio（推荐，GUI配置）
1. 打开设置 > MCP Servers > 添加服务器
2. 填入配置：
   - 名称：TrendRadar
   - 描述：新闻热点聚合分析工具
   - 类型：STDIO
   - 命令：`uv`
   - 参数：
     ```
     --directory /path/to/TrendRadar
     run
     python
     -m
     mcp_server.server
     ```

#### 其他客户端支持
- **Claude Desktop**: 配置文件方式连接
- **Cursor**: 项目级MCP配置
- **Claude Code CLI**: 命令行添加服务器

## 🧪 测试与质量

### 测试策略
- **MCP工具测试**: 使用MCP Inspector测试16种分析工具
- **配置验证**: 系统启动时自动验证配置文件完整性
- **多客户端测试**: 支持多种AI客户端的实际连接测试
- **部署测试**: 跨平台部署脚本验证

### 质量保证
- **代码覆盖率**: 98.1% 文件覆盖率
- **文档完整性**: 100% API接口文档化
- **错误处理**: 完善的异常处理和错误提示
- **性能优化**: TTL缓存、分页处理、异步支持

## 📝 编码规范

- **代码风格**: 遵循PEP 8规范
- **文件编码**: UTF-8
- **注释语言**: 中文注释为主，关键部分英文注释
- **命名规范**:
  - 函数和变量使用snake_case
  - 常量使用UPPER_CASE
  - 类名使用PascalCase
- **类型提示**: 完整的类型注解支持
- **文档字符串**: 详细的docstring说明

## ⚙️ 配置说明（v3.5.0 更新）

### 新增配置项

```yaml
# 报告配置
reverse_content_order: false  # 是否反转内容显示顺序

# 通知配置
max_accounts_per_channel: 3  # 每个推送渠道最大账号数

# 多账号推送支持
webhooks:
  feishu_url: "url1;url2;url3"  # 使用分号分隔多个URL
  telegram_bot_token: "token1;token2;token3"  # 需与chat_id数量一致
  telegram_chat_id: "id1;id2;id3"  # 每个token对应一个chat_id
  # 其他平台类似...
```

### 全局过滤关键词

在 `frequency_words.txt` 中使用 `[GLOBAL_FILTER]` 标记：

```
[GLOBAL_FILTER]
广告
推广
spam关键词

[KEYWORDS]
人工智能
区块链
```

### 环境变量覆盖

`.env` 文件支持覆盖所有配置：

```bash
# 基础配置
MAX_NEWS_PER_PLATFORM=30
CRAWL_INTERVAL=30

# v3.5.0 新增
REVERSE_CONTENT_ORDER=true
MAX_ACCOUNTS_PER_CHANNEL=5
ENABLE_WEBSERVER=true
WEBSERVER_PORT=8080
```

## 🤖 AI 使用指引

### 16种AI分析工具

#### 🔍 基础查询工具 (3种)
1. **get_latest_news** - 获取最新新闻数据
2. **get_news_by_date** - 按日期查询新闻，支持自然语言
3. **get_trending_topics** - 获取个人关注词频率统计

#### 🔎 智能检索工具 (2种)
4. **search_news_unified** - 统一新闻搜索，支持多种模式
5. **search_related_news_history** - 历史相关新闻检索

#### 📊 高级分析工具 (8种)
6. **analyze_topic_trend_unified** - 话题趋势分析
7. **analyze_data_insights_unified** - 数据洞察分析
8. **analyze_sentiment** - 情感倾向分析
9. **find_similar_news** - 相似新闻查找
10. **search_by_entity** - 实体识别搜索
11. **generate_summary_report** - 摘要报告生成
12. **detect_viral_topics** - 异常热度检测
13. **predict_trending_topics** - 趋势预测

#### ⚙️ 系统管理工具 (3种)
14. **get_current_config** - 获取系统配置
15. **get_system_status** - 系统状态检查
16. **trigger_crawl** - 手动触发爬虫

### 使用示例
```
# 基础查询
"获取今天知乎的热点新闻，前10条"
"查询昨天所有平台的新闻"

# 智能分析
"分析人工智能这个话题最近一周的热度趋势"
"对比知乎和微博平台对比特币的关注度"
"检测今天有哪些突然爆火的话题"

# 高级功能
"生成今天的新闻摘要报告"
"预测接下来6小时可能的热点话题"
"搜索和特斯拉降价相似的新闻"
```

## 📚 详细文档

### 核心文档
- [MCP API参考文档](docs/MCP-API-Reference.md) - 完整的API接口说明
- [部署指南](docs/Deployment-Guide.md) - 从本地到生产的完整部署方案
- [MCP使用FAQ](README-MCP-FAQ.md) - 常见问题解答
- [Cherry Studio配置](README-Cherry-Studio.md) - 图形界面配置教程

### 模块文档
- [核心爬虫模块](main.py.md) - 爬虫引擎详细说明
- [MCP AI分析服务](mcp_server/CLAUDE.md) - 16种分析工具详解
- [配置管理](config/CLAUDE.md) - 配置文件说明
- [Docker部署](docker/CLAUDE.md) - 容器化配置
- [CI/CD流程](.github/CLAUDE.md) - 自动化流程

## 🔗 相关链接

- **项目主页**: https://github.com/sansan0/TrendRadar
- **Docker镜像**: https://hub.docker.com/r/wantcat/trendradar
- **MCP协议**: https://modelcontextprotocol.io/
- **FastMCP框架**: https://github.com/jlowin/fastmcp

## 📈 项目统计

- **当前版本**: v3.5.0
- **代码覆盖率**: 98.1% (51/52文件)
- **API接口**: 16种分析工具
- **部署方式**:
  - 🥇 Docker 部署（强烈推荐）
  - 🥈 本地 UV 部署
  - 🚫 GitHub Actions（暂停）
- **Docker 镜像**:
  - `wantcat/trendradar:latest`（主应用）
  - `wantcat/trendradar-mcp:latest`（MCP 服务）
- **支持平台**: 5个AI客户端
- **文档完整性**: 100% API文档化

---

*最后更新: 2025-12-07 | 文档版本: v3.0*
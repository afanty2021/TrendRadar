# mcp_server - MCP 协议服务器

[根目录](../CLAUDE.md) > **mcp_server/**

> **最后更新**：2026-01-31 15:19:33
> **模块类型**：MCP 服务

## 模块职责

MCP 服务器模块实现 Model Context Protocol 协议，为 AI 客户端（Cherry Studio、Claude Desktop、Cursor 等）提供 21 个工具和 5 个资源，支持数据查询、分析、搜索、配置管理、系统控制和存储同步等功能。

## 入口与启动

### 主要入口
- **`server.py`**：MCP 服务器主入口

### 启动方式
```bash
# stdio 模式（单客户端）
trendradar-mcp

# HTTP 模式（多客户端）
./start-http.sh
# URL: http://localhost:3333/mcp
```

### 支持的传输模式
- **stdio**：单客户端，命令行管道
- **HTTP**：多客户端，WebSocket 通信

## 对外接口

### MCP 工具（21个）

**数据查询工具**
```python
get_latest_news(limit: int) -> Dict
get_news_by_date(date: str, keywords: List[str]) -> Dict
get_trending_topics(limit: int) -> Dict
list_available_dates(source: str) -> Dict
get_latest_rss(feeds: List[str], limit: int) -> Dict
search_rss(query: str, feeds: List[str], limit: int) -> Dict
get_rss_feeds_status() -> Dict
```

**分析工具**
```python
analyze_topic_trend(topic: str, days: int) -> Dict
analyze_data_insights(date: str) -> Dict
analyze_sentiment(text: str) -> Dict
aggregate_news(platforms: List[str], limit: int) -> Dict
compare_periods(period1: str, period2: str) -> Dict
generate_summary_report(period: str, report_type: str) -> Dict
find_similar_news(title: str, limit: int) -> Dict
```

**搜索工具**
```python
search_news(query: str, date_range: str, platforms: List[str]) -> Dict
```

**系统工具**
```python
get_system_status() -> Dict
get_current_config(section: str) -> Dict
check_version() -> Dict
trigger_crawl(platforms: List[str]) -> Dict
```

**存储工具**
```python
sync_from_remote(dates: List[str]) -> Dict
get_storage_status() -> Dict
```

### MCP 资源（5个）

```python
config://platforms        # 支持的平台列表
config://rss-feeds        # RSS 订阅源列表
data://available-dates    # 可用日期范围
config://keywords         # 关注词配置
data://statistics         # 数据统计信息
```

## 关键依赖与配置

### 内部依赖
```
mcp_server/
├── server.py             # 服务器主入口
├── tools/                # 工具集
│   ├── data_query.py     # 数据查询工具
│   ├── analytics.py      # 分析工具
│   ├── search_tools.py   # 搜索工具
│   ├── config_mgmt.py    # 配置管理工具
│   ├── system.py         # 系统工具
│   └── storage_sync.py   # 存储同步工具
└── utils/                # 工具类
    ├── date_parser.py    # 日期解析器
    ├── errors.py         # 错误处理
    └── validators.py     # 数据验证
```

### 服务层
```
services/
├── cache_service.py      # 缓存服务
├── data_service.py       # 数据服务
└── parser_service.py     # 解析服务
```

### 外部依赖
- **fastmcp >= 2.12.0**：MCP 协议实现
- **websockets >= 13.0**：WebSocket 支持

## 日期解析工具

**自然语言日期支持**：
- "今天"、"昨天"、"前天"
- "最近3天"、"本周"、"上周"
- "最近一周"、"最近一个月"
- "YYYY-MM-DD" 格式

**示例**：
```python
from mcp_server.utils.date_parser import DateParser

parser = DateParser()
parser.parse_date_range("最近3天")  # 返回 (start_date, end_date)
```

## 数据模型

### MCPResponse
```python
@dataclass
class MCPResponse:
    success: bool                # 是否成功
    data: Any                    # 返回数据
    error: Optional[str]         # 错误信息
    metadata: Optional[Dict]     # 元数据
```

### ToolContext
```python
@dataclass
class ToolContext:
    project_root: str            # 项目根目录
    config: Dict                 # 配置
    storage: StorageManager      # 存储管理器
```

## 测试与质量

**当前状态**：未配置测试

**建议测试覆盖**：
- 各工具函数测试
- 日期解析器测试
- 错误处理测试
- 缓存服务测试

## 常见问题 (FAQ)

### Q1: 如何在 Cherry Studio 中使用？

**A**: 配置 MCP 服务器：
```json
{
  "mcpServers": {
    "trendradar": {
      "command": "trendradar-mcp",
      "cwd": "/path/to/TrendRadar"
    }
  }
}
```

### Q2: 如何启用 HTTP 模式？

**A**: 运行启动脚本：
```bash
./start-http.sh
# URL: http://localhost:3333/mcp
```

### Q3: 工具返回数据格式？

**A**: 统一使用 MCPResponse：
```json
{
  "success": true,
  "data": {...},
  "error": null,
  "metadata": {...}
}
```

### Q4: 如何调试 MCP 服务器？

**A**: 启用调试模式：
```bash
trendradar-mcp --debug
```

## 相关文件清单

### 核心文件
- `server.py`：服务器主入口，约 300+ 行

### 工具文件
- `tools/analytics.py`：分析工具，约 2291 行
- `tools/search_tools.py`：搜索工具，约 965 行
- `tools/system.py`：系统工具，约 558 行
- `tools/storage_sync.py`：存储同步，约 506 行
- `tools/data_query.py`：数据查询，约 354 行
- `tools/config_mgmt.py`：配置管理，约 54 行

### 服务文件
- `services/data_service.py`：数据服务，约 803 行
- `services/parser_service.py`：解析服务，约 364 行
- `services/cache_service.py`：缓存服务，约 121 行

### 工具类文件
- `utils/date_parser.py`：日期解析，约 456 行
- `utils/validators.py`：数据验证，约 435 行
- `utils/errors.py`：错误处理，约 81 行

## 变更记录 (Changelog)

### 2026-01-31 15:19:33
- ✨ 创建模块文档
- 📊 完成 21 个工具接口分析
- 🔗 完成 5 个资源接口分析

---

*本文档由 AI 自动生成并维护*

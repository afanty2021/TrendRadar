# mcp_server/tools - MCP 工具模块

[根目录](../../CLAUDE.md) > [mcp_server](../CLAUDE.md) > **tools/**

> **最后更新**：2026-01-31 15:19:33
> **模块类型**：MCP 工具集

## 模块职责

MCP 工具模块包含所有对外暴露的工具实现，按功能分为 6 大类：数据查询、分析、搜索、配置管理、系统控制和存储同步。

## 工具分类

### 1. 数据查询工具 (data_query.py)

```python
class DataQueryTools:
    """数据查询工具集"""

    def get_latest_news(
        self,
        limit: int = 50
    ) -> Dict:
        """获取最新新闻"""

    def get_news_by_date(
        self,
        date: str,
        keywords: Optional[List[str]] = None
    ) -> Dict:
        """按日期查询新闻"""

    def get_trending_topics(
        self,
        limit: int = 20
    ) -> Dict:
        """获取趋势话题"""

    def list_available_dates(
        self,
        source: str = "local"
    ) -> Dict:
        """列出可用日期"""

    def get_latest_rss(
        self,
        feeds: Optional[List[str]] = None,
        limit: int = 50
    ) -> Dict:
        """获取最新 RSS 订阅数据"""

    def search_rss(
        self,
        query: str,
        feeds: Optional[List[str]] = None,
        limit: int = 50
    ) -> Dict:
        """搜索 RSS 数据"""

    def get_rss_feeds_status(
        self
    ) -> Dict:
        """获取 RSS 源状态"""
```

### 2. 分析工具 (analytics.py)

```python
class AnalyticsTools:
    """数据分析工具集"""

    def analyze_topic_trend(
        self,
        topic: str,
        days: int = 7
    ) -> Dict:
        """话题趋势分析"""

    def analyze_data_insights(
        self,
        date: str
    ) -> Dict:
        """数据洞察分析"""

    def analyze_sentiment(
        self,
        text: str
    ) -> Dict:
        """情感倾向分析"""

    def aggregate_news(
        self,
        platforms: Optional[List[str]] = None,
        limit: int = 100
    ) -> Dict:
        """跨平台新闻聚合"""

    def compare_periods(
        self,
        period1: str,
        period2: str
    ) -> Dict:
        """时期对比分析"""

    def generate_summary_report(
        self,
        period: str = "today",
        report_type: str = "daily"
    ) -> Dict:
        """生成摘要报告"""

    def find_similar_news(
        self,
        title: str,
        limit: int = 10
    ) -> Dict:
        """查找相似新闻"""
```

### 3. 搜索工具 (search_tools.py)

```python
class SearchTools:
    """搜索工具集"""

    def search_news(
        self,
        query: str,
        date_range: Optional[str] = None,
        platforms: Optional[List[str]] = None,
        keywords: Optional[List[str]] = None,
        limit: int = 50
    ) -> Dict:
        """统一新闻搜索"""
```

### 4. 配置管理工具 (config_mgmt.py)

```python
class ConfigManagementTools:
    """配置管理工具集"""

    def get_current_config(
        self,
        section: Optional[str] = None
    ) -> Dict:
        """获取当前配置"""
```

### 5. 系统工具 (system.py)

```python
class SystemManagementTools:
    """系统管理工具集"""

    def get_system_status(
        self
    ) -> Dict:
        """获取系统状态"""

    def check_version(
        self
    ) -> Dict:
        """检查版本更新"""

    def trigger_crawl(
        self,
        platforms: Optional[List[str]] = None,
        mode: str = "quick"
    ) -> Dict:
        """触发爬取任务"""
```

### 6. 存储同步工具 (storage_sync.py)

```python
class StorageSyncTools:
    """存储同步工具集"""

    def sync_from_remote(
        self,
        dates: Optional[List[str]] = None
    ) -> Dict:
        """从远程同步数据"""

    def get_storage_status(
        self
    ) -> Dict:
        """获取存储状态"""

    def cleanup_old_data(
        self,
        retain_days: int = 30
    ) -> Dict:
        """清理过期数据"""
```

## 关键依赖

### 内部依赖
```
mcp_server/
└── tools/
    ├── data_query.py      # 数据查询（7个工具）
    ├── analytics.py       # 分析工具（7个工具）
    ├── search_tools.py    # 搜索工具（1个工具）
    ├── config_mgmt.py     # 配置管理（1个工具）
    ├── system.py          # 系统工具（3个工具）
    └── storage_sync.py    # 存储同步（3个工具）
```

### 服务依赖
- `services/data_service.py`：数据访问服务
- `services/parser_service.py`：数据解析服务
- `services/cache_service.py`：缓存服务

### 工具依赖
- `utils/date_parser.py`：日期解析器
- `utils/validators.py`：数据验证器
- `utils/errors.py`：错误处理

## 工具总数统计

| 类别 | 工具数量 | 文件 |
|------|---------|------|
| 数据查询 | 7 | data_query.py |
| 分析 | 7 | analytics.py |
| 搜索 | 1 | search_tools.py |
| 配置管理 | 1 | config_mgmt.py |
| 系统 | 3 | system.py |
| 存储同步 | 3 | storage_sync.py |
| **总计** | **22** | |

## 测试与质量

**当前状态**：未配置测试

**建议测试覆盖**：
- 每个工具函数的输入输出测试
- 错误处理和边界条件测试
- 服务集成测试

## 常见问题 (FAQ)

### Q1: 如何添加新工具？

**A**: 在对应工具类中添加方法，并在 `server.py` 中注册：
```python
@mcp.tool()
async def my_new_tool(arg: str) -> Dict:
    """工具描述"""
    tools = _get_tools()
    return await asyncio.to_thread(
        tools['category'].my_new_tool, arg
    )
```

### Q2: 工具参数如何验证？

**A**: 使用 `validators.py` 中的验证器：
```python
from .utils.validators import validate_date_string

validate_date_string(date_str)  # 抛出 MCPError 如果无效
```

### Q3: 如何处理异步操作？

**A**: 使用 `asyncio.to_thread` 将同步操作转为异步：
```python
result = await asyncio.to_thread(
    self.data_service.query_news,
    date_str
)
```

## 相关文件清单

- `data_query.py`：数据查询工具，约 354 行
- `analytics.py`：分析工具，约 2291 行
- `search_tools.py`：搜索工具，约 965 行
- `config_mgmt.py`：配置管理工具，约 54 行
- `system.py`：系统工具，约 558 行
- `storage_sync.py`：存储同步工具，约 506 行

## 变更记录 (Changelog)

### 2026-01-31 15:19:33
- ✨ 创建工具模块文档
- 📊 完成 22 个工具接口分析

---

*本文档由 AI 自动生成并维护*

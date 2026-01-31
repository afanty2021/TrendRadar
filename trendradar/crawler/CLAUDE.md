# trendradar/crawler - 数据采集模块

[根目录](../../CLAUDE.md) > [trendradar](../CLAUDE.md) > **crawler/**

> **最后更新**：2026-01-31 15:19:33
> **模块类型**：数据采集

## 模块职责

数据采集模块负责从多个平台爬取热榜数据和 RSS 订阅内容。支持 11 个主流热榜平台（今日头条、百度、B站、微博等）和标准 RSS/Atom 订阅源。

## 入口与启动

### 主要入口
- **`fetcher.py`**：热榜数据爬虫
- **`rss/fetcher.py`**：RSS 订阅爬虫
- **`rss/parser.py`**：RSS 解析器

### 使用方式
```python
from trendradar.crawler.fetcher import DataFetcher
from trendradar.crawler.rss.fetcher import RSSFetcher

# 热榜爬取
fetcher = DataFetcher(config)
news_data = await fetcher.crawl_websites()

# RSS 爬取
rss_fetcher = RSSFetcher(config)
rss_data = await rss_fetcher.fetch_all_rss()
```

## 对外接口

### DataFetcher 类

**fetcher.py**
```python
class DataFetcher:
    """热榜数据爬虫"""

    async def crawl_websites(
        self,
        platforms: Optional[List[str]] = None
    ) -> NewsData:
        """爬取所有平台热榜"""

    async def fetch_single_platform(
        self,
        platform_id: str,
        platform_config: Dict
    ) -> Optional[Dict]:
        """爬取单个平台"""

    def get_request_interval(
        self,
        base_interval: float
    ) -> float:
        """获取带抖动的请求间隔"""
```

### RSSFetcher 类

**rss/fetcher.py**
```python
class RSSFetcher:
    """RSS 订阅爬虫"""

    async def fetch_all_rss(
        self,
        feed_ids: Optional[List[str]] = None
    ) -> RSSData:
        """获取所有 RSS 源"""

    async def fetch_single_feed(
        self,
        feed_id: str,
        feed_config: Dict
    ) -> Optional[RSSFeed]:
        """获取单个 RSS 源"""

    def filter_fresh_articles(
        self,
        articles: List[Dict],
        max_age_days: int
    ) -> List[Dict]:
        """过滤新鲜文章"""
```

### 解析函数

**rss/parser.py**
```python
def parse_rss_content(
    raw_content: str,
    feed_id: str
) -> Optional[RSSFeed]:
    """解析 RSS/Atom 内容"""

def extract_publish_time(
    entry: Dict,
    feed_id: str
) -> Optional[datetime]:
    """提取发布时间"""
```

## 关键依赖与配置

### 内部依赖
```
trendradar/
└── crawler/
    ├── fetcher.py       # 热榜爬虫
    └── rss/
        ├── fetcher.py   # RSS 爬虫
        └── parser.py    # RSS 解析
```

### 外部依赖
- **requests**：HTTP 请求
- **feedparser**：RSS 解析

### 支持的平台

| 平台 ID | 平台名称 | API 端点 |
|---------|---------|---------|
| toutiao | 今日头条 | NewsNow API |
| baidu | 百度 | NewsNow API |
| bilibili | B站 | NewsNow API |
| weibo | 微博 | NewsNow API |
| zhihu | 知乎 | NewsNow API |
| wallstreetcn | 华尔街见闻 | NewsNow API |
| thepaper | 澎湃新闻 | NewsNow API |
| cls | 财联社 | NewsNow API |
| ifeng | 凤凰网 | NewsNow API |
| tieba | 贴吧 | NewsNow API |
| douyin | 抖音 | NewsNow API |

### 配置示例
```yaml
crawler:
  request_interval: 1.0      # 基础请求间隔（秒）
  jitter_range: 0.5          # 随机抖动范围
  timeout: 10                # 请求超时（秒）
  retry_times: 3             # 重试次数
  proxy:                     # 代理配置
    enabled: false
    http_proxy: ""
    https_proxy: ""

rss:
  freshness_filter:
    enabled: true
    max_age_days: 3
```

## 数据模型

### NewsData
```python
@dataclass
class NewsData:
    crawl_date: str                # 爬取日期
    crawl_time: str                # 爬取时间
    results: Dict                  # 平台数据
    id_to_name: Dict               # 平台名称映射
    failed_ids: List               # 失败平台列表
```

### RSSData
```python
@dataclass
class RSSData:
    date: str                      # 日期
    feeds: Dict                     # RSS 源数据
    id_to_name: Dict                # 源名称映射
```

### RSSFeed
```python
@dataclass
class RSSFeed:
    feed_id: str                   # 源 ID
    feed_url: str                  # 源 URL
    title: str                     # 源标题
    articles: List[Dict]           # 文章列表
```

## 测试与质量

**当前状态**：未配置测试

**建议测试覆盖**：
- `DataFetcher.crawl_websites()`：爬取流程测试
- `RSSFetcher.fetch_all_rss()`：RSS 获取测试
- 解析器测试
- 重试机制测试

## 常见问题 (FAQ)

### Q1: 如何添加新平台？

**A**: 在 `config.yaml` 添加平台配置，确保 NewsNow API 支持该平台。

### Q2: 如何调整请求速度？

**A**: 修改配置：
```yaml
crawler:
  request_interval: 2.0    # 增加间隔
  jitter_range: 1.0        # 增加抖动
```

### Q3: 如何使用代理？

**A**: 配置代理：
```yaml
crawler:
  proxy:
    enabled: true
    http_proxy: "http://127.0.0.1:7890"
    https_proxy: "http://127.0.0.1:7890"
```

### Q4: RSS 文章重复推送？

**A**: 启用新鲜度过滤：
```yaml
rss:
  freshness_filter:
    enabled: true
    max_age_days: 3
```

## 相关文件清单

- `fetcher.py`：热榜爬虫，约 152 行
- `rss/fetcher.py`：RSS 爬虫，约 156 行
- `rss/parser.py`：RSS 解析器，约 130 行

## 变更记录 (Changelog)

### 2026-01-31 15:19:33
- ✨ 创建模块文档
- 📊 完成接口与配置分析

---

*本文档由 AI 自动生成并维护*

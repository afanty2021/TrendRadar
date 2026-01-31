# trendradar/report - 报告生成模块

[根目录](../../CLAUDE.md) > [trendradar](../CLAUDE.md) > **report/**

> **最后更新**：2026-01-31 15:19:33
> **模块类型**：报告生成

## 模块职责

报告生成模块负责将分析结果转换为可读的报告格式，支持 TXT 文本快照和 HTML 可视化报告两种输出格式。

## 入口与启动

### 主要入口
- **`generator.py`**：报告生成器
- **`formatter.py`**：格式化工具
- **`helpers.py`**：辅助函数
- **`html.py`**：HTML 报告生成
- **`rss_html.py`**：RSS HTML 报告

### 使用方式
```python
from trendradar.report.generator import ReportGenerator

# 创建生成器
generator = ReportGenerator(config, frequency_result, news_data)

# 生成报告
await generator.generate_all()
```

## 对外接口

### ReportGenerator 类

**generator.py**
```python
class ReportGenerator:
    """报告生成器"""

    def __init__(
        self,
        config: Dict[str, Any],
        frequency_result: WordFrequencyResult,
        news_data: NewsData
    ):
        """初始化生成器"""

    async def generate_all(
        self
    ) -> Dict[str, str]:
        """生成所有格式报告"""

    async def generate_txt(
        self
    ) -> str:
        """生成 TXT 报告"""

    async def generate_html(
        self
    ) -> str:
        """生成 HTML 报告"""
```

### 格式化函数

**formatter.py**
```python
def format_keyword_section(
    keyword: str,
    news_list: List[Dict],
    platform_names: Dict[str, str]
) -> str:
    """格式化关键词区块"""

def format_platform_section(
    platform: str,
    news_list: List[Dict]
) -> str:
    """格式化平台区块"""

def format_news_item(
    news: Dict,
    index: int
) -> str:
    """格式化新闻条目"""
```

### HTML 生成

**html.py**
```python
def generate_html_report(
    data: Dict,
    output_path: str
) -> None:
    """生成 HTML 报告"""

def render_keyword_table(
    results: List[WordFrequencyResult]
) -> str:
    """渲染关键词表格"""

def render_platform_section(
    platform: str,
    news_list: List[Dict]
) -> str:
    """渲染平台区块"""
```

## 关键依赖与配置

### 内部依赖
```
trendradar/
└── report/
    ├── generator.py      # 报告生成器
    ├── formatter.py      # 格式化工具
    ├── helpers.py        # 辅助函数
    ├── html.py           # HTML 报告
    └── rss_html.py       # RSS HTML 报告
```

### 外部依赖
- 无特殊外部依赖

### 配置示例
```yaml
report:
  mode: "current"              # daily | current | incremental
  display_mode: "keyword"      # keyword | platform

storage:
  formats:
    txt: true
    html: true
```

## 数据模型

### ReportConfig
```python
@dataclass
class ReportConfig:
    mode: str                  # 报告模式
    display_mode: str          # 显示模式
    output_dir: str            # 输出目录
```

### ReportData
```python
@dataclass
class ReportData:
    crawl_date: str            # 爬取日期
    crawl_time: str            # 爬取时间
    results: List              # 分析结果
    news_data: NewsData        # 新闻数据
```

## 测试与质量

**当前状态**：未配置测试

**建议测试覆盖**：
- `ReportGenerator.generate_all()`：生成流程测试
- 格式化函数测试
- HTML 模板渲染测试

## 常见问题 (FAQ)

### Q1: 如何切换显示模式？

**A**: 修改配置：
```yaml
report:
  display_mode: "platform"  # 按平台显示
```

### Q2: 报告输出位置？

**A**: 默认在 `output/` 目录：
- `output/txt/`：TXT 报告
- `output/html/`：HTML 报告

### Q3: 如何自定义报告样式？

**A**: 修改 `html.py` 中的 HTML 模板

## 相关文件清单

- `generator.py`：报告生成器，约 199 行
- `formatter.py`：格式化工具，约 210 行
- `helpers.py`：辅助函数，约 96 行
- `html.py`：HTML 报告，约 1397 行
- `rss_html.py`：RSS HTML 报告，约 367 行

## 变更记录 (Changelog)

### 2026-01-31 15:19:33
- ✨ 创建模块文档
- 📊 完成接口分析

---

*本文档由 AI 自动生成并维护*

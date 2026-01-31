# trendradar/core - 核心分析模块

[根目录](../../CLAUDE.md) > [trendradar](../CLAUDE.md) > **core/**

> **最后更新**：2026-01-31 15:19:33
> **模块类型**：核心引擎

## 模块职责

核心分析模块是 TrendRadar 的分析引擎，负责配置管理、词频统计、权重计算和关键词过滤。它将原始爬取数据转换为可用于推送和存储的结构化信息。

## 入口与启动

### 主要入口
- **`analyzer.py`**：统计分析器，实现词频统计和权重计算
- **`config.py`**：配置模型定义
- **`data.py`**：数据模型定义
- **`frequency.py`**：频次统计模块
- **`loader.py`**：配置加载器

### 使用方式
```python
from trendradar.core.analyzer import count_word_frequency
from trendradar.core.loader import load_config

# 加载配置
config = load_config("config/config.yaml")

# 词频统计
result = count_word_frequency(news_data, frequency_words, config)
```

## 对外接口

### 分析函数

**analyzer.py**
```python
def count_word_frequency(
    news_data: NewsData,
    frequency_words: FrequencyWords,
    config: Dict[str, Any],
    previous_data: Optional[NewsData] = None
) -> WordFrequencyResult:
    """统计词频并计算权重"""

def calculate_weight(
    rank: int,
    frequency: int,
    hot_value: Optional[int] = None,
    rank_weight: float = 0.6,
    frequency_weight: float = 0.3,
    hot_weight: float = 0.1
) -> float:
    """计算综合权重"""
```

### 配置加载

**loader.py**
```python
def load_config(config_path: str) -> Dict[str, Any]:
    """加载配置文件"""

def load_frequency_words(
    file_path: str
) -> FrequencyWords:
    """加载关键词配置"""

def merge_config_with_env(
    config: Dict[str, Any]
) -> Dict[str, Any]:
    """合并环境变量配置"""
```

### 频次统计

**frequency.py**
```python
def count_platform_frequency(
    all_news: List[Dict]
) -> Dict[str, Any]:
    """统计平台出现频次"""

def get_news_by_keyword(
    all_news: List[Dict],
    keyword: str
) -> List[Dict]:
    """按关键词获取新闻"""
```

## 关键依赖与配置

### 内部依赖
```
trendradar/
└── core/
    ├── analyzer.py      # 统计分析器
    ├── config.py        # 配置模型
    ├── data.py          # 数据模型
    ├── frequency.py     # 频次统计
    └── loader.py        # 配置加载
```

### 外部依赖
- **config/config.yaml**：主配置文件
- **config/frequency_words.txt**：关键词配置

### 权重算法
```
总权重 = 排名权重 × 0.6 + 频次权重 × 0.3 + 热度权重 × 0.1
```

## 数据模型

### WordFrequencyResult
```python
@dataclass
class WordFrequencyResult:
    word: str                      # 关键词
    count: int                     # 出现次数
    platforms: List[str]           # 出现平台
    rank_sum: int                  # 排名总和
    weight: float                  # 综合权重
    news_list: List[Dict]          # 匹配新闻
```

### FrequencyWords
```python
@dataclass
class FrequencyWords:
    must_have: List[str]           # 必须关键词
    keywords: List[str]            # 普通关键词
    filter_words: List[str]        # 过滤关键词
    global_filter: List[str]       # 全局过滤
```

### NewsData
```python
@dataclass
class NewsData:
    crawl_date: str                # 爬取日期
    crawl_time: str                # 爬取时间
    results: Dict                  # 爬取结果
    id_to_name: Dict               # 平台映射
    failed_ids: List               # 失败平台
```

## 测试与质量

**当前状态**：未配置测试

**建议测试覆盖**：
- `count_word_frequency()`：核心算法测试
- `calculate_weight()`：权重计算测试
- 关键词过滤逻辑测试
- 配置加载测试

## 常见问题 (FAQ)

### Q1: 如何调整权重系数？

**A**: 修改配置文件：
```yaml
advanced:
  weight_config:
    rank_weight: 0.6
    frequency_weight: 0.3
    hot_weight: 0.1
```

### Q2: 关键词语法是什么？

**A**: 支持 4 种类型：
- `+前缀`：必须关键词
- 无前缀：普通关键词
- `-前缀`：过滤关键词
- `@前缀`：全局过滤

### Q3: 如何调试分析结果？

**A**: 启用调试模式：
```yaml
advanced:
  debug: true
  save_analysis_result: true
```

## 相关文件清单

- `analyzer.py`：统计分析器，约 719 行
- `config.py`：配置模型，约 115 行
- `data.py`：数据模型，约 251 行
- `frequency.py`：频次统计，约 251 行
- `loader.py`：配置加载，约 478 行

## 变更记录 (Changelog)

### 2026-01-31 15:19:33
- ✨ 创建模块文档
- 📊 完成接口与数据模型分析

---

*本文档由 AI 自动生成并维护*

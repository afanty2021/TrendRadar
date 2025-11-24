[根目录](./CLAUDE.md) > **main.py - 核心爬虫引擎**

# main.py - 核心爬虫引擎

## 模块职责

TrendRadar的核心爬虫引擎，负责从11+主流平台爬取热点新闻，通过智能权重算法排序，支持关键词筛选和多渠道推送。

## 入口与启动

### 主入口函数
```python
def main():
    """主函数 - 执行完整的爬取和推送流程"""
    # 1. 加载配置
    # 2. 爬取数据
    # 3. 数据处理与排序
    # 4. 生成报告
    # 5. 多渠道推送
```

### 启动方式
- **GitHub Actions**: 通过 `.github/workflows/crawler.yml` 定时触发
- **Docker环境**: 通过SuperCronic定时任务启动
- **本地直接运行**: `python main.py`

## 对外接口

### 核心功能函数

#### 数据爬取接口
```python
def fetch_news_from_all_platforms(platforms: List[Dict]) -> Dict[str, List[Dict]]
```
- **功能**: 从配置的所有平台爬取热点数据
- **输入**: 平台配置列表
- **输出**: 按平台分组的新闻数据

#### 数据处理接口
```python
def process_and_rank_news(raw_data: Dict, keywords: List[str]) -> Dict
```
- **功能**: 关键词筛选、权重排序、热点分析
- **算法**: 排名权重60% + 频次权重30% + 热度权重10%

#### 推送接口
```python
def send_notifications(content: str, config: Dict) -> bool
```
- **支持渠道**: 企业微信、飞书、钉钉、Telegram、邮件、ntfy、Bark

### 配置接口
```python
def load_config() -> Dict
def load_keywords() -> List[str]
```

## 关键依赖与配置

### 外部依赖
- **requests**: HTTP请求库，用于爬取各平台数据
- **pytz**: 时区处理，支持多时区推送
- **PyYAML**: 配置文件解析

### 核心配置
- **config/config.yaml**: 主配置文件
  - 爬虫设置：请求间隔、代理配置
  - 推送模式：daily/incremental/current
  - 权重配置：排名/频次/热度权重
  - 通知设置：各平台webhook配置

- **config/frequency_words.txt**: 关键词配置
  - 支持四种语法：普通词、必须词(+)、过滤词(!)、数量限制(@)
  - 词组化管理：空行分隔不同主题

### 平台配置
默认支持11个主流平台：
- 社交媒体：微博、知乎、抖音、贴吧
- 新闻资讯：今日头条、百度热搜、澎湃新闻、凤凰网
- 财经科技：华尔街见闻、财联社热门、bilibili热搜

## 数据模型

### 新闻数据结构
```python
{
    "title": "新闻标题",
    "url": "新闻链接",
    "rank": "排名",
    "hotness": "热度值",
    "platform": "平台名称",
    "timestamp": "抓取时间",
    "is_new": "是否新增"
}
```

### 报告数据结构
```python
{
    "summary": {
        "total_news": "总新闻数",
        "new_news": "新增新闻数",
        "groups": "关键词组数"
    },
    "groups": [
        {
            "keywords": ["关键词组"],
            "count": "匹配数量",
            "news": [新闻列表]
        }
    ],
    "new_topics": [新增话题列表]
}
```

## 测试与质量

### 错误处理机制
- **网络异常**: 自动重试机制，最多3次重试
- **数据异常**: 过滤无效数据，保证程序稳定运行
- **配置异常**: 启动时验证配置文件完整性

### 日志输出
- **INFO**: 正常运行状态、配置加载成功
- **WARNING**: 数据获取失败、配置项缺失
- **ERROR**: 严重错误、程序异常退出

### 性能优化
- **请求控制**: 可配置请求间隔，避免频繁请求
- **数据缓存**: 避免重复处理相同数据
- **分批推送**: 大消息自动分批发送

## 常见问题 (FAQ)

### Q1: 爬虫频率如何设置？
**A**: 在 `config.yaml` 中调整 `request_interval`，建议1000ms以上避免被限制。

### Q2: 推送模式有什么区别？
**A**:
- `daily`: 当日汇总，包含所有匹配新闻
- `current`: 当前榜单，显示实时排名
- `incremental`: 增量监控，仅推送新增内容

### Q3: 关键词配置技巧？
**A**:
- 使用空行分隔不同主题
- +号限定必须词，!号过滤干扰词
- @数字控制显示数量

## 相关文件清单

| 文件路径 | 描述 | 重要性 |
|---------|------|-------|
| `config/config.yaml` | 主配置文件 | ⭐⭐⭐ |
| `config/frequency_words.txt` | 关键词配置 | ⭐⭐⭐ |
| `.github/workflows/crawler.yml` | CI/CD配置 | ⭐⭐ |
| `docker/Dockerfile` | 容器化配置 | ⭐⭐ |
| `requirements.txt` | 依赖管理 | ⭐ |

## 变更记录 (Changelog)

**2025-11-24**: 创建模块文档，详细说明核心功能和接口
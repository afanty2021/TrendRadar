[根目录](../../CLAUDE.md) > [config](../) > **配置管理模块**

# 配置管理模块

## 模块职责

负责TrendRadar项目的所有配置管理，包括系统配置、关键词配置、平台配置等，支持环境变量覆盖和灵活的配置策略。

## 入口与启动

### 配置文件加载
```python
def load_config():
    """加载主配置文件 config/config.yaml"""
    config_path = os.environ.get("CONFIG_PATH", "config/config.yaml")
    # 支持环境变量覆盖
    # 配置验证和默认值设置
```

### 关键词加载
```python
def load_keywords():
    """加载关键词配置 config/frequency_words.txt"""
    # 支持四种语法：普通词、必须词(+)、过滤词(!)、数量限制(@)
    # 词组化管理：空行分隔不同主题
```

## 对外接口

### 配置项接口

#### 应用配置
```yaml
app:
  version_check_url: "版本检查URL"
  show_version_update: true  # 是否显示版本更新提示
```

#### 爬虫配置
```yaml
crawler:
  request_interval: 1000     # 请求间隔(毫秒)
  enable_crawler: true      # 是否启用爬取
  use_proxy: false          # 是否使用代理
  default_proxy: "http://127.0.0.1:10086"
```

#### 报告配置
```yaml
report:
  mode: "daily"             # 推送模式: daily/incremental/current
  rank_threshold: 5         # 排名高亮阈值
  sort_by_position_first: false  # 排序优先级
  max_news_per_keyword: 0   # 每个关键词最大显示数量
```

#### 通知配置
```yaml
notification:
  enable_notification: true
  message_batch_size: 4000
  push_window:
    enabled: false          # 推送时间窗口控制
    time_range:
      start: "20:00"
      end: "22:00"
    once_per_day: true
  webhooks:                # 各平台webhook配置
    feishu_url: ""
    dingtalk_url: ""
    wework_url: ""
    telegram_bot_token: ""
    # ... 其他平台配置
```

### 关键词接口

#### 基础语法支持
- **普通词**: 基础匹配，包含任意一个即可
- **必须词**: `+词汇`，必须同时包含
- **过滤词**: `!词汇`，包含则直接排除
- **数量限制**: `@数字`，限制显示数量

#### 词组功能
- **空行分隔**: 不同主题的词组独立统计
- **权重计算**: 按词组分别计算匹配度和热度

## 关键依赖与配置

### 配置文件依赖
- **PyYAML**: YAML配置文件解析
- **环境变量**: 支持Docker部署时的配置覆盖

### 平台配置
```yaml
platforms:
  - id: "toutiao"
    name: "今日头条"
  - id: "baidu"
    name: "百度热搜"
  - id: "zhihu"
    name: "知乎"
  # ... 更多平台配置
```

### 权重配置
```yaml
weight:
  rank_weight: 0.6         # 排名权重
  frequency_weight: 0.3    # 频次权重
  hotness_weight: 0.1      # 热度权重
```

## 数据模型

### 配置数据模型
```python
class AppConfig:
    version_check_url: str
    show_version_update: bool

class CrawlerConfig:
    request_interval: int
    enable_crawler: bool
    use_proxy: bool
    default_proxy: str

class ReportConfig:
    mode: str              # daily/incremental/current
    rank_threshold: int
    sort_by_position_first: bool
    max_news_per_keyword: int

class NotificationConfig:
    enable_notification: bool
    message_batch_size: int
    push_window: PushWindowConfig
    webhooks: WebhookConfig
```

### 关键词模型
```python
class KeywordGroup:
    keywords: List[str]    # 关键词列表
    must_have: List[str]   # 必须词列表
    must_not: List[str]    # 过滤词列表
    max_count: int         # 最大显示数量
```

## 测试与质量

### 配置验证
- **文件存在性检查**: 启动时验证配置文件是否存在
- **格式验证**: 验证YAML格式和关键词格式
- **参数范围验证**: 检查数值参数的合理范围
- **逻辑验证**: 验证配置间的逻辑关系

### 默认值策略
- **缺失配置**: 为可选配置提供合理默认值
- **类型转换**: 自动转换环境变量到正确类型
- **配置继承**: 支持基础配置和覆盖配置

### 错误处理
- **友好提示**: 配置错误时提供具体的修复建议
- **降级策略**: 部分配置错误时使用默认值继续运行
- **日志记录**: 详细记录配置加载过程和错误信息

## 常见问题 (FAQ)

### Q1: 如何修改推送模式？
**A**: 在 `config.yaml` 中修改 `report.mode`:
- `daily`: 当日汇总模式
- `current`: 当前榜单模式
- `incremental`: 增量监控模式

### Q2: 关键词配置技巧？
**A**:
- 使用空行分隔不同主题
- +号限定必须词提高精度
- !号过滤无关内容
- @数字控制显示数量

### Q3: Docker部署配置不生效？
**A**: 使用环境变量覆盖配置:
```bash
-e REPORT_MODE=daily
-e ENABLE_NOTIFICATION=true
```

### Q4: 如何调整热点权重？
**A**: 修改 `weight` 配置，三个数值之和需等于1.0:
- `rank_weight`: 排名权重，看重新闻的当前热度
- `frequency_weight`: 频次权重，看重持续热度
- `hotness_weight`: 热度权重，看重热度值

## 相关文件清单

| 文件路径 | 描述 | 重要性 |
|---------|------|-------|
| `config/config.yaml` | 主配置文件 | ⭐⭐⭐ |
| `config/frequency_words.txt` | 关键词配置 | ⭐⭐⭐ |
| `config/frequency_words.txt` | 高频词汇表 | ⭐⭐ |

## 变更记录 (Changelog)

**2025-11-24**: 创建配置管理模块文档，详细说明配置项和使用技巧
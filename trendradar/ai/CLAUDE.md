# trendradar/ai - AI 分析模块

[根目录](../../CLAUDE.md) > [trendradar](../CLAUDE.md) > **ai/**

> **最后更新**：2026-01-31 15:19:33
> **模块类型**：AI 服务

## 模块职责

AI 分析模块负责使用大语言模型对新闻数据进行智能分析，包括热点总结、情感分析、趋势提取等功能。基于 LiteLLM 统一接口，支持多种 AI 提供商（DeepSeek、OpenAI、Gemini 等）。

## 入口与启动

### 主要入口
- **`analyzer.py`**：AI 分析器，实现新闻数据分析和简报生成
- **`client.py`**：AI 客户端，封装 LiteLLM 调用
- **`formatter.py`**：结果格式化器，将 AI 返回转换为可读格式
- **`translator.py`**：翻译器，处理多语言内容

### 使用方式
```python
from trendradar.ai.analyzer import AIAnalyzer

# 创建分析器
analyzer = AIAnalyzer(
    provider="deepseek",
    model="deepseek-chat",
    api_key="your_api_key"
)

# 分析新闻
result = await analyzer.analyze(news_data)
```

## 对外接口

### AIAnalyzer 类

**analyzer.py**
```python
class AIAnalyzer:
    """AI 新闻分析器"""

    async def analyze(
        self,
        news_data: Dict[str, Any],
        prompt: Optional[str] = None
    ) -> Dict[str, Any]:
        """分析新闻数据"""

    async def generate_summary(
        self,
        news_list: List[Dict]
    ) -> str:
        """生成简报摘要"""

    async def analyze_sentiment(
        self,
        text: str
    ) -> Dict[str, float]:
        """分析情感倾向"""
```

### AIClient 类

**client.py**
```python
class AIClient:
    """AI 客户端，封装 LiteLLM"""

    def __init__(
        self,
        provider: str,
        model: str,
        api_key: str,
        base_url: Optional[str] = None
    ):
        """初始化客户端"""

    async def chat(
        self,
        messages: List[Dict],
        **kwargs
    ) -> str:
        """发送聊天请求"""

    async def chat_with_stream(
        self,
        messages: List[Dict],
        **kwargs
    ) -> AsyncIterator[str]:
        """流式聊天"""
```

### Formatter 函数

**formatter.py**
```python
def format_analysis_result(
    result: Dict[str, Any]
) -> str:
    """格式化分析结果为文本"""

def to_html_summary(
    analysis: Dict[str, Any]
) -> str:
    """转换为 HTML 格式"""
```

## 关键依赖与配置

### 内部依赖
```
trendradar/
└── ai/
    ├── analyzer.py       # AI 分析器
    ├── client.py         # AI 客户端
    ├── formatter.py      # 结果格式化
    └── translator.py     # 翻译器
```

### 外部依赖
- **litellm**：AI 模型统一接口
- **config/config.yaml**：AI 配置
- **config/ai_analysis_prompt.txt**：AI 分析提示词

### 配置示例
```yaml
ai_analysis:
  enabled: true
  mode: "deepseek-chat"
  model: "deepseek-chat"
  api_key: ""
  api_base: ""
  max_news_for_analysis: 60
  temperature: 0.7
  timeout: 30
```

## 数据模型

### AnalysisResult
```python
@dataclass
class AnalysisResult:
    summary: str              # 总结
    key_events: List[str]     # 关键事件
    sentiment: str            # 情感倾向
    topics: List[str]         # 话题标签
    impact: str               # 影响评估
```

### ChatMessage
```python
@dataclass
class ChatMessage:
    role: str                 # system | user | assistant
    content: str              # 消息内容
```

## 测试与质量

**当前状态**：未配置测试

**建议测试覆盖**：
- `AIAnalyzer.analyze()`：分析功能测试
- `AIClient.chat()`：客户端调用测试
- 错误处理与重试机制测试

## 常见问题 (FAQ)

### Q1: 如何切换 AI 提供商？

**A**: 修改配置文件：
```yaml
ai_analysis:
  mode: "openai"  # deepseek | openai | gemini | custom
  model: "gpt-4"
  api_key: "your_openai_key"
```

### Q2: 如何自定义分析提示词？

**A**: 编辑 `config/ai_analysis_prompt.txt`

### Q3: 成本控制策略？

**A**: 限制分析新闻数量：
```yaml
ai_analysis:
  max_news_for_analysis: 20  # 默认 60
```

## 相关文件清单

- `analyzer.py`：AI 分析器，约 437 行
- `client.py`：AI 客户端，约 96 行
- `formatter.py`：结果格式化，约 308 行
- `translator.py`：翻译器，约 268 行

## 变更记录 (Changelog)

### 2026-01-31 15:19:33
- ✨ 创建模块文档
- 📊 完成接口分析

---

*本文档由 AI 自动生成并维护*

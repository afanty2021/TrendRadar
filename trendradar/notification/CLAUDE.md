# trendradar/notification - 通知推送模块

[根目录](../../CLAUDE.md) > [trendradar](../CLAUDE.md) > **notification/**

> **最后更新**：2026-01-31 15:19:33
> **模块类型**：消息推送

## 模块职责

通知推送模块负责将分析结果通过多种渠道推送给用户。支持 9+ 主流通知渠道（企业微信、飞书、钉钉、Telegram、邮件等），并提供消息格式化、分批发送和推送管理功能。

## 入口与启动

### 主要入口
- **`dispatcher.py`**：通知调度器，统一推送入口
- **`senders.py`**：各渠道发送器实现
- **`renderer.py`**：内容渲染器
- **`splitter.py`**：消息分割器
- **`formatters.py`**：消息格式化
- **`batch.py`**：分批处理
- **`push_manager.py`**：推送管理器

### 使用方式
```python
from trendradar.notification.dispatcher import NotificationDispatcher

# 创建调度器
dispatcher = NotificationDispatcher(config, frequency_result)

# 推送到所有配置的渠道
await dispatcher.dispatch_all()
```

## 对外接口

### NotificationDispatcher 类

**dispatcher.py**
```python
class NotificationDispatcher:
    """通知调度器"""

    def __init__(
        self,
        config: Dict[str, Any],
        frequency_result: WordFrequencyResult
    ):
        """初始化调度器"""

    async def dispatch_all(
        self,
        channels: Optional[List[str]] = None
    ) -> Dict[str, bool]:
        """推送到所有渠道"""

    async def dispatch_single(
        self,
        channel: str
    ) -> bool:
        """推送到单个渠道"""

    def should_push_now(self) -> bool:
        """检查是否应该在当前时间推送"""
```

### 发送器函数

**senders.py**
```python
async def send_to_wechat(
    webhook_url: str,
    content: str,
    msg_type: str = "text"
) -> bool:
    """企业微信推送"""

async def send_to_feishu(
    webhook_url: str,
    content: str
) -> bool:
    """飞书推送"""

async def send_to_dingtalk(
    webhook_url: str,
    content: str,
    secret: Optional[str] = None
) -> bool:
    """钉钉推送"""

async def send_to_telegram(
    bot_token: str,
    chat_id: str,
    content: str
) -> bool:
    """Telegram 推送"""

async def send_to_email(
    smtp_server: str,
    smtp_port: int,
    username: str,
    password: str,
    to_addrs: List[str],
    subject: str,
    content: str
) -> bool:
    """邮件推送"""
```

### 消息渲染

**renderer.py**
```python
class MessageRenderer:
    """消息渲染器"""

    def render_keyword_message(
        self,
        keyword: str,
        news_list: List[Dict]
    ) -> str:
        """渲染关键词消息"""

    def render_summary_message(
        self,
        all_results: List[WordFrequencyResult]
    ) -> str:
        """渲染汇总消息"""

    def render_markdown(
        self,
        data: Dict
    ) -> str:
        """渲染 Markdown 格式"""
```

## 关键依赖与配置

### 内部依赖
```
trendradar/
└── notification/
    ├── dispatcher.py    # 通知调度器
    ├── senders.py       # 发送器实现
    ├── renderer.py      # 内容渲染
    ├── splitter.py      # 消息分割
    ├── formatters.py    # 消息格式化
    ├── batch.py         # 分批处理
    └── push_manager.py  # 推送管理
```

### 外部依赖
- **requests**：HTTP 请求
- **smtplib**：邮件发送

### 支持的渠道

| 渠道 | 配置键 | 多账号 |
|-----|--------|-------|
| 企业微信 | `wechat` | ✅ |
| 飞书 | `feishu` | ✅ |
| 钉钉 | `dingtalk` | ✅ |
| Telegram | `telegram` | ✅ |
| 邮件 | `email` | ✅ |
| ntfy | `ntfy` | ✅ |
| Bark | `bark` | ✅ |
| Slack | `slack` | ✅ |
| Webhook | `webhook` | ✅ |

### 配置示例
```yaml
notification:
  enabled: true

  channels:
    wechat:
      webhook_url: "url1;url2"
    feishu:
      webhook_url: "url"
    telegram:
      bot_token: "token"
      chat_id: "chat1;chat2"
    email:
      smtp_server: "smtp.gmail.com"
      smtp_port: 587
      username: "your@email.com"
      password: "password"
      to_addrs: "recipient1@email.com;recipient2@email.com"

  # 推送时间窗口
  push_window:
    enabled: true
    start: "08:00"
    end: "22:00"

  # 消息分批
  batch:
    enabled: true
    max_length: 2000
    batch_delay: 1
```

## 数据模型

### PushResult
```python
@dataclass
class PushResult:
    channel: str                 # 渠道名称
    success: bool                # 是否成功
    message: str                 # 返回消息
    account_index: int           # 账号索引
```

### BatchConfig
```python
@dataclass
class BatchConfig:
    enabled: bool                # 是否启用
    max_length: int              # 最大长度
    batch_delay: float           # 分批间隔
```

## 测试与质量

**当前状态**：未配置测试

**建议测试覆盖**：
- 各渠道发送器测试
- 消息渲染测试
- 分批逻辑测试
- 推送时间窗口测试

## 常见问题 (FAQ)

### Q1: 消息太长被截断？

**A**: 启用消息分批：
```yaml
notification:
  batch:
    enabled: true
    max_length: 2000
```

### Q2: 如何配置多个账号？

**A**: 使用分号分隔：
```yaml
telegram:
  chat_id: "chat1;chat2;chat3"
```

### Q3: 推送时间不准确？

**A**: 检查时区配置：
```yaml
app:
  timezone: "Asia/Shanghai"
```

### Q4: 钉钉签名验证失败？

**A**: 配置加签密钥：
```yaml
dingtalk:
  secret: "SEC..."
```

## 相关文件清单

- `dispatcher.py`：通知调度器，约 1084 行
- `senders.py`：发送器实现，约 1231 行
- `renderer.py`：内容渲染，约 455 行
- `splitter.py`：消息分割，约 1795 行
- `formatters.py`：消息格式化，约 54 行
- `batch.py`：分批处理，约 86 行
- `push_manager.py`：推送管理，约 81 行

## 变更记录 (Changelog)

### 2026-01-31 15:19:33
- ✨ 创建模块文档
- 📊 完成接口与配置分析

---

*本文档由 AI 自动生成并维护*

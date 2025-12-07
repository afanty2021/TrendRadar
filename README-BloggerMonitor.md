# TrendRadar 博主监控工具

一个简单高效的博主发言监控工具，可以监控特定博主（微博、知乎等）的最新动态，根据关键词过滤并实时推送通知。

## 🌟 功能特点

- **多平台支持**：支持微博、知乎等主流平台
- **关键词过滤**：支持精确匹配和模糊匹配
- **实时推送**：集成 TrendRadar 的推送系统，支持飞书、钉钉、Telegram 等
- **去重机制**：智能去重，避免重复通知
- **灵活配置**：YAML 配置文件，支持多个监控目标
- **轻量级**：基于 RSSHub，无需复杂的登录认证

## 🚀 快速开始

### 1. 初始化配置

```bash
# 进入项目目录
cd TrendRadar

# 初始化博主监控配置文件
python blogger_monitor.py --init-config
```

这会在 `config/` 目录下创建 `blogger_config.yaml` 配置文件。

### 2. 编辑配置文件

编辑 `config/blogger_config.yaml`，添加要监控的博主：

```yaml
# 监控目标列表
monitors:
  # 监控微博用户
  - platform: weibo
    user_id: "1739928273"  # 替换为实际的微博数字ID
    keywords: ["人工智能", "AI"]
    name: "技术博主"

  # 监控知乎用户
  - platform: zhihu
    user_id: "victor-wye"  # 可以是用户名或ID
    keywords: ["创业", "产品"]
    name: "知乎大V"

# 全局关键词
keywords:
  - "热点"
  - "重要"

# 监控间隔（秒）
check_interval: 300
```

### 3. 运行监控

```bash
# 单次运行测试
python blogger_monitor.py --once

# 守护进程模式（持续监控）
python blogger_monitor.py
```

## 📖 详细配置说明

### 获取用户ID

#### 微博用户ID
1. 访问用户主页：https://weibo.com/u/1739928273
2. URL 中的数字部分就是用户ID：`1739928273`

#### 知乎用户ID
1. 访问用户主页：https://www.zhihu.com/people/victor-wye
2. URL 中的用户名部分就是ID：`victor-wye`

### 关键词配置

- **用户特定关键词**：仅对该用户的帖子进行过滤
- **全局关键词**：对所有监控的帖子进行过滤
- 匹配规则：不区分大小写，部分匹配

### 监控参数

- `check_interval`：检查间隔（秒），建议不低于 300 秒（5分钟）
- `max_posts_per_check`：每次检查最多获取的帖子数，建议 5-20

## 🔗 与 TrendRadar 集成

博主监控工具可以完美集成到 TrendRadar 的推送系统中：

### 1. 使用 TrendRadar 的推送渠道

博主监控会自动读取 `config/config.yaml` 中的推送配置，支持：
- 飞书机器人
- 钉钉机器人
- Telegram Bot
- 企业微信机器人

### 2. 数据格式兼容

监控到的博主动态会保存为 TrendRadar 兼容的 JSON 格式：
```bash
output/YYYYMMDD_blogger.json
```

### 3. 统一通知

所有通知（热点新闻 + 博主动态）会通过相同的渠道推送。

## 📁 文件结构

```
TrendRadar/
├── blogger_monitor.py              # 主监控脚本
├── integrations/
│   └── blogger_integration.py     # TrendRadar 集成模块
├── config/
│   └── blogger_config.yaml        # 博主监控配置文件
├── output/
│   ├── blogger_cache.json         # 监控缓存
│   ├── blogger_notifications.json # 通知记录
│   └── YYYYMMDD_blogger.json      # 格式化的博主动态
└── README-BloggerMonitor.md       # 本说明文档
```

## 🛠️ 高级用法

### 1. 批量导入监控目标

创建一个 Python 脚本批量导入：

```python
# import_monitors.py
import yaml

monitors = [
    {"platform": "weibo", "user_id": "123456", "keywords": ["AI"]},
    {"platform": "zhihu", "user_id": "username", "keywords": ["技术"]},
]

with open('config/blogger_config.yaml', 'r') as f:
    config = yaml.safe_load(f)

config['monitors'].extend(monitors)

with open('config/blogger_config.yaml', 'w') as f:
    yaml.dump(config, f)
```

### 2. 自定义通知处理

```python
# custom_notification.py
from integrations.blogger_integration import BloggerToTrendRadarIntegration

integration = BloggerToTrendRadarIntegration()

# 处理新通知
integration.process_new_notifications()

# 自定义通知处理
def custom_handler(posts):
    for post in posts:
        # 自定义处理逻辑
        print(f"发现: {post['title']}")
```

### 3. 定时任务

使用 crontab 设置定时任务：

```bash
# 编辑 crontab
crontab -e

# 添加定时任务（每10分钟检查一次）
*/10 * * * * cd /path/to/TrendRadar && python blogger_monitor.py --once >> /var/log/blogger_monitor.log 2>&1
```

## 🔧 故障排除

### 1. RSSHub 访问失败

如果 RSSHub 公共实例访问不稳定，可以：
- 使用代理访问
- 自建 RSSHub 实例
- 使用其他 RSSHub 镜像

### 2. 用户ID错误

- 微博必须是数字ID，不是昵称
- 知乎可以使用用户名或ID
- 确保用户主页可以正常访问

### 3. 关键词匹配失败

- 检查关键词是否包含特殊字符
- 尝试使用更通用的关键词
- 查看日志了解匹配过程

### 4. 推送通知失败

- 检查 `config/config.yaml` 中的推送配置
- 确认 webhook URL 或 token 配置正确
- 查看日志获取详细错误信息

## 📝 日志

监控程序会生成详细的日志：
- 控制台输出：实时显示监控状态
- 日志文件：`blogger_monitor.log`

日志级别可以通过修改代码中的 `logging.basicConfig` 调整。

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

### 待实现功能
- [ ] 更多平台支持（B站、小红书等）
- [ ] 图文内容解析
- [ ] 语音播报
- [ ] 微信小程序界面
- [ ] 数据统计分析

## 📄 许可证

本项目与 TrendRadar 使用相同的许可证。

## 🆘 帮助

如果遇到问题：
1. 查看日志文件获取详细错误信息
2. 检查配置文件格式是否正确
3. 确认网络连接正常
4. 提交 Issue 寻求帮助

---

*最后更新：2025-12-07*
# get_current_config 工具

<cite>
**本文档引用的文件**
- [config_mgmt.py](file://mcp_server/tools/config_mgmt.py)
- [data_service.py](file://mcp_server/services/data_service.py)
- [config.yaml](file://config/config.yaml)
- [frequency_words.txt](file://config/frequency_words.txt)
- [parser_service.py](file://mcp_server/services/parser_service.py)
- [validators.py](file://mcp_server/utils/validators.py)
</cite>

## 目录
1. [简介](#简介)
2. [核心功能](#核心功能)
3. [配置节详解](#配置节详解)
4. [返回的JSON格式](#返回的json格式)
5. [调用示例](#调用示例)
6. [调试与验证](#调试与验证)
7. [配置文件对应关系](#配置文件对应关系)

## 简介

`get_current_config` 是 TrendRadar MCP Server 提供的一个系统管理工具，用于获取当前系统的运行时配置。该工具通过查询 `config.yaml` 配置文件和 `frequency_words.txt` 关键词文件，将系统配置以结构化的JSON格式返回。这对于调试、验证配置变更以及确认系统当前运行状态至关重要。

此工具是系统自省能力的核心，允许用户和开发者在不直接访问服务器文件系统的情况下，实时检查和确认配置。它在 `server.py` 中被注册为一个MCP工具，可通过HTTP或stdio接口调用。

**Section sources**
- [server.py](file://mcp_server/server.py#L589-L610)

## 核心功能

`get_current_config` 工具的核心功能是根据指定的 `section` 参数，返回系统配置的特定部分。其工作流程如下：
1.  **参数验证**：首先调用 `validate_config_section` 函数验证 `section` 参数的有效性。
2.  **配置获取**：通过 `DataService` 服务获取配置数据。
3.  **结果组装**：根据 `section` 参数，从完整的配置中提取并组装所需的部分。
4.  **返回结果**：将配置信息包装在包含 `success`、`section` 和 `config` 字段的字典中返回。

该工具利用了缓存机制（`CacheService`），对配置进行1小时的缓存，以提高性能并减少对文件系统的频繁读取。

**Section sources**
- [config_mgmt.py](file://mcp_server/tools/config_mgmt.py#L26-L67)
- [data_service.py](file://mcp_server/services/data_service.py#L411-L496)

## 配置节详解

`get_current_config` 工具支持通过 `section` 参数指定返回的配置节。该参数有五种可选值，每种都对应系统配置的一个特定方面。

### all（所有配置）

当 `section` 参数为 `all` 或未指定时，工具返回所有配置节的完整信息。这是默认行为，返回一个包含 `crawler`、`push`、`keywords` 和 `weights` 四个键的字典。

### crawler（爬虫配置）

此配置节返回与新闻爬取相关的设置。它从 `config.yaml` 文件的 `crawler` 和 `platforms` 节点提取信息。

```json
{
  "enable_crawler": true,
  "use_proxy": false,
  "request_interval": 1000,
  "retry_times": 3,
  "platforms": ["toutiao", "baidu", "wallstreetcn-hot", "thepaper", "bilibili-hot-search", "cls-hot", "ifeng", "tieba", "weibo", "douyin", "zhihu"]
}
```

- `enable_crawler`: 是否启用爬虫功能。
- `use_proxy`: 是否使用代理。
- `request_interval`: 请求间隔（毫秒）。
- `retry_times`: 爬取失败时的重试次数（固定为3）。
- `platforms`: 当前配置的新闻平台ID列表。

**Section sources**
- [data_service.py](file://mcp_server/services/data_service.py#L435-L443)

### push（推送配置）

此配置节返回与通知推送相关的设置。它从 `config.yaml` 文件的 `notification` 节点提取信息，并动态检测已配置的推送渠道。

```json
{
  "enable_notification": true,
  "enabled_channels": [],
  "message_batch_size": 4000,
  "push_window": {
    "enabled": false,
    "time_range": {
      "start": "20:00",
      "end": "22:00"
    },
    "once_per_day": true
  }
}
```

- `enable_notification`: 是否启用通知功能。
- `enabled_channels`: 检测到的已配置渠道列表（如 `feishu`, `dingtalk`），通过检查 `webhooks` 下的URL是否为空来确定。
- `message_batch_size`: 消息分批大小（字节）。
- `push_window`: 推送时间窗口配置。

**Section sources**
- [data_service.py](file://mcp_server/services/data_service.py#L444-L461)

### keywords（关键词配置）

此配置节返回用户自定义的关键词配置。它解析 `config/frequency_words.txt` 文件，将文件中的每一行（以 `|` 分隔）视为一个词组。

```json
{
  "word_groups": [
    {
      "required": [],
      "normal": ["胖东来"],
      "filter_words": []
    },
    {
      "required": [],
      "normal": ["于东来"],
      "filter_words": []
    },
    {
      "required": [],
      "normal": ["DeepSeek"],
      "filter_words": []
    },
    {
      "required": [],
      "normal": ["梁文锋"],
      "filter_words": []
    }
  ],
  "total_groups": 4
}
```

- `word_groups`: 一个词组列表，每个词组包含 `required` (必须包含的词，以`+`结尾)、`normal` (普通词) 和 `filter_words` (过滤词，以`!`结尾)。
- `total_groups`: 词组总数。

**Section sources**
- [data_service.py](file://mcp_server/services/data_service.py#L462-L466)
- [parser_service.py](file://mcp_server/services/parser_service.py#L543-L608)

### weights（权重配置）

此配置节返回用于计算新闻热度的权重配置。它从 `config.yaml` 文件的 `weight` 节点提取信息。

```json
{
  "rank_weight": 0.6,
  "frequency_weight": 0.3,
  "hotness_weight": 0.1
}
```

- `rank_weight`: 排名权重。
- `frequency_weight`: 频次权重。
- `hotness_weight`: 热度权重。

这些权重用于算法重新组合不同平台的热搜排序，形成用户侧重的热搜榜单。

**Section sources**
- [data_service.py](file://mcp_server/services/data_service.py#L467-L473)

## 返回的JSON格式

`get_current_config` 工具返回的JSON格式是统一的，无论 `section` 参数为何值。其顶层结构如下：

```json
{
  "success": true,
  "section": "crawler",
  "config": { /* 具体的配置内容 */ }
}
```

- `success`: 布尔值，表示操作是否成功。
- `section`: 字符串，回显请求的配置节名称。
- `config`: 对象，包含实际的配置数据，其结构根据 `section` 的值而变化。

如果请求失败（如参数无效），`success` 将为 `false`，并返回一个包含错误代码和消息的 `error` 对象。

## 调用示例

以下是使用 `get_current_config` 工具的几个典型调用示例：

### 获取当前的关键词配置

```json
{
  "tool": "get_current_config",
  "arguments": {
    "section": "keywords"
  }
}
```

此调用将返回 `frequency_words.txt` 文件中定义的所有关键词组，用于确认系统正在监控哪些话题。

### 获取推送配置

```json
{
  "tool": "get_current_config",
  "arguments": {
    "section": "push"
  }
}
```

此调用将返回推送功能的启用状态、已配置的渠道和推送时间窗口等信息，帮助用户验证通知设置是否正确。

### 获取所有配置

```json
{
  "tool": "get_current_config",
  "arguments": {
    "section": "all"
  }
}
```

此调用将返回完整的系统配置，是进行全面系统检查的首选方法。

## 调试与验证

`get_current_config` 工具在调试和验证配置变更时扮演着至关重要的角色。

1.  **即时验证**：当用户修改了 `config.yaml` 或 `frequency_words.txt` 文件后，无需重启服务，即可通过调用此工具来验证新配置是否已被正确加载。
2.  **状态确认**：在自动化脚本或CI/CD流程中，可以调用此工具来确认部署后的系统配置是否符合预期。
3.  **故障排查**：当系统行为异常时（如未收到推送），可以调用 `get_current_config` 来检查 `push` 配置节，确认 `enable_notification` 是否为 `true` 以及 `webhooks` 是否正确配置。
4.  **环境检查**：在多环境部署（开发、测试、生产）中，可以使用此工具来对比不同环境的配置差异。

通过提供一个标准化的接口来查询配置，`get_current_config` 极大地简化了系统的运维和调试工作。

**Section sources**
- [config.yaml](file://config/config.yaml#L82-L156)
- [frequency_words.txt](file://config/frequency_words.txt)

## 配置文件对应关系

`get_current_config` 工具返回的配置信息直接映射到项目中的两个核心配置文件。

### 与 config.yaml 的对应关系

| 返回的配置项 | 对应的 config.yaml 路径 |
| :--- | :--- |
| `crawler.enable_crawler` | `crawler.enable_crawler` |
| `crawler.use_proxy` | `crawler.use_proxy` |
| `crawler.request_interval` | `crawler.request_interval` |
| `crawler.platforms` | `platforms[*].id` |
| `push.enable_notification` | `notification.enable_notification` |
| `push.message_batch_size` | `notification.message_batch_size` |
| `push.push_window` | `notification.push_window` |
| `weights.rank_weight` | `weight.rank_weight` |
| `weights.frequency_weight` | `weight.frequency_weight` |
| `weights.hotness_weight` | `weight.hotness_weight` |

### 与 frequency_words.txt 的对应关系

`keywords` 配置节直接由 `frequency_words.txt` 文件的内容生成。文件中的每一行对应 `word_groups` 数组中的一个对象。行内的逗号分隔的词根据后缀（`+` 或 `!`）被分类到 `required` 或 `filter_words`，其余则归入 `normal`。

通过理解这种对应关系，用户可以精确地知道如何修改配置文件来改变系统的行为，并通过 `get_current_config` 工具来验证这些修改是否生效。

**Section sources**
- [config.yaml](file://config/config.yaml)
- [frequency_words.txt](file://config/frequency_words.txt)
- [parser_service.py](file://mcp_server/services/parser_service.py#L515-L542)
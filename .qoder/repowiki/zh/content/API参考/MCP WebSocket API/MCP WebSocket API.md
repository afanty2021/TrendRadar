# MCP WebSocket API

<cite>
**本文档引用的文件**  
- [server.py](file://mcp_server/server.py)
- [errors.py](file://mcp_server/utils/errors.py)
- [date_parser.py](file://mcp_server/utils/date_parser.py)
- [analytics.py](file://mcp_server/tools/analytics.py)
- [search_tools.py](file://mcp_server/tools/search_tools.py)
- [config.yaml](file://config/config.yaml)
- [README.md](file://README.md)
</cite>

## 目录
1. [介绍](#介绍)
2. [连接与会话管理](#连接与会话管理)
3. [消息格式](#消息格式)
4. [支持的工具调用](#支持的工具调用)
5. [错误码体系](#错误码体系)
6. [客户端代码示例](#客户端代码示例)
7. [部署与故障排除](#部署与故障排除)

## 介绍
TrendRadar MCP WebSocket API 是一个基于 FastMCP 2.0 实现的生产级工具服务器，通过 WebSocket 协议提供对新闻数据的查询、分析和管理功能。该 API 支持 JSON-RPC 2.0 标准，允许客户端通过自然语言或结构化请求与服务器进行交互，获取实时和历史新闻数据，并执行高级分析任务。

**Section sources**
- [server.py](file://mcp_server/server.py#L1-L25)
- [README.md](file://README.md#L328-L344)

## 连接与会话管理
### WebSocket 连接URL
MCP WebSocket API 的连接URL为 `ws://localhost:3333/mcp`。该服务默认在本地监听 3333 端口，提供 WebSocket 传输模式。

### 握手协议
连接建立时，客户端与服务器之间通过标准的 WebSocket 握手协议进行通信。握手过程由底层的 FastMCP 框架自动处理，客户端无需执行额外的认证或初始化步骤即可开始发送 JSON-RPC 请求。

### 会话管理
会话管理由服务器端自动处理。每个 WebSocket 连接代表一个独立的会话。服务器使用单例模式管理工具实例，确保在会话期间数据访问和分析的一致性。会话在客户端断开连接时自动终止。

**Section sources**
- [server.py](file://mcp_server/server.py#L785-L799)
- [server.py](file://mcp_server/server.py#L23-L27)

## 消息格式
所有消息均遵循 JSON-RPC 2.0 标准，包括请求、响应和错误消息。

### 请求格式
```json
{
  "jsonrpc": "2.0",
  "method": "工具方法名",
  "params": {
    "参数名": "参数值"
  },
  "id": 1
}
```

### 响应格式
成功响应包含 `result` 字段：
```json
{
  "jsonrpc": "2.0",
  "result": "工具返回的JSON字符串",
  "id": 1
}
```

### 错误格式
错误响应包含 `error` 字段：
```json
{
  "jsonrpc": "2.0",
  "error": {
    "code": "错误代码",
    "message": "错误信息",
    "suggestion": "建议"
  },
  "id": 1
}
```

**Section sources**
- [server.py](file://mcp_server/server.py#L44-L110)
- [server.py](file://mcp_server/server.py#L95-L110)

## 支持的工具调用
服务器提供了多个工具方法，涵盖数据查询、高级分析、智能检索和系统管理。

### 数据查询工具
#### `resolve_date_range`
**重要性**: 此工具是前置调用工具，用于将自然语言日期表达式（如“本周”、“最近7天”）解析为精确的日期范围，确保所有AI模型获得一致的计算结果。

**参数**:
- `expression` (str): 自然语言日期表达式。

**返回值**:
```json
{
  "success": true,
  "expression": "本周",
  "date_range": {
    "start": "2025-11-18",
    "end": "2025-11-26"
  },
  "current_date": "2025-11-26",
  "description": "本周（周一到周日，11-18 至 11-26）"
}
```

**示例流程**:
1.  `resolve_date_range("本周")`
2.  `analyze_sentiment(topic="AI", date_range=上一步返回的date_range)`

**Section sources**
- [server.py](file://mcp_server/server.py#L44-L94)
- [date_parser.py](file://mcp_server/utils/date_parser.py#L331-L423)

#### `get_latest_news`
获取最新一批爬取的新闻数据。

**参数**:
- `platforms` (List[str], 可选): 平台ID列表。
- `limit` (int): 返回条数限制，默认50，最大1000。
- `include_url` (bool): 是否包含URL链接，默认False。

**返回值**: JSON格式的新闻列表。

**Section sources**
- [server.py](file://mcp_server/server.py#L115-L150)

#### `get_trending_topics`
获取个人关注词的新闻出现频率统计。

**参数**:
- `top_n` (int): 返回TOP N关注词，默认10。
- `mode` (str): 模式选择，`daily`(当日累计) 或 `current`(最新一批)。

**返回值**: JSON格式的关注词频率统计列表。

**Section sources**
- [server.py](file://mcp_server/server.py#L153-L175)

#### `get_news_by_date`
获取指定日期的新闻数据。

**参数**:
- `date_query` (str, 可选): 日期查询，如“今天”、“昨天”、“2024-01-15”。
- `platforms` (List[str], 可选): 平台ID列表。
- `limit` (int): 返回条数限制，默认50。
- `include_url` (bool): 是否包含URL链接，默认False。

**返回值**: JSON格式的新闻列表。

**Section sources**
- [server.py](file://mcp_server/server.py#L178-L223)

### 高级数据分析工具
#### `analyze_topic_trend`
统一话题趋势分析工具，整合多种分析模式。

**参数**:
- `topic` (str): 话题关键词（必需）。
- `analysis_type` (str): 分析类型，可选值：`trend`, `lifecycle`, `viral`, `predict`。
- `date_range` (Dict[str, str], 可选): 日期范围，格式 `{"start": "YYYY-MM-DD", "end": "YYYY-MM-DD"}`。
- `granularity` (str): 时间粒度，默认`day`。
- `threshold` (float): 热度突增倍数阈值（viral模式），默认3.0。
- `time_window` (int): 检测时间窗口小时数（viral模式），默认24。
- `lookahead_hours` (int): 预测未来小时数（predict模式），默认6。
- `confidence_threshold` (float): 置信度阈值（predict模式），默认0.7。

**使用场景**: 当用户使用“本周”、“最近7天”等自然语言时，必须先调用 `resolve_date_range` 获取精确日期。

**Section sources**
- [server.py](file://mcp_server/server.py#L229-L290)
- [analytics.py](file://mcp_server/tools/analytics.py#L155-L241)

#### `analyze_data_insights`
统一数据洞察分析工具。

**参数**:
- `insight_type` (str): 洞察类型，可选值：`platform_compare`, `platform_activity`, `keyword_cooccur`。
- `topic` (str, 可选): 话题关键词。
- `date_range` (Dict[str, str], 可选): 日期范围。
- `min_frequency` (int): 最小共现频次（keyword_cooccur模式），默认3。
- `top_n` (int): 返回TOP N结果（keyword_cooccur模式），默认20。

**Section sources**
- [server.py](file://mcp_server/server.py#L293-L333)

#### `analyze_sentiment`
分析新闻的情感倾向和热度趋势。

**参数**:
- `topic` (str, 可选): 话题关键词。
- `platforms` (List[str], 可选): 平台ID列表。
- `date_range` (Dict[str, str], 可选): 日期范围。
- `limit` (int): 返回新闻数量，默认50，最大100。
- `sort_by_weight` (bool): 是否按热度权重排序，默认True。
- `include_url` (bool): 是否包含URL链接，默认False。

**使用场景**: 该工具生成用于AI情感分析的结构化提示词，可将返回的 `ai_prompt` 发送给AI进行深度分析。

**Section sources**
- [server.py](file://mcp_server/server.py#L336-L397)
- [analytics.py](file://mcp_server/tools/analytics.py#L630-L798)

#### `find_similar_news`
查找与指定新闻标题相似的其他新闻。

**参数**:
- `reference_title` (str): 新闻标题（完整或部分）。
- `threshold` (float): 相似度阈值，0-1之间，默认0.6。
- `limit` (int): 返回条数限制，默认50，最大100。
- `include_url` (bool): 是否包含URL链接，默认False。

**使用场景**: 用于发现同一事件在不同平台的报道或相似主题的新闻。

**Section sources**
- [server.py](file://mcp_server/server.py#L400-L433)

#### `generate_summary_report`
生成每日/每周摘要报告。

**参数**:
- `report_type` (str): 报告类型，`daily` 或 `weekly`。
- `date_range` (Dict[str, str], 可选): 自定义日期范围。

**返回值**: 包含Markdown格式内容的摘要报告。

**Section sources**
- [server.py](file://mcp_server/server.py#L436-L459)

### 智能检索工具
#### `search_news`
统一搜索接口，支持多种搜索模式。

**参数**:
- `query` (str): 搜索关键词或内容片段。
- `search_mode` (str): 搜索模式，可选值：`keyword`, `fuzzy`, `entity`。
- `date_range` (Dict[str, str], 可选): 日期范围。
- `platforms` (List[str], 可选): 平台ID列表。
- `limit` (int): 返回条数限制，默认50，最大1000。
- `sort_by` (str): 排序方式，可选值：`relevance`, `weight`, `date`。
- `threshold` (float): 相似度阈值（仅fuzzy模式有效），默认0.6。
- `include_url` (bool): 是否包含URL链接，默认False。

**使用场景**: 当用户使用“本周”、“最近7天”等自然语言时，必须先调用 `resolve_date_range` 获取精确日期。

**Section sources**
- [server.py](file://mcp_server/server.py#L464-L540)

#### `search_related_news_history`
基于种子新闻，在历史数据中搜索相关新闻。

**参数**:
- `reference_text` (str): 参考新闻标题。
- `time_preset` (str): 时间范围预设值，可选：`yesterday`, `last_week`, `last_month`, `custom`。
- `threshold` (float): 相关性阈值，0-1之间，默认0.4。
- `limit` (int): 返回条数限制，默认50。
- `include_url` (bool): 是否包含URL链接，默认False。

**Section sources**
- [server.py](file://mcp_server/server.py#L543-L584)
- [search_tools.py](file://mcp_server/tools/search_tools.py#L494-L701)

### 配置与系统管理工具
#### `get_current_config`
获取当前系统配置。

**参数**:
- `section` (str): 配置节，可选值：`all`, `crawler`, `push`, `keywords`, `weights`。

**返回值**: JSON格式的配置信息。

**Section sources**
- [server.py](file://mcp_server/server.py#L589-L609)

#### `get_system_status`
获取系统运行状态和健康检查信息。

**返回值**: JSON格式的系统状态信息。

**Section sources**
- [server.py](file://mcp_server/server.py#L612-L624)
- [system.py](file://mcp_server/tools/system.py#L33-L66)

#### `trigger_crawl`
手动触发一次爬取任务。

**参数**:
- `platforms` (List[str], 可选): 指定平台ID列表。
- `save_to_local` (bool): 是否保存到本地 output 目录，默认 False。
- `include_url` (bool): 是否包含URL链接，默认False。

**返回值**: JSON格式的任务状态信息。

**Section sources**
- [server.py](file://mcp_server/server.py#L627-L659)
- [system.py](file://mcp_server/tools/system.py#L68-L278)

#### `sync_from_remote`
从远程存储拉取数据到本地。

**参数**:
- `days` (int): 拉取最近 N 天的数据，默认 7 天。

**返回值**: JSON格式的同步结果。

**Section sources**
- [server.py](file://mcp_server/server.py#L664-L702)
- [storage_sync.py](file://mcp_server/tools/storage_sync.py#L176-L287)

#### `get_storage_status`
获取存储配置和状态。

**返回值**: JSON格式的存储状态信息。

**Section sources**
- [server.py](file://mcp_server/server.py#L705-L736)
- [storage_sync.py](file://mcp_server/tools/storage_sync.py#L289-L371)

#### `list_available_dates`
列出本地/远程可用的日期范围。

**参数**:
- `source` (str): 数据来源，可选值：`local`, `remote`, `both`。

**返回值**: JSON格式的日期列表。

**Section sources**
- [server.py](file://mcp_server/server.py#L739-L780)
- [storage_sync.py](file://mcp_server/tools/storage_sync.py#L373-L454)

## 错误码体系
服务器定义了多种错误类型，其错误码和消息格式遵循统一标准。

### 常见错误码
- `INTERNAL_ERROR`: 内部错误，表示服务器执行过程中发生未预期的异常。
- `VALIDATION_ERROR`: 验证错误，表示请求参数无效或格式错误。
- `DATA_NOT_FOUND`: 数据不存在，表示在指定范围内未找到匹配的数据。
- `INVALID_PARAMETER`: 参数无效，表示请求参数不符合要求。
- `CONFIGURATION_ERROR`: 配置错误，表示系统配置存在问题。
- `PLATFORM_NOT_SUPPORTED`: 平台不支持，表示请求的平台ID无效。
- `CRAWL_TASK_ERROR`: 爬取任务错误，表示执行爬取任务时发生错误。
- `FILE_PARSE_ERROR`: 文件解析错误，表示解析配置文件失败。
- `REMOTE_NOT_CONFIGURED`: 远程未配置，表示未配置远程存储。

### 错误消息格式
所有错误响应均包含 `code` 和 `message` 字段，部分错误还包含 `suggestion` 字段提供解决方案。

```json
{
  "success": false,
  "error": {
    "code": "ERROR_CODE",
    "message": "错误描述",
    "suggestion": "解决建议"
  }
}
```

**Section sources**
- [errors.py](file://mcp_server/utils/errors.py#L10-L93)
- [server.py](file://mcp_server/server.py#L98-L110)

## 客户端代码示例
以下Python代码示例展示了如何使用 `websockets` 库建立连接、发送请求和处理响应。

```python
import asyncio
import json
import websockets

async def main():
    uri = "ws://localhost:3333/mcp"
    async with websockets.connect(uri) as websocket:
        # 构造请求
        request = {
            "jsonrpc": "2.0",
            "method": "get_latest_news",
            "params": {
                "limit": 5
            },
            "id": 1
        }
        
        # 发送请求
        await websocket.send(json.dumps(request))
        print(f"> {request}")
        
        # 接收响应
        response = await websocket.recv()
        print(f"< {response}")

if __name__ == "__main__":
    asyncio.run(main())
```

**Section sources**
- [README.md](file://README.md#L330-L334)

## 部署与故障排除
### 连接地址差异
- **本地部署**: 连接地址为 `ws://localhost:3333/mcp`。
- **Docker部署**: 如果MCP服务在Docker容器内运行，且已将端口3333映射到宿主机，则连接地址为 `ws://宿主机IP:3333/mcp`。例如，若宿主机IP为 `192.168.1.100`，则地址为 `ws://192.168.1.100:3333/mcp`。

### 故障排除
#### 连接被拒绝
- **原因**: 服务器未启动或端口未正确监听。
- **解决方案**: 
  1.  确认 `mcp_server` 服务已成功启动。
  2.  检查 `docker-compose.yml` 文件中端口映射是否正确（如 `3333:3333`）。
  3.  使用 `netstat -an | grep 3333` 或 `lsof -i :3333` 命令检查端口占用情况。

#### 认证失败
- **说明**: 本API目前不涉及认证失败问题，因为连接建立无需认证。
- **可能问题**: 如果客户端在发送请求后收到 `INTERNAL_ERROR`，请检查请求的 `method` 名称是否拼写正确，或参数是否符合要求。

**Section sources**
- [README.md](file://README.md#L443-L448)
- [docker-compose.yml](file://docker/docker-compose.yml)
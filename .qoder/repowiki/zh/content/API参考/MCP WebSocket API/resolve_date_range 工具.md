# resolve_date_range 工具

<cite>
**本文档引用文件**   
- [server.py](file://mcp_server/server.py#L44-L110)
- [date_parser.py](file://mcp_server/utils/date_parser.py#L331-L423)
- [README-MCP-FAQ.md](file://README-MCP-FAQ.md#L535-L587)
</cite>

## 目录
1. [简介](#简介)
2. [核心作用与优先调用原因](#核心作用与优先调用原因)
3. [参数与支持格式](#参数与支持格式)
4. [返回的JSON结构](#返回的json结构)
5. [实际调用示例](#实际调用示例)
6. [确保日期计算一致性](#确保日期计算一致性)
7. [Python客户端代码示例](#python客户端代码示例)

## 简介
`resolve_date_range` 是 TrendRadar MCP 服务中的一个核心工具，专门用于将用户输入的自然语言日期表达式（如“本周”、“最近7天”）解析为精确、标准化的日期范围。该工具作为前置调用工具，旨在解决AI模型自行计算日期时可能产生的不一致问题，确保所有下游分析工具（如情感分析、趋势分析）都能基于统一、准确的时间范围进行计算。

**Section sources**
- [server.py](file://mcp_server/server.py#L44-L110)
- [README-MCP-FAQ.md](file://README-MCP-FAQ.md#L535-L587)

## 核心作用与优先调用原因
该工具的核心作用是充当一个**日期解析的权威服务器**。当用户使用“本周”、“昨天”、“最近30天”等相对性、模糊性的自然语言描述日期时，不同的AI模型或不同的调用时间可能会计算出不同的具体日期范围，导致分析结果出现偏差。

通过优先调用 `resolve_date_range`，AI可以将模糊的日期请求委托给服务器端进行精确计算。服务器使用其系统时间（`datetime.now()`）和统一的逻辑来确定日期范围，从而保证了：
1.  **一致性**：无论哪个AI模型调用，只要输入相同的表达式，返回的日期范围都完全相同。
2.  **准确性**：计算逻辑集中管理，避免了客户端计算错误。
3.  **标准化**：返回的日期格式统一为 `YYYY-MM-DD`，可直接用于其他工具。

因此，文档强烈推荐在任何需要处理自然语言日期的场景下，首先调用此工具获取精确的 `date_range` 对象，再将其传递给 `analyze_sentiment`、`search_news` 等分析工具。

**Section sources**
- [server.py](file://mcp_server/server.py#L49-L54)
- [README-MCP-FAQ.md](file://README-MCP-FAQ.md#L546-L548)

## 参数与支持格式
该工具接受一个名为 `expression` 的字符串参数，支持多种中文和英文的自然语言日期表达式。

### 支持的表达式格式
| 类型 | 中文表达式 | 英文表达式 |
| :--- | :--- | :--- |
| **单日** | 今天、昨天 | today, yesterday |
| **周** | 本周、这周、上周 | this week, current week, last week |
| **月** | 本月、这个月、上月、上个月 | this month, current month, last month |
| **最近N天** | 最近7天、最近30天、最近一周、过去一个月 | last 7 days, last 30 days, past week, past month |
| **动态天数** | 最近N天（例如：最近5天、最近10天） | last N days (e.g., last 5 days, last 10 days) |

**Section sources**
- [date_parser.py](file://mcp_server/utils/date_parser.py#L32-L58)
- [README-MCP-FAQ.md](file://README-MCP-FAQ.md#L552-L558)

## 返回的JSON结构
调用 `resolve_date_range` 工具后，将返回一个JSON格式的字符串，其结构如下：

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

### 字段说明
- **`success`**: 布尔值，表示解析是否成功。
- **`expression`**: 用户输入的原始表达式。
- **`date_range`**: 包含 `start` 和 `end` 两个字段的对象，表示解析出的精确日期范围，格式为 `YYYY-MM-DD`。
- **`current_date`**: 服务器执行解析时的当前日期，格式为 `YYYY-MM-DD`。
- **`description`**: 对解析结果的文本描述，便于人类理解。

**Section sources**
- [server.py](file://mcp_server/server.py#L71-L79)
- [README-MCP-FAQ.md](file://README-MCP-FAQ.md#L562-L572)

## 实际调用示例
以下是一个典型的调用流程，展示了如何在分析任务中使用 `resolve_date_range`。

### 场景：分析AI本周的情感倾向
1.  **用户请求**：“分析AI本周的情感倾向”
2.  **AI调用 `resolve_date_range`**：
    ```python
    # 伪代码
    result = resolve_date_range("本周")
    # 返回: {"date_range": {"start": "2025-11-18", "end": "2025-11-26"}, ...}
    ```
3.  **AI调用 `analyze_sentiment`**：
    ```python
    # 伪代码
    date_range = result["date_range"]  # 使用上一步的返回值
    sentiment_result = analyze_sentiment(topic="AI", date_range=date_range)
    ```

这个流程确保了情感分析工具接收到的 `date_range` 是经过服务器精确计算的，而不是由AI模型自行估算的。

**Section sources**
- [server.py](file://mcp_server/server.py#L83-L87)
- [README-MCP-FAQ.md](file://README-MCP-FAQ.md#L578-L587)

## 确保日期计算一致性
AI模型自行计算日期（如“本周”）时，可能因为时区、计算逻辑或调用时间的微小差异而产生不同的结果。例如，一个模型可能将“本周”定义为周一到周日，而另一个模型可能定义为周日到周六。

`resolve_date_range` 工具通过在**服务器端集中计算**解决了这个问题。它使用统一的逻辑（例如，本周从周一算起）和服务器的系统时间，为所有请求提供一致的输出。这消除了跨模型、跨会话的计算偏差，保证了数据分析的可靠性和可重复性。

**Section sources**
- [server.py](file://mcp_server/server.py#L51-L54)
- [README-MCP-FAQ.md](file://README-MCP-FAQ.md#L546-L548)

## Python客户端代码示例
以下是一个使用Python `requests` 库调用 `resolve_date_range` 工具的JSON-RPC 2.0客户端代码片段。

```python
import requests
import json

def call_resolve_date_range(expression):
    """
    调用 resolve_date_range 工具
    
    Args:
        expression (str): 自然语言日期表达式，如 "本周", "最近7天"
    
    Returns:
        dict: 解析结果的字典
    """
    # MCP 服务器的HTTP地址
    url = "http://localhost:3333"  # 或您的服务器地址
    
    # JSON-RPC 2.0 请求体
    payload = {
        "jsonrpc": "2.0",
        "method": "resolve_date_range",  # 方法名
        "params": {
            "expression": expression  # 传入参数
        },
        "id": 1  # 请求ID
    }
    
    headers = {
        "Content-Type": "application/json"
    }
    
    try:
        # 发送POST请求
        response = requests.post(url, data=json.dumps(payload), headers=headers)
        response.raise_for_status()  # 检查HTTP错误
        
        # 解析JSON响应
        result = response.json()
        
        # 检查RPC错误
        if "error" in result:
            raise Exception(f"RPC Error: {result['error']}")
        
        # 返回结果（result['result'] 是一个JSON字符串，需要再次解析）
        return json.loads(result["result"])
        
    except requests.exceptions.RequestException as e:
        print(f"请求失败: {e}")
        return None
    except json.JSONDecodeError as e:
        print(f"JSON解析失败: {e}")
        return None

# 使用示例
if __name__ == "__main__":
    # 调用工具解析“本周”
    result = call_resolve_date_range("本周")
    if result and result.get("success"):
        print(f"表达式: {result['expression']}")
        print(f"日期范围: {result['date_range']['start']} 至 {result['date_range']['end']}")
        print(f"描述: {result['description']}")
    else:
        print("解析失败")
```

**Section sources**
- [server.py](file://mcp_server/server.py#L44-L110)
- [requirements.txt](file://requirements.txt#L1)
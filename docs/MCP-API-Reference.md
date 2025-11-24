# TrendRadar MCP API 参考文档

## 概述

TrendRadar MCP (Model Context Protocol) 服务器提供16种智能分析工具，支持AI客户端通过标准协议进行新闻数据的查询、分析和可视化。

## 连接信息

- **协议版本**: MCP 2.0
- **服务器名称**: trendradar-news
- **传输模式**: STDIO (推荐) / HTTP
- **HTTP端点**: `http://localhost:3333/mcp`

## API 分类

### 🔍 基础查询工具 (Basic Query Tools)

#### 1. get_latest_news

获取最新一批爬取的新闻数据。

**参数**
- `platforms` (可选): 平台ID列表，如 `["zhihu", "weibo"]`
- `limit` (可选): 返回条数限制，默认50，最大200
- `include_url` (可选): 是否包含URL链接，默认false

**返回示例**
```json
{
  "success": true,
  "news": [
    {
      "title": "人工智能技术获重大突破",
      "platform": "zhihu",
      "platform_name": "知乎",
      "rank": 1,
      "ranks": [1, 2, 3],
      "count": 3,
      "url": "https://example.com/news/1",
      "mobileUrl": "https://m.example.com/news/1"
    }
  ],
  "total": 1,
  "platforms": ["zhihu"]
}
```

#### 2. get_news_by_date

按日期查询新闻，支持自然语言日期。

**参数**
- `date_query` (可选): 日期查询字符串，默认"今天"
  - 相对日期: "今天"、"昨天"、"前天"、"3天前"
  - 绝对日期: "2025-10-10"、"10月10日"
- `platforms` (可选): 平台ID列表
- `limit` (可选): 返回条数限制，默认50
- `include_url` (可选): 是否包含URL链接

**示例调用**
```python
# 查询今天的新闻
get_news_by_date()

# 查询昨天的知乎新闻
get_news_by_date(date_query="昨天", platforms=["zhihu"], limit=20)
```

#### 3. get_trending_topics

获取个人关注词的出现频率统计。

**参数**
- `top_n` (可选): 返回TOP N关注词，默认10，最大50
- `mode` (可选): 统计模式，默认"current"
  - "daily": 当日累计统计
  - "current": 最新一批数据
  - "incremental": 增量统计

**返回示例**
```json
{
  "success": true,
  "topics": [
    {
      "word": "人工智能",
      "count": 15,
      "platforms": ["zhihu", "weibo"],
      "sample_titles": ["AI技术突破...", "人工智能应用..."]
    }
  ],
  "total_words": 10,
  "mode": "current"
}
```

### 🔎 智能检索工具 (Smart Search Tools)

#### 4. search_news_unified

统一新闻搜索工具，支持多种搜索模式。

**参数**
- `query` (必需): 查询内容
- `search_mode` (可选): 搜索模式，默认"keyword"
  - "keyword": 精确关键词匹配
  - "fuzzy": 模糊内容匹配
  - "entity": 实体名称搜索
- `date_range` (可选): 日期范围 `{"start": "2025-01-01", "end": "2025-01-07"}`
- `platforms` (可选): 平台过滤列表
- `limit` (可选): 返回条数限制，默认50
- `sort_by` (可选): 排序方式，默认"relevance"
  - "relevance": 按相关度排序
  - "weight": 按新闻权重排序
  - "date": 按日期排序
- `threshold` (可选): 相似度阈值(0-1)，默认0.6
- `include_url` (可选): 是否包含URL链接

**示例调用**
```python
# 关键词搜索
search_news_unified(query="人工智能", search_mode="keyword")

# 模糊搜索
search_news_unified(query="AI技术", search_mode="fuzzy", threshold=0.5)

# 实体搜索
search_news_unified(query="马斯克", search_mode="entity")
```

#### 5. search_related_news_history

在历史数据中搜索与给定新闻相关的新闻。

**参数**
- `reference_text` (必需): 参考新闻标题或内容
- `time_preset` (可选): 时间范围预设，默认"yesterday"
  - "yesterday": 昨天
  - "last_week": 上周(7天)
  - "last_month": 上个月(30天)
  - "custom": 自定义日期范围
- `start_date` (可选): 自定义开始日期
- `end_date` (可选): 自定义结束日期
- `threshold` (可选): 相似度阈值(0-1)，默认0.4
- `limit` (可选): 返回条数限制，默认50
- `include_url` (可选): 是否包含URL链接

### 📊 高级分析工具 (Advanced Analytics Tools)

#### 6. analyze_topic_trend_unified

统一话题趋势分析，整合多种分析模式。

**参数**
- `topic` (必需): 话题关键词
- `analysis_type` (可选): 分析类型，默认"trend"
  - "trend": 热度趋势分析
  - "lifecycle": 生命周期分析
  - "viral": 异常热度检测
  - "predict": 话题预测
- `date_range` (可选): 日期范围
- `granularity` (可选): 时间粒度，默认"day"
- `threshold` (可选): 热度突增倍数阈值，默认3.0
- `time_window` (可选): 检测时间窗口小时数，默认24
- `lookahead_hours` (可选): 预测未来小时数，默认6
- `confidence_threshold` (可选): 置信度阈值，默认0.7

**示例调用**
```python
# 趋势分析
analyze_topic_trend_unified(topic="人工智能", analysis_type="trend")

# 生命周期分析
analyze_topic_trend_unified(topic="iPhone", analysis_type="lifecycle")

# 异常检测
analyze_topic_trend_unified(analysis_type="viral", threshold=3.0)

# 趋势预测
analyze_topic_trend_unified(analysis_type="predict", lookahead_hours=12)
```

#### 7. analyze_data_insights_unified

统一数据洞察分析。

**参数**
- `insight_type` (必需): 洞察类型
  - "platform_compare": 平台对比分析
  - "platform_activity": 平台活跃度统计
  - "keyword_cooccur": 关键词共现分析
- `topic` (可选): 话题关键词（platform_compare模式）
- `date_range` (可选): 日期范围
- `min_frequency` (可选): 最小共现频次，默认3
- `top_n` (可选): 返回TOP N结果，默认20

#### 8. analyze_sentiment

情感倾向分析，生成AI提示词。

**参数**
- `topic` (可选): 话题关键词，只分析包含该关键词的新闻
- `platforms` (可选): 平台过滤列表
- `date_range` (可选): 日期范围
- `limit` (可选): 返回新闻数量限制，默认50，最大100
- `sort_by_weight` (可选): 是否按权重排序，默认true
- `include_url` (可选): 是否包含URL链接，默认false

**返回示例**
```json
{
  "success": true,
  "method": "ai_prompt_generation",
  "summary": {
    "total_found": 25,
    "returned_count": 20,
    "topic": "人工智能",
    "platforms": ["zhihu", "weibo"]
  },
  "ai_prompt": "请分析以下关于「人工智能」的新闻标题的情感倾向...",
  "news_sample": [...],
  "usage_note": "请将 ai_prompt 字段的内容发送给 AI 进行情感分析"
}
```

#### 9. find_similar_news

基于标题相似度查找相关新闻。

**参数**
- `reference_title` (必需): 参考标题
- `threshold` (可选): 相似度阈值(0-1)，默认0.6
- `limit` (可选): 返回条数限制，默认50
- `include_url` (可选): 是否包含URL链接

#### 10. search_by_entity

实体识别搜索。

**参数**
- `entity` (必需): 实体名称
- `entity_type` (可选): 实体类型
  - "person": 人物
  - "location": 地点
  - "organization": 机构
- `limit` (可选): 返回条数限制，默认50，最大200
- `sort_by_weight` (可选): 是否按权重排序，默认true

#### 11. generate_summary_report

自动生成热点摘要报告。

**参数**
- `report_type` (可选): 报告类型，默认"daily"
  - "daily": 每日报告
  - "weekly": 每周报告
- `date_range` (可选): 自定义日期范围

**返回示例**
```json
{
  "success": true,
  "report_type": "daily",
  "date_range": {
    "start": "2025-01-17",
    "end": "2025-01-17"
  },
  "markdown_report": "# 每日新闻热点摘要\n\n**报告日期**: 2025-01-17\n...",
  "statistics": {
    "total_news": 387,
    "platforms_count": 8,
    "top_keyword": {"人工智能": 25}
  }
}
```

#### 12. detect_viral_topics

异常热度检测，识别突然爆火的话题。

**参数**
- `threshold` (可选): 热度突增倍数阈值，默认3.0
- `time_window` (可选): 检测时间窗口小时数，默认24，最大72

**返回示例**
```json
{
  "success": true,
  "viral_topics": [
    {
      "keyword": "突发新闻",
      "current_count": 15,
      "previous_count": 2,
      "growth_rate": 7.5,
      "sample_titles": [...],
      "alert_level": "高"
    }
  ],
  "total_detected": 1,
  "threshold": 3.0,
  "detection_time": "2025-01-17 14:30:00"
}
```

#### 13. predict_trending_topics

基于历史数据预测未来热点。

**参数**
- `lookahead_hours` (可选): 预测未来小时数，默认6，最大48
- `confidence_threshold` (可选): 置信度阈值，默认0.7

### ⚙️ 系统管理工具 (System Management Tools)

#### 14. get_current_config

获取当前系统配置。

**参数**
- `section` (可选): 配置节，默认"all"
  - "all": 所有配置
  - "crawler": 爬虫配置
  - "push": 推送配置
  - "keywords": 关键词配置
  - "weights": 权重配置

#### 15. get_system_status

获取系统运行状态和健康检查。

**返回示例**
```json
{
  "success": true,
  "system": {
    "version": "3.3.0",
    "status": "healthy",
    "uptime": "2 days, 14 hours",
    "memory_usage": "45.2 MB"
  },
  "data": {
    "available_date_range": {
      "start": "2025-01-10",
      "end": "2025-01-17"
    },
    "total_news_count": 15420,
    "platforms_count": 8
  },
  "cache": {
    "total_entries": 25,
    "hit_rate": "78%"
  }
}
```

#### 16. trigger_crawl

手动触发爬取任务。

**参数**
- `platforms` (可选): 指定平台列表，为空则爬取所有平台
- `save_to_local` (可选): 是否保存到本地output目录，默认false
- `include_url` (可选): 是否包含URL链接，默认false

**返回示例**
```json
{
  "success": true,
  "task_id": "crawl_1642425600",
  "status": "completed",
  "crawl_time": "2025-01-17 14:30:00",
  "platforms": ["zhihu", "weibo"],
  "total_news": 45,
  "failed_platforms": [],
  "data": [...],
  "saved_to_local": true,
  "saved_files": {
    "txt": "/path/to/output/2025年01月17日/txt/14时30分.txt",
    "html": "/path/to/output/2025年01月17日/html/14时30分.html"
  }
}
```

## 错误处理

所有API都遵循统一的错误响应格式：

```json
{
  "success": false,
  "error": {
    "code": "ERROR_CODE",
    "message": "错误描述",
    "suggestion": "解决建议",
    "details": {}
  }
}
```

### 常见错误码

- `INVALID_PARAMETER`: 参数无效
- `DATA_NOT_FOUND`: 数据未找到
- `CRAWL_TASK_ERROR`: 爬虫任务错误
- `INTERNAL_ERROR`: 内部错误
- `NO_DATA_AVAILABLE`: 没有可用数据

## 使用示例

### Python 客户端示例

```python
import asyncio
from mcp import Client

async def main():
    client = Client()
    await client.connect_stdio(["uv", "run", "python", "-m", "mcp_server.server"])

    # 获取最新新闻
    result = await client.call_tool("get_latest_news", {
        "platforms": ["zhihu"],
        "limit": 10
    })
    print(result)

    # 分析话题趋势
    trend_result = await client.call_tool("analyze_topic_trend_unified", {
        "topic": "人工智能",
        "analysis_type": "trend",
        "date_range": {"start": "2025-01-10", "end": "2025-01-17"}
    })
    print(trend_result)

asyncio.run(main())
```

### JavaScript 客户端示例

```javascript
import { MCPClient } from '@modelcontextprotocol/client';

const client = new MCPClient();
await client.connectToProcess(['uv', 'run', 'python', '-m', 'mcp_server.server']);

// 获取系统状态
const status = await client.callTool('get_system_status', {});
console.log('系统状态:', status);

// 搜索新闻
const searchResult = await client.callTool('search_news_unified', {
  query: '人工智能',
  search_mode: 'keyword',
  limit: 20
});
console.log('搜索结果:', searchResult);
```

## 性能优化建议

1. **合理使用limit参数**: 避免一次性获取过多数据
2. **启用缓存**: 系统会自动缓存常用查询结果
3. **分批处理大数据**: 使用date_range分批查询历史数据
4. **选择合适的搜索模式**:
   - 精确匹配使用"keyword"模式
   - 模糊搜索使用"fuzzy"模式
   - 实体搜索使用"entity"模式
5. **定期清理缓存**: 系统会自动清理过期缓存

## 更新日志

- **v1.0.0**: 初始版本，提供16种分析工具
- **v1.1.0**: 新增HTTP传输模式支持
- **v1.2.0**: 增强缓存机制和性能优化
- **v1.3.0**: 添加预测和异常检测功能
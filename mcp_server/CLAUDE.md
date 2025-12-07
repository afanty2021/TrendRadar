[根目录](../../CLAUDE.md) > [mcp_server](../) > **MCP AI分析服务**

# MCP AI分析服务

## 模块职责

基于FastMCP 2.0框架构建的MCP(Model Context Protocol)服务器，提供16种智能分析工具，支持AI客户端通过自然语言与新闻数据进行深度交互分析。

## 入口与启动

### 主服务入口
```python
# mcp_server/server.py
mcp = FastMCP('trendradar-news')

# 支持两种传输模式
# STDIO模式：用于本地客户端连接
# HTTP模式：用于远程客户端连接
```

### 启动方式

#### STDIO模式（推荐）
```bash
uv run python -m mcp_server.server
```

#### HTTP模式
```bash
uv run python -m mcp_server.server --transport http --host 0.0.0.0 --port 3333
# 或使用便捷脚本
./start-http.sh  # Linux/macOS
start-http.bat   # Windows
```

### 连接配置
- **Cherry Studio**: GUI界面配置，5分钟快速部署
- **Claude Desktop**: 配置文件方式连接
- **Cursor**: 项目级MCP配置
- **Claude Code CLI**: 命令行添加服务器

## 对外接口

### 16种分析工具详细说明

#### 🔍 基础查询工具 (3种)

**1. get_latest_news**
- **功能**: 获取最新一批爬取的新闻数据
- **参数**: platforms(平台列表), limit(返回数量), include_url(是否包含链接)
- **返回**: 新闻列表，包含标题、平台、排名等信息
- **用途**: 快速查看最新热点新闻

**2. get_news_by_date**
- **功能**: 按日期查询新闻，支持自然语言日期
- **参数**: date_query(日期查询，支持"今天"、"昨天"等), platforms, limit
- **返回**: 指定日期的新闻列表
- **用途**: 查看特定日期的历史新闻

**3. get_trending_topics**
- **功能**: 获取个人关注词的出现频率统计
- **参数**: top_n(TOP N数量), mode(daily/current/incremental)
- **返回**: 关注词频率统计
- **用途**: 监控个人关注话题的热度变化

#### 🔎 智能检索工具 (2种)

**4. search_news_unified**
- **功能**: 统一新闻搜索工具，支持多种搜索模式
- **参数**: query(查询内容), search_mode(keyword/fuzzy/entity), date_range, platforms
- **返回**: 匹配的新闻列表，按相关度排序
- **用途**: 灵活搜索相关新闻

**5. search_related_news_history**
- **功能**: 在历史数据中搜索与给定新闻相关的新闻
- **参数**: reference_text(参考文本), time_preset(时间范围), threshold(相似度阈值)
- **返回**: 相关新闻列表，包含相似度评分
- **用途**: 发现新闻的关联性和发展趋势

#### 📊 高级分析工具 (8种)

**6. analyze_topic_trend_unified**
- **功能**: 统一话题趋势分析，整合多种分析模式
- **参数**: topic(话题), analysis_type(trend/lifecycle/viral/predict), date_range
- **返回**: 话题趋势分析结果
- **用途**: 深度分析话题的发展趋势和热度变化

**7. analyze_data_insights_unified**
- **功能**: 统一数据洞察分析
- **参数**: insight_type(platform_compare/platform_activity/keyword_cooccur)
- **返回**: 数据洞察分析结果
- **用途**: 发现数据背后的规律和洞察

**8. analyze_sentiment**
- **功能**: 情感倾向分析，生成AI提示词
- **参数**: topic(话题), platforms, date_range, limit
- **返回**: 结构化的AI提示词和新闻数据
- **用途**: 利用AI分析新闻情感倾向

**9. find_similar_news**
- **功能**: 基于标题相似度查找相关新闻
- **参数**: reference_title(参考标题), threshold(相似度阈值), limit
- **返回**: 相似新闻列表
- **用途**: 发现相似报道和相关新闻

**10. search_by_entity**
- **功能**: 实体识别搜索
- **参数**: entity(实体名称), entity_type(person/location/organization), limit
- **返回**: 实体相关新闻
- **用途**: 搜索特定人物、地点或机构的新闻

**11. generate_summary_report**
- **功能**: 自动生成热点摘要报告
- **参数**: report_type(daily/weekly), date_range
- **返回**: Markdown格式的摘要报告
- **用途**: 快速生成新闻热点总结

**12. detect_viral_topics**
- **功能**: 异常热度检测，识别突然爆火的话题
- **参数**: threshold(热度突增倍数), time_window(检测时间窗口)
- **返回**: 爆火话题列表
- **用途**: 预警可能的重大事件

**13. predict_trending_topics**
- **功能**: 基于历史数据预测未来热点
- **参数**: lookahead_hours(预测时间), confidence_threshold(置信度)
- **返回**: 预测的潜力话题列表
- **用途**: 早期发现潜力热点话题

#### ⚙️ 系统管理工具 (3种)

**14. get_current_config**
- **功能**: 获取当前系统配置
- **参数**: section(配置节)
- **返回**: 配置信息
- **用途**: 查看系统运行配置

**15. get_system_status**
- **功能**: 获取系统运行状态和健康检查
- **参数**: 无
- **返回**: 系统状态信息
- **用途**: 监控系统运行状况

**16. trigger_crawl**
- **功能**: 手动触发爬取任务
- **参数**: platforms(指定平台), save_to_local(是否保存)
- **返回**: 爬取结果和保存路径
- **用途**: 临时爬取最新数据

### 工具特性
- **异步支持**: 所有工具支持async/await
- **参数验证**: 自动验证输入参数合法性
- **错误处理**: 完善的异常处理和错误提示
- **数据缓存**: 智能缓存机制提升查询性能
- **分页支持**: 大数据集自动分页处理
- **多种排序**: 支持按相关度、权重、日期等排序

## 关键依赖与配置

### 核心依赖
- **fastmcp>=2.12.0**: MCP 2.0协议实现
- **websockets>=13.0**: WebSocket通信支持
- **requests>=2.32.5**: HTTP请求库
- **pytz>=2025.2**: 时区处理
- **PyYAML>=6.0.3**: 配置文件解析

### 项目配置
- **pyproject.toml**: Python项目配置，定义依赖和脚本
- **requirements.txt**: 依赖包列表
- **setup-*.sh/setup-*.bat**: 跨平台部署脚本

### 模块结构
```
mcp_server/
├── server.py              # MCP服务器主入口，注册所有工具
├── tools/                 # 分析工具模块
│   ├── __init__.py       # 工具模块初始化
│   ├── data_query.py     # 基础查询工具 (3种)
│   ├── analytics.py      # 高级分析工具 (8种)
│   ├── search_tools.py   # 智能检索工具 (2种)
│   ├── config_mgmt.py    # 配置管理工具 (1种)
│   └── system.py         # 系统管理工具 (1种)
├── services/              # 核心服务模块
│   ├── __init__.py       # 服务模块初始化
│   ├── data_service.py   # 数据处理服务，统一数据访问层
│   ├── cache_service.py  # 缓存管理服务，TTL缓存机制
│   └── parser_service.py # 数据解析服务，解析output文件
└── utils/                 # 工具模块
    ├── __init__.py       # 工具模块初始化
    ├── date_parser.py    # 日期解析工具，支持自然语言
    ├── validators.py     # 参数验证工具，统一参数校验
    └── errors.py         # 错误定义，自定义异常类
```

### 配置依赖
- **项目根目录**: 自动检测项目路径
- **config/config.yaml**: 读取平台配置和爬虫参数
- **config/frequency_words.txt**: 读取个人关注词配置
- **output/**: 读取新闻数据文件，支持历史数据查询

## 数据模型

### 新闻数据模型
```python
class NewsItem:
    title: str          # 新闻标题
    url: str           # 新闻链接
    platform: str      # 来源平台ID
    platform_name: str # 来源平台名称
    rank: int          # 热搜排名
    ranks: List[int]   # 历史排名列表
    count: int         # 出现次数
    timestamp: str     # 抓取时间
    is_new: bool       # 是否新增
```

### 分析结果模型
```python
class AnalysisResult:
    summary: str        # 分析摘要
    insights: List     # 数据洞察
    trends: List       # 趋势数据
    sentiment: Dict    # 情感分析
    recommendations: List  # 推荐建议
    metadata: Dict     # 元数据信息
```

### 工具响应模型
```python
class ToolResponse:
    success: bool       # 执行是否成功
    data: Any          # 返回数据
    message: str       # 状态消息
    error: Dict        # 错误信息（如果有）
    summary: Dict      # 执行摘要
    metadata: Dict     # 元数据信息
```

## 部署配置

### 一键部署脚本
```bash
# macOS/Linux
./setup-mac.sh

# Windows
setup-windows.bat
setup-windows-en.bat  # 英文版
```

### 手动部署步骤
1. 安装UV包管理器
2. 创建虚拟环境: `uv sync`
3. 配置AI客户端连接参数

### 连接参数配置
```json
{
  "name": "TrendRadar",
  "description": "新闻热点聚合分析工具",
  "command": "uv",
  "args": [
    "--directory", "/path/to/TrendRadar",
    "run", "python", "-m", "mcp_server.server"
  ]
}
```

## 性能优化

### 缓存策略
- **TTL缓存**: 15分钟自动过期
- **智能缓存**: 基于查询频率的动态缓存
- **缓存统计**: 实时监控缓存命中率

### 数据处理优化
- **分页加载**: 大数据集自动分页，避免内存溢出
- **异步处理**: 非阻塞的并发数据处理
- **内存管理**: 及时释放大型数据对象

### 网络优化
- **连接池**: 复用HTTP连接
- **请求重试**: 自动重试机制，提高可靠性
- **超时控制**: 合理的超时设置，避免长时间等待

## 错误处理

### 错误分类
- **MCPError**: MCP协议相关错误
- **InvalidParameterError**: 参数验证错误
- **DataNotFoundError**: 数据未找到错误
- **CrawlTaskError**: 爬虫任务错误

### 错误恢复机制
- **优雅降级**: 部分功能失败时继续提供服务
- **错误提示**: 详细的错误信息和解决建议
- **日志记录**: 完整的错误日志和调试信息

## 测试与质量

### 测试方法
- **MCP Inspector**: 官方调试工具
- **单元测试**: 各模块功能测试
- **集成测试**: 完整流程测试
- **客户端测试**: 多种AI客户端实际连接测试

### 质量保证
- **代码规范**: 遵循PEP8编码规范
- **类型提示**: 完整的类型注解
- **文档注释**: 详细的docstring说明
- **版本控制**: 语义化版本管理

## 常见问题 (FAQ)

### Q1: 如何连接MCP服务器？
**A**:
1. **STDIO模式**: 在AI客户端中配置uv命令路径和参数
2. **HTTP模式**: 启动HTTP服务后连接 http://localhost:3333/mcp

### Q2: 支持哪些AI客户端？
**A**: 支持所有标准MCP协议的客户端：
- **Cherry Studio** (推荐，GUI配置)
- **Claude Desktop** (配置文件方式)
- **Cursor/Cline/Continue** (项目级配置)
- **Claude Code CLI** (命令行添加)

### Q3: 查询数据没有结果怎么办？
**A**:
1. 确认output目录有新闻数据
2. 检查查询日期范围是否正确
3. 验证平台ID和关键词格式
4. 使用get_system_status检查系统状态

### Q4: 如何添加新的分析工具？
**A**:
1. 在相应tools模块中创建新工具函数
2. 使用@mcp.tool装饰器注册工具
3. 添加详细的docstring说明
4. 在server.py中导入并注册
5. 更新文档说明

### Q5: 性能问题如何优化？
**A**:
1. 合理设置limit参数，避免返回过多数据
2. 使用缓存功能，减少重复查询
3. 选择合适的排序方式
4. 定期清理过期缓存

### Q6: 如何配置个人关注词？
**A**:
编辑 `config/frequency_words.txt` 文件：
```
人工智能
机器学习
区块链
新能源
```

## 相关文件清单

| 文件路径 | 描述 | 重要性 |
|---------|------|-------|
| `mcp_server/server.py` | MCP服务器主入口，注册所有16种工具 | ⭐⭐⭐ |
| `mcp_server/tools/analytics.py` | 高级分析工具，包含8种分析方法 | ⭐⭐⭐ |
| `mcp_server/tools/data_query.py` | 基础查询工具，3种核心查询功能 | ⭐⭐⭐ |
| `mcp_server/tools/search_tools.py` | 智能检索工具，支持模糊搜索和关联分析 | ⭐⭐⭐ |
| `mcp_server/services/data_service.py` | 数据处理服务，统一数据访问层 | ⭐⭐ |
| `mcp_server/services/cache_service.py` | 缓存管理服务，TTL缓存机制 | ⭐⭐ |
| `mcp_server/utils/validators.py` | 参数验证工具，确保输入合法性 | ⭐⭐ |
| `pyproject.toml` | Python项目配置，定义依赖和脚本 | ⭐⭐ |
| `setup-mac.sh` | macOS一键部署脚本 | ⭐ |
| `README-MCP-FAQ.md` | MCP使用FAQ文档 | ⭐⭐ |

## 变更记录 (Changelog)

**2025-12-07**: v3.5.0同步更新
- 更新分析工具数量从13种到16种
- 确认所有工具描述和功能说明准确
- 保持文档与实际代码一致

**2025-11-24**: 深度更新MCP服务器模块文档，详细说明13种分析工具的功能、参数和用途，添加部署配置、性能优化、错误处理等完整信息
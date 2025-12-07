# BlogMonitor - 博主发言监控工具架构设计

## 1. 项目概述

### 1.1 项目目标
BlogMonitor 是一个多平台博主发言监控工具，旨在帮助用户实时跟踪指定博主在各大社交平台的发言，通过智能过滤和分析，确保不错过重要信息。

### 1.2 核心功能
- 多平台数据采集（微博、Twitter、知乎、B站等）
- 智能关键词过滤和内容分析
- 实时通知推送（多渠道）
- 数据持久化存储和快速检索
- AI 驱动的内容分析和趋势预测
- 类似 TrendRadar 的 MCP 集成能力

## 2. 系统架构

### 2.1 整体架构图

```mermaid
graph TB
    subgraph "外部数据源"
        W[微博]
        T[Twitter]
        Z[知乎]
        B[B站]
        O[其他平台]
    end

    subgraph "数据采集层"
        CA[采集适配器]
        PS[平台调度器]
        RM[速率管理器]
    end

    subgraph "数据处理层"
        DP[数据处理器]
        KF[关键词过滤器]
        SA[语义分析器]
        DD[去重引擎]
    end

    subgraph "存储层"
        PQ[PostgreSQL]
        RD[Redis缓存]
        ES[Elasticsearch]
        MQ[消息队列]
    end

    subgraph "AI分析层"
        MCP[MCP服务器]
        AT[分析工具集]
        ML[ML模型]
    end

    subgraph "通知层"
        NM[通知管理器]
        EM[邮件通知]
        WS[WebSocket]
        TG[Telegram Bot]
        WX[微信推送]
    end

    subgraph "API服务层"
        RG[REST API]
        GA[GraphQL API]
        WSA[WebSocket API]
    end

    subgraph "前端界面"
        WD[Web Dashboard]
        MB[移动端App]
        AD[管理员面板]
    end

    W --> CA
    T --> CA
    Z --> CA
    B --> CA
    O --> CA

    CA --> DP
    PS --> CA
    RM --> PS

    DP --> KF
    KF --> SA
    SA --> DD
    DD --> PQ
    DD --> ES

    PQ --> MCP
    ES --> AT
    RD --> ML

    MCP --> AT
    AT --> NM

    NM --> EM
    NM --> WS
    NM --> TG
    NM --> WX

    PQ --> RG
    PQ --> GA
    MQ --> WSA

    RG --> WD
    GA --> MB
    WSA --> AD
```

### 2.2 核心模块设计

#### 2.2.1 数据采集模块 (Collector)
```python
# collector/base.py
from abc import ABC, abstractmethod
from typing import List, Dict, Any
from dataclasses import dataclass

@dataclass
class BlogPost:
    """统一的博文数据结构"""
    platform: str
    author_id: str
    author_name: str
    content: str
    published_at: datetime
    post_id: str
    url: str
    media_urls: List[str]
    metrics: Dict[str, Any]  # 点赞、转发、评论等

class BaseCollector(ABC):
    """采集器基类"""

    @abstractmethod
    async def collect_posts(self, author_ids: List[str]) -> List[BlogPost]:
        pass

    @abstractmethod
    async def get_author_info(self, author_id: str) -> Dict[str, Any]:
        pass

    @abstractmethod
    def get_rate_limit(self) -> Dict[str, int]:
        pass
```

#### 2.2.2 关键词过滤模块 (Filter)
```python
# filter/keyword_filter.py
import re
from typing import List, Tuple
from jieba import cut
from sklearn.feature_extraction.text import TfidfVectorizer

class KeywordFilter:
    """智能关键词过滤器"""

    def __init__(self, config: Dict[str, Any]):
        self.exact_keywords = config.get('exact_keywords', [])
        self.fuzzy_keywords = config.get('fuzzy_keywords', [])
        self.exclude_keywords = config.get('exclude_keywords', [])
        self.semantic_patterns = config.get('semantic_patterns', [])

        # 初始化语义相似度模型
        self.vectorizer = TfidfVectorizer()
        self.semantic_vectors = None

    def should_include(self, post: BlogPost) -> Tuple[bool, List[str]]:
        """
        判断是否应该包含该帖子
        返回: (是否包含, 匹配的关键词列表)
        """
        content = post.content.lower()

        # 检查排除关键词
        if self._check_exclude(content):
            return False, []

        # 检查精确匹配
        exact_matches = self._check_exact_match(content)
        if exact_matches:
            return True, exact_matches

        # 检查模糊匹配
        fuzzy_matches = self._check_fuzzy_match(content)
        if fuzzy_matches:
            return True, fuzzy_matches

        # 检查语义匹配
        semantic_matches = self._check_semantic_match(content)
        if semantic_matches:
            return True, semantic_matches

        return False, []
```

#### 2.2.3 实时通知模块 (Notifier)
```python
# notifier/manager.py
from enum import Enum
from typing import Dict, Any, List

class NotificationChannel(Enum):
    EMAIL = "email"
    TELEGRAM = "telegram"
    WECHAT = "wechat"
    WEBHOOK = "webhook"
    WEBHOOK_PUSH = "webhook_push"

class NotificationManager:
    """通知管理器"""

    def __init__(self, config: Dict[str, Any]):
        self.channels = {}
        self.templates = config.get('templates', {})
        self.rules = config.get('rules', [])

    async def send_notification(
        self,
        post: BlogPost,
        matched_keywords: List[str]
    ) -> None:
        """发送通知"""
        # 评估通知规则
        should_notify, channels = self._evaluate_rules(post, matched_keywords)

        if not should_notify:
            return

        # 准备通知内容
        content = self._prepare_content(post, matched_keywords)

        # 多渠道发送
        tasks = []
        for channel in channels:
            if channel in self.channels:
                tasks.append(
                    self.channels[channel].send(content)
                )

        await asyncio.gather(*tasks)
```

#### 2.2.4 MCP 服务器模块 (MCP Server)
```python
# mcp_server/tools/blog_monitor_tools.py
from mcp.server import Server
from mcp.types import Tool

class BlogMonitorTools:
    """MCP 博主监控工具集"""

    def __init__(self, db, collector, analyzer):
        self.db = db
        self.collector = collector
        self.analyzer = analyzer

    def get_tools(self) -> List[Tool]:
        """返回所有可用的 MCP 工具"""
        return [
            Tool(
                name="get_latest_posts",
                description="获取指定博主的最新发言",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "author_id": {"type": "string"},
                        "platform": {"type": "string"},
                        "limit": {"type": "integer", "default": 10}
                    }
                }
            ),
            Tool(
                name="search_posts_by_keyword",
                description="根据关键词搜索历史发言",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "keywords": {"type": "array", "items": {"type": "string"}},
                        "date_range": {"type": "object"},
                        "platforms": {"type": "array", "items": {"type": "string"}}
                    }
                }
            ),
            Tool(
                name="analyze_author_activity",
                description="分析博主活跃度和发言趋势",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "author_id": {"type": "string"},
                        "days": {"type": "integer", "default": 30}
                    }
                }
            ),
            Tool(
                name="get_keyword_trends",
                description="获取关键词热度趋势",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "keywords": {"type": "array", "items": {"type": "string"}},
                        "days": {"type": "integer", "default": 7}
                    }
                }
            ),
            Tool(
                name="detect_anomaly",
                description="检测异常发言模式",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "author_id": {"type": "string"},
                        "hours": {"type": "integer", "default": 24}
                    }
                }
            )
        ]
```

## 3. 数据库设计

### 3.1 PostgreSQL 主数据库

```sql
-- 用户表
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    preferences JSONB DEFAULT '{}'
);

-- 监控博主表
CREATE TABLE monitored_authors (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id),
    platform VARCHAR(20) NOT NULL,
    author_id VARCHAR(100) NOT NULL,
    author_name VARCHAR(100),
    display_name VARCHAR(100),
    avatar_url VARCHAR(255),
    followers_count INTEGER,
    is_active BOOLEAN DEFAULT true,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(user_id, platform, author_id)
);

-- 博文表
CREATE TABLE posts (
    id SERIAL PRIMARY KEY,
    platform VARCHAR(20) NOT NULL,
    post_id VARCHAR(100) NOT NULL,
    author_id VARCHAR(100) NOT NULL,
    author_name VARCHAR(100),
    content TEXT NOT NULL,
    url VARCHAR(500),
    media_urls JSONB DEFAULT '[]',
    metrics JSONB DEFAULT '{}',
    published_at TIMESTAMP,
    collected_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    is_processed BOOLEAN DEFAULT false,
    UNIQUE(platform, post_id)
);

-- 关键词匹配表
CREATE TABLE keyword_matches (
    id SERIAL PRIMARY KEY,
    post_id INTEGER REFERENCES posts(id),
    user_id INTEGER REFERENCES users(id),
    keyword VARCHAR(100),
    match_type VARCHAR(20), -- exact, fuzzy, semantic
    confidence FLOAT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 通知记录表
CREATE TABLE notifications (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id),
    post_id INTEGER REFERENCES posts(id),
    channel VARCHAR(20),
    status VARCHAR(20), -- pending, sent, failed
    sent_at TIMESTAMP,
    error_message TEXT
);

-- 创建索引
CREATE INDEX idx_posts_author ON posts(author_id);
CREATE INDEX idx_posts_published ON posts(published_at);
CREATE INDEX idx_posts_platform ON posts(platform);
CREATE INDEX idx_keyword_matches_user_keyword ON keyword_matches(user_id, keyword);
CREATE INDEX idx_monitored_authors_user ON monitored_authors(user_id);
```

### 3.2 Elasticsearch 索引

```json
{
  "mappings": {
    "properties": {
      "platform": {"type": "keyword"},
      "author_id": {"type": "keyword"},
      "author_name": {
        "type": "text",
        "fields": {"keyword": {"type": "keyword"}}
      },
      "content": {
        "type": "text",
        "analyzer": "ik_max_word",
        "search_analyzer": "ik_smart"
      },
      "published_at": {"type": "date"},
      "metrics": {
        "properties": {
          "likes": {"type": "integer"},
          "shares": {"type": "integer"},
          "comments": {"type": "integer"}
        }
      },
      "keywords": {"type": "keyword"},
      "sentiment": {"type": "float"}
    }
  }
}
```

## 4. API 设计

### 4.1 REST API 端点

```python
# api/routes.py
from fastapi import APIRouter, Depends, HTTPException
from typing import List, Optional

router = APIRouter(prefix="/api/v1")

@router.get("/authors")
async def get_monitored_authors(
    platform: Optional[str] = None,
    user_id: int = Depends(get_current_user)
):
    """获取监控的博主列表"""
    pass

@router.post("/authors")
async def add_monitored_author(
    author: MonitoredAuthorCreate,
    user_id: int = Depends(get_current_user)
):
    """添加监控博主"""
    pass

@router.get("/posts")
async def get_posts(
    author_id: Optional[str] = None,
    platform: Optional[str] = None,
    keywords: Optional[str] = None,
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None,
    limit: int = 20
):
    """获取博文列表"""
    pass

@router.get("/posts/{post_id}")
async def get_post_detail(post_id: int):
    """获取博文详情"""
    pass

@router.get("/analytics/keywords")
async def get_keyword_trends(
    keywords: List[str],
    days: int = 7
):
    """获取关键词趋势分析"""
    pass

@router.get("/analytics/authors/{author_id}/activity")
async def get_author_activity(
    author_id: str,
    days: int = 30
):
    """获取博主活跃度分析"""
    pass
```

### 4.2 GraphQL Schema

```graphql
# schema.graphql
type User {
  id: ID!
  username: String!
  email: String!
  monitoredAuthors: [MonitoredAuthor!]!
  notifications: [Notification!]!
}

type MonitoredAuthor {
  id: ID!
  platform: String!
  authorId: String!
  authorName: String!
  displayName: String!
  avatarUrl: String
  followersCount: Int
  isActive: Boolean!
  latestPosts: [Post!]!
}

type Post {
  id: ID!
  platform: String!
  postId: String!
  author: MonitoredAuthor!
  content: String!
  url: String
  mediaUrls: [String!]!
  metrics: PostMetrics!
  publishedAt: DateTime!
  keywordMatches: [KeywordMatch!]!
}

type PostMetrics {
  likes: Int
  shares: Int
  comments: Int
  views: Int
}

type KeywordMatch {
  id: ID!
  keyword: String!
  matchType: MatchType!
  confidence: Float!
}

enum MatchType {
  EXACT
  FUZZY
  SEMANTIC
}

type Query {
  user(id: ID!): User
  monitoredAuthors(platform: String): [MonitoredAuthor!]!
  posts(
    authorId: String
    platform: String
    keywords: [String!]
    dateRange: DateRange
    limit: Int = 20
  ): [Post!]!
  keywordTrends(keywords: [String!]!, days: Int = 7): [KeywordTrend!]!
}

type Mutation {
  addMonitoredAuthor(input: AddMonitoredAuthorInput!): MonitoredAuthor!
  removeMonitoredAuthor(id: ID!): Boolean!
  updateNotificationSettings(input: NotificationSettingsInput!): User!
}
```

## 5. 部署架构

### 5.1 Docker 容器化

```dockerfile
# Dockerfile
FROM python:3.11-slim

WORKDIR /app

# 安装系统依赖
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    curl \
    && rm -rf /var/lib/apt/lists/*

# 安装 Python 依赖
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 复制应用代码
COPY . .

# 设置环境变量
ENV PYTHONPATH=/app
ENV PYTHONUNBUFFERED=1

# 暴露端口
EXPOSE 8000 3333

# 启动命令
CMD ["uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### 5.2 Docker Compose

```yaml
# docker-compose.yml
version: '3.8'

services:
  app:
    build: .
    ports:
      - "8000:8000"
      - "3333:3333"
    environment:
      - DATABASE_URL=postgresql://blogmonitor:password@postgres:5432/blogmonitor
      - REDIS_URL=redis://redis:6379
      - ELASTICSEARCH_URL=http://elasticsearch:9200
    depends_on:
      - postgres
      - redis
      - elasticsearch
    volumes:
      - ./logs:/app/logs
      - ./config:/app/config

  postgres:
    image: postgres:15
    environment:
      - POSTGRES_DB=blogmonitor
      - POSTGRES_USER=blogmonitor
      - POSTGRES_PASSWORD=password
    volumes:
      - postgres_data:/var/lib/postgresql/data
      - ./migrations:/docker-entrypoint-initdb.d
    ports:
      - "5432:5432"

  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"
    volumes:
      - redis_data:/data

  elasticsearch:
    image: elasticsearch:8.8.0
    environment:
      - discovery.type=single-node
      - xpack.security.enabled=false
    ports:
      - "9200:9200"
    volumes:
      - es_data:/usr/share/elasticsearch/data

  scheduler:
    build: .
    command: python scheduler.py
    environment:
      - DATABASE_URL=postgresql://blogmonitor:password@postgres:5432/blogmonitor
      - REDIS_URL=redis://redis:6379
    depends_on:
      - postgres
      - redis

  worker:
    build: .
    command: celery -A tasks worker --loglevel=info
    environment:
      - DATABASE_URL=postgresql://blogmonitor:password@postgres:5432/blogmonitor
      - REDIS_URL=redis://redis:6379
    depends_on:
      - postgres
      - redis

volumes:
  postgres_data:
  redis_data:
  es_data:
```

### 5.3 Kubernetes 部署

```yaml
# k8s/deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: blogmonitor-api
spec:
  replicas: 3
  selector:
    matchLabels:
      app: blogmonitor-api
  template:
    metadata:
      labels:
        app: blogmonitor-api
    spec:
      containers:
      - name: api
        image: blogmonitor:latest
        ports:
        - containerPort: 8000
        env:
        - name: DATABASE_URL
          valueFrom:
            secretKeyRef:
              name: blogmonitor-secrets
              key: database-url
        - name: REDIS_URL
          valueFrom:
            secretKeyRef:
              name: blogmonitor-secrets
              key: redis-url
        resources:
          requests:
            memory: "256Mi"
            cpu: "250m"
          limits:
            memory: "512Mi"
            cpu: "500m"
        livenessProbe:
          httpGet:
            path: /health
            port: 8000
          initialDelaySeconds: 30
          periodSeconds: 10
        readinessProbe:
          httpGet:
            path: /ready
            port: 8000
          initialDelaySeconds: 5
          periodSeconds: 5
---
apiVersion: v1
kind: Service
metadata:
  name: blogmonitor-api-service
spec:
  selector:
    app: blogmonitor-api
  ports:
  - protocol: TCP
    port: 80
    targetPort: 8000
  type: LoadBalancer
```

## 6. 性能优化策略

### 6.1 缓存策略
- **Redis 缓存**: 热点数据缓存，TTL 30分钟
- **应用层缓存**: 博主信息缓存，LRU 策略
- **CDN 缓存**: 静态资源和媒体文件

### 6.2 数据库优化
- **读写分离**: 主从数据库架构
- **分区表**: 按平台和时间分区
- **索引优化**: 复合索引和部分索引

### 6.3 采集优化
- **增量采集**: 基于最后采集时间
- **并发控制**: 协程池限制并发数
- **速率限制**: 遵守平台 API 限制

## 7. 监控和日志

### 7.1 监控指标
```python
# metrics/collector.py
from prometheus_client import Counter, Histogram, Gauge

# 采集指标
posts_collected = Counter('blogmonitor_posts_collected_total',
                         'Total posts collected', ['platform'])
collection_duration = Histogram('blogmonitor_collection_duration_seconds',
                              'Time spent collecting posts')

# 过滤指标
posts_filtered = Counter('blogmonitor_posts_filtered_total',
                        'Total posts filtered', ['match_type'])
filter_duration = Histogram('blogmonitor_filter_duration_seconds',
                           'Time spent filtering posts')

# 通知指标
notifications_sent = Counter('blogmonitor_notifications_sent_total',
                           'Total notifications sent', ['channel'])
notification_duration = Histogram('blogmonitor_notification_duration_seconds',
                                'Time spent sending notifications')
```

### 7.2 日志配置
```yaml
# logging.yaml
version: 1
disable_existing_loggers: false

formatters:
  standard:
    format: "%(asctime)s [%(levelname)s] %(name)s: %(message)s"
  json:
    format: '{"timestamp": "%(asctime)s", "level": "%(levelname)s", "logger": "%(name)s", "message": "%(message)s"}'

handlers:
  console:
    class: logging.StreamHandler
    formatter: standard
    level: INFO

  file:
    class: logging.handlers.RotatingFileHandler
    filename: logs/blogmonitor.log
    maxBytes: 10485760  # 10MB
    backupCount: 5
    formatter: json
    level: DEBUG

  sentry:
    class: sentry_sdk.integrations.logging.SentryHandler
    level: ERROR

loggers:
  blogmonitor:
    level: DEBUG
    handlers: [console, file]
    propagate: false

  uvicorn:
    level: INFO
    handlers: [console]
    propagate: false

root:
  level: INFO
  handlers: [console, file]
```

## 8. 安全考虑

### 8.1 API 安全
- JWT 认证
- API 速率限制
- CORS 配置
- SQL 注入防护

### 8.2 数据安全
- 敏感数据加密
- 访问权限控制
- 审计日志
- GDPR 合规

## 9. 实施计划

### Phase 1: 基础框架 (2周)
- [ ] 项目初始化和环境搭建
- [ ] 数据库设计和迁移
- [ ] 基础 API 框架
- [ ] 单个平台采集器实现

### Phase 2: 核心功能 (3周)
- [ ] 多平台采集器
- [ ] 关键词过滤系统
- [ ] 基础通知功能
- [ ] Web 界面原型

### Phase 3: 高级功能 (2周)
- [ ] MCP 服务器集成
- [ ] AI 分析功能
- [ ] 实时推送优化
- [ ] 性能优化

### Phase 4: 部署上线 (1周)
- [ ] 容器化部署
- [ ] 监控和日志
- [ ] 文档完善
- [ ] 测试和调优

## 10. 总结

BlogMonitor 博主监控工具采用现代化的微服务架构，具有以下特点：

1. **高度可扩展**: 模块化设计，易于添加新平台和功能
2. **实时响应**: 基于消息队列和 WebSocket 的实时处理
3. **智能分析**: 集成 AI 能力，提供深度内容分析
4. **高可用性**: 容器化部署，支持水平扩展
5. **易于集成**: 提供 MCP 接口，可与 AI 工具无缝集成

该架构方案充分考虑了性能、可靠性、可维护性和扩展性，能够满足大规模博主监控的需求。

---

*文档版本: v1.0 | 最后更新: 2025-12-07*
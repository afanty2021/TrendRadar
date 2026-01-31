# trendradar/storage - 存储管理模块

[根目录](../../CLAUDE.md) > [trendradar](../CLAUDE.md) > **storage/**

> **最后更新**：2026-01-31 15:19:33
> **模块类型**：数据存储

## 模块职责

存储管理模块负责数据的持久化，支持本地 SQLite 存储和远程 S3 兼容存储（R2/OSS/COS）。提供统一的存储接口，自动选择存储后端，并处理数据同步和清理。

## 入口与启动

### 主要入口
- **`manager.py`**：存储管理器，统一入口
- **`local.py`**：本地存储实现
- **`remote.py`**：远程存储实现
- **`base.py`**：存储基类接口
- **`sqlite_mixin.py`**：SQLite 混入类
- **`schema.sql`**：数据库表结构
- **`rss_schema.sql`**：RSS 数据库表结构

### 使用方式
```python
from trendradar.storage.manager import StorageManager

# 创建存储管理器
manager = StorageManager(config)

# 保存数据
await manager.save_news_data(news_data)

# 加载数据
data = await manager.load_news_data(date_str)
```

## 对外接口

### StorageManager 类

**manager.py**
```python
class StorageManager:
    """存储管理器"""

    def __init__(self, config: Dict[str, Any]):
        """初始化管理器"""

    def get_backend(self) -> StorageBackend:
        """获取存储后端（单例）"""

    async def save_news_data(
        self,
        news_data: NewsData
    ) -> bool:
        """保存新闻数据"""

    async def load_news_data(
        self,
        date_str: str
    ) -> Optional[NewsData]:
        """加载新闻数据"""

    async def save_rss_data(
        self,
        rss_data: RSSData
    ) -> bool:
        """保存 RSS 数据"""

    async def load_rss_data(
        self,
        date_str: str
    ) -> Optional[RSSData]:
        """加载 RSS 数据"""

    async def list_available_dates(
        self
    ) -> List[str]:
        """列出可用日期"""

    async def cleanup_old_data(
        self,
        retain_days: int
    ) -> int:
        """清理过期数据"""
```

### StorageBackend 基类

**base.py**
```python
class StorageBackend(ABC):
    """存储后端基类"""

    @abstractmethod
    async def save_news_data(
        self,
        news_data: NewsData
    ) -> bool:
        """保存新闻数据"""

    @abstractmethod
    async def load_news_data(
        self,
        date_str: str
    ) -> Optional[NewsData]:
        """加载新闻数据"""

    @abstractmethod
    async def list_available_dates(
        self
    ) -> List[str]:
        """列出可用日期"""
```

### LocalStorage 类

**local.py**
```python
class LocalStorage(StorageBackend):
    """本地存储实现"""

    def __init__(self, config: Dict[str, Any]):
        """初始化本地存储"""

    async def save_news_data(
        self,
        news_data: NewsData
    ) -> bool:
        """保存到本地"""

    async def load_news_data(
        self,
        date_str: str
    ) -> Optional[NewsData]:
        """从本地加载"""

    def get_output_path(
        self,
        file_type: str
    ) -> Path:
        """获取输出路径"""
```

### RemoteStorage 类

**remote.py**
```python
class RemoteStorage(StorageBackend):
    """远程存储实现（S3 兼容）"""

    def __init__(self, config: Dict[str, Any]):
        """初始化远程存储"""

    async def save_news_data(
        self,
        news_data: NewsData
    ) -> bool:
        """保存到远程"""

    async def load_news_data(
        self,
        date_str: str
    ) -> Optional[NewsData]:
        """从远程加载"""

    async def sync_to_local(
        self,
        date_str: str
    ) -> bool:
        """同步到本地"""
```

## 关键依赖与配置

### 内部依赖
```
trendradar/
└── storage/
    ├── manager.py        # 存储管理器
    ├── local.py          # 本地存储
    ├── remote.py         # 远程存储
    ├── base.py           # 基类接口
    ├── sqlite_mixin.py   # SQLite 混入
    ├── schema.sql        # 表结构
    └── rss_schema.sql    # RSS 表结构
```

### 外部依赖
- **sqlite3**：本地数据库
- **boto3**：S3 兼容存储

### 配置示例
```yaml
storage:
  backend: "auto"                 # auto | local | remote

  local:
    output_dir: "output"
    db_dir: "output/db"

  remote:
    provider: "cloudflare"        # cloudflare | aliyun | tencent | aws
    bucket: "your-bucket"
    access_key_id: ""
    secret_access_key: ""
    endpoint_url: ""
    region: "auto"

  data_retention:
    enabled: true
    retain_days: 30
```

## 数据模型

### 存储文件结构
```
output/
├── db/                    # SQLite 数据库
│   ├── news.db
│   └── rss.db
├── txt/                   # TXT 快照
│   └── 2026-01-31.txt
└── html/                  # HTML 报告
    └── 2026-01-31.html
```

### 数据库表结构

**news 表**
```sql
CREATE TABLE news (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    date TEXT NOT NULL,
    time TEXT NOT NULL,
    platform TEXT NOT NULL,
    title TEXT NOT NULL,
    url TEXT,
    rank INTEGER,
    hot_value INTEGER,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

## 测试与质量

**当前状态**：未配置测试

**建议测试覆盖**：
- `StorageManager`：管理器测试
- 本地存储读写测试
- 远程存储同步测试
- 数据清理测试

## 常见问题 (FAQ)

### Q1: 如何切换存储后端？

**A**: 修改配置：
```yaml
storage:
  backend: "local"  # local | remote | auto
```

### Q2: 如何配置 S3 兼容存储？

**A**: 配置远程存储：
```yaml
storage:
  remote:
    provider: "cloudflare"
    bucket: "trendradar"
    endpoint_url: "https://..."
    access_key_id: "..."
    secret_access_key: "..."
```

### Q3: 如何清理过期数据？

**A**: 启用数据保留策略：
```yaml
storage:
  data_retention:
    enabled: true
    retain_days: 30
```

### Q4: GitHub Actions 环境使用哪种后端？

**A**: `auto` 模式会自动选择远程存储

## 相关文件清单

- `manager.py`：存储管理器，约 332 行
- `local.py`：本地存储，约 377 行
- `remote.py`：远程存储，约 680 行
- `base.py`：基类接口，约 457 行
- `sqlite_mixin.py`：SQLite 混入，约 1167 行
- `schema.sql`：表结构，约 109 行
- `rss_schema.sql`：RSS 表结构，约 83 行

## 变更记录 (Changelog)

### 2026-01-31 15:19:33
- ✨ 创建模块文档
- 📊 完成接口与配置分析

---

*本文档由 AI 自动生成并维护*

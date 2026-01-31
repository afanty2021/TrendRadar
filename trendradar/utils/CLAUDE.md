# trendradar/utils - 工具函数模块

[根目录](../../CLAUDE.md) > [trendradar](../CLAUDE.md) > **utils/**

> **最后更新**：2026-01-31 15:19:33
> **模块类型**：工具函数

## 模块职责

工具函数模块提供通用的辅助函数，包括时间处理、URL 处理等功能。

## 入口与启动

### 主要文件
- **`time.py`**：时间处理工具
- **`url.py`**：URL 处理工具

### 使用方式
```python
from trendradar.utils.time import get_current_time, parse_time
from trendradar.utils.url import normalize_url, extract_domain

# 时间处理
now = get_current_time("Asia/Shanghai")
parsed = parse_time("2026-01-31 12:00:00")

# URL 处理
clean_url = normalize_url(raw_url)
domain = extract_domain(url)
```

## 对外接口

### 时间函数

**time.py**
```python
def get_current_time(
    timezone: str = "Asia/Shanghai"
) -> datetime:
    """获取当前时间"""

def parse_time(
    time_str: str,
    format: str = "%Y-%m-%d %H:%M:%S"
) -> datetime:
    """解析时间字符串"""

def format_time(
    dt: datetime,
    format: str = "%Y-%m-%d %H:%M:%S"
) -> str:
    """格式化时间"""

def get_date_str(
    dt: Optional[datetime] = None
) -> str:
    """获取日期字符串"""

def get_time_str(
    dt: Optional[datetime] = None
) -> str:
    """获取时间字符串"""
```

### URL 函数

**url.py**
```python
def normalize_url(
    url: str
) -> str:
    """规范化 URL"""

def extract_domain(
    url: str
) -> str:
    """提取域名"""

def is_valid_url(
    url: str
) -> bool:
    """验证 URL 有效性"""

def add_query_param(
    url: str,
    key: str,
    value: str
) -> str:
    """添加查询参数"""
```

## 关键依赖与配置

### 内部依赖
```
trendradar/
└── utils/
    ├── time.py          # 时间处理
    └── url.py           # URL 处理
```

### 外部依赖
- **datetime**：时间处理
- **urllib.parse**：URL 解析
- **pytz**：时区处理

## 测试与质量

**当前状态**：未配置测试

**建议测试覆盖**：
- 时间格式转换测试
- 时区处理测试
- URL 规范化测试
- 域名提取测试

## 常见问题 (FAQ)

### Q1: 如何处理不同时区？

**A**: 使用 `get_current_time()` 并传入时区：
```python
time = get_current_time("America/New_York")
```

### Q2: URL 包含中文字符怎么办？

**A**: 使用 `normalize_url()` 自动处理编码

## 相关文件清单

- `time.py`：时间处理，约 177 行
- `url.py`：URL 处理，约 113 行

## 变更记录 (Changelog)

### 2026-01-31 15:19:33
- ✨ 创建模块文档
- 📊 完成接口分析

---

*本文档由 AI 自动生成并维护*

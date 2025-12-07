#!/usr/bin/env python3
"""
博主发言监控工具
监控特定博主（微博、知乎等）的最新发言，根据关键词过滤并推送通知
"""

import json
import time
import hashlib
import requests
from datetime import datetime, timedelta
from typing import List, Dict, Optional, Set
from pathlib import Path
import logging
import yaml
import re
from urllib.parse import quote

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('blogger_monitor.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


class BloggerMonitor:
    """博主监控主类"""

    def __init__(self, config_path: str = "config/blogger_config.yaml"):
        """
        初始化监控器

        Args:
            config_path: 配置文件路径
        """
        self.config = self.load_config(config_path)
        self.cache_file = Path("output/blogger_cache.json")
        self.ensure_output_dir()

        # 加载缓存
        self.cache = self.load_cache()

        # 初始化会话
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })

    def load_config(self, config_path: str) -> Dict:
        """加载配置文件"""
        try:
            with open(config_path, 'r', encoding='utf-8') as f:
                config = yaml.safe_load(f)
            return config
        except FileNotFoundError:
            logger.warning(f"配置文件 {config_path} 不存在，使用默认配置")
            return self.get_default_config()

    def get_default_config(self) -> Dict:
        """获取默认配置"""
        return {
            'monitors': [],
            'keywords': [],
            'notification': {
                'enable': True,
                'channels': ['console']
            },
            'check_interval': 300,  # 5分钟
            'max_posts_per_check': 10
        }

    def ensure_output_dir(self):
        """确保输出目录存在"""
        Path("output").mkdir(exist_ok=True)

    def load_cache(self) -> Dict:
        """加载缓存数据"""
        if self.cache_file.exists():
            try:
                with open(self.cache_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except Exception as e:
                logger.error(f"加载缓存失败: {e}")
        return {}

    def save_cache(self):
        """保存缓存数据"""
        try:
            with open(self.cache_file, 'w', encoding='utf-8') as f:
                json.dump(self.cache, f, ensure_ascii=False, indent=2)
        except Exception as e:
            logger.error(f"保存缓存失败: {e}")

    def get_post_hash(self, post: Dict) -> str:
        """生成内容的唯一哈希值"""
        content = f"{post.get('platform', '')}{post.get('user_id', '')}{post.get('content', '')}{post.get('publish_time', '')}"
        return hashlib.md5(content.encode('utf-8')).hexdigest()

    def match_keywords(self, content: str, keywords: List[str]) -> bool:
        """匹配关键词"""
        if not keywords:
            return True

        content_lower = content.lower()
        for keyword in keywords:
            if keyword.lower() in content_lower:
                return True
        return False

    def monitor_weibo_user(self, user_id: str, keywords: List[str]) -> List[Dict]:
        """
        监控微博用户（使用RSSHub）

        Args:
            user_id: 微博用户ID
            keywords: 关键词列表

        Returns:
            新的匹配帖子列表
        """
        try:
            # 使用RSSHub获取微博用户动态
            url = f"https://rsshub.app/weibo/user/{user_id}"

            response = self.session.get(url, timeout=10)
            response.raise_for_status()

            # 解析RSS（这里简化处理，实际应该使用feedparser）
            posts = self.parse_rss_content(response.text, 'weibo', user_id)

            # 过滤关键词
            if keywords:
                posts = [p for p in posts if self.match_keywords(p.get('content', ''), keywords)]

            # 检查是否有新内容
            new_posts = []
            for post in posts:
                post_hash = self.get_post_hash(post)
                if post_hash not in self.cache.get('posts', []):
                    new_posts.append(post)
                    self.cache.setdefault('posts', {})[post_hash] = datetime.now().isoformat()

            return new_posts

        except Exception as e:
            logger.error(f"监控微博用户 {user_id} 失败: {e}")
            return []

    def monitor_zhihu_user(self, user_id: str, keywords: List[str]) -> List[Dict]:
        """
        监控知乎用户（使用RSSHub）

        Args:
            user_id: 知乎用户ID或用户名
            keywords: 关键词列表

        Returns:
            新的匹配帖子列表
        """
        try:
            # 使用RSSHub获取知乎用户动态
            url = f"https://rsshub.app/zhihu/people/{user_id}/activities"

            response = self.session.get(url, timeout=10)
            response.raise_for_status()

            # 解析RSS
            posts = self.parse_rss_content(response.text, 'zhihu', user_id)

            # 过滤关键词
            if keywords:
                posts = [p for p in posts if self.match_keywords(p.get('content', ''), keywords)]

            # 检查是否有新内容
            new_posts = []
            for post in posts:
                post_hash = self.get_post_hash(post)
                if post_hash not in self.cache.get('posts', []):
                    new_posts.append(post)
                    self.cache.setdefault('posts', {})[post_hash] = datetime.now().isoformat()

            return new_posts

        except Exception as e:
            logger.error(f"监控知乎用户 {user_id} 失败: {e}")
            return []

    def parse_rss_content(self, rss_content: str, platform: str, user_id: str) -> List[Dict]:
        """
        解析RSS内容（简化版）

        Args:
            rss_content: RSS XML内容
            platform: 平台名称
            user_id: 用户ID

        Returns:
            解析后的帖子列表
        """
        # 这里使用正则表达式简单解析
        # 实际项目中应该使用 xml.etree.ElementTree 或 feedparser

        posts = []

        # 提取item标签
        items = re.findall(r'<item>.*?</item>', rss_content, re.DOTALL)

        for item in items[:self.config.get('max_posts_per_check', 10)]:
            # 提取标题
            title_match = re.search(r'<title><!\[CDATA\[(.*?)\]\]></title>', item)
            title = title_match.group(1) if title_match else ""

            # 提取链接
            link_match = re.search(r'<link>(.*?)</link>', item)
            link = link_match.group(1) if link_match else ""

            # 提取描述
            desc_match = re.search(r'<description><!\[CDATA\[(.*?)\]\]></description>', item, re.DOTALL)
            description = desc_match.group(1) if desc_match else ""

            # 提取发布时间
            pub_date_match = re.search(r'<pubDate>(.*?)</pubDate>', item)
            pub_date = pub_date_match.group(1) if pub_date_match else ""

            # 清理HTML标签
            content = re.sub(r'<[^>]+>', '', f"{title} {description}").strip()

            posts.append({
                'platform': platform,
                'user_id': user_id,
                'title': title,
                'content': content,
                'url': link,
                'publish_time': pub_date,
                'crawl_time': datetime.now().isoformat()
            })

        return posts

    def send_notification(self, post: Dict):
        """
        发送通知

        Args:
            post: 帖子信息
        """
        message = f"""
🔔 发现新的相关内容

平台: {post['platform'].upper()}
用户: {post['user_id']}
时间: {post.get('publish_time', '未知')}

内容: {post['content'][:100]}...
链接: {post.get('url', '无')}
"""

        # 保存到output目录（复用TrendRadar的输出格式）
        output_file = Path("output/blogger_notifications.json")

        notifications = []
        if output_file.exists():
            try:
                with open(output_file, 'r', encoding='utf-8') as f:
                    notifications = json.load(f)
            except:
                notifications = []

        notifications.append({
            'type': 'blogger_post',
            'timestamp': datetime.now().isoformat(),
            'data': post,
            'message': message.strip()
        })

        # 只保留最近100条通知
        notifications = notifications[-100:]

        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(notifications, f, ensure_ascii=False, indent=2)

        # 控制台输出
        logger.info(f"\n{message}")

        # 如果配置了其他通知渠道，可以在这里扩展
        # 例如：发送到微信、Telegram等

    def run_once(self):
        """执行一次监控检查"""
        logger.info("开始执行博主监控检查...")

        total_new_posts = 0

        for monitor in self.config.get('monitors', []):
            platform = monitor.get('platform')
            user_id = monitor.get('user_id')
            keywords = monitor.get('keywords', [])
            keywords.extend(self.config.get('keywords', []))  # 添加全局关键词

            if not platform or not user_id:
                logger.warning(f"监控配置缺少必要信息: {monitor}")
                continue

            logger.info(f"检查 {platform} 用户 {user_id}")

            new_posts = []

            if platform == 'weibo':
                new_posts = self.monitor_weibo_user(user_id, keywords)
            elif platform == 'zhihu':
                new_posts = self.monitor_zhihu_user(user_id, keywords)
            else:
                logger.warning(f"不支持的平台: {platform}")
                continue

            # 发送通知
            for post in new_posts:
                self.send_notification(post)
                total_new_posts += 1

        # 保存缓存
        self.save_cache()

        logger.info(f"检查完成，发现 {total_new_posts} 条新内容")

        return total_new_posts

    def run_daemon(self):
        """以守护进程模式运行"""
        logger.info("启动博主监控守护进程...")

        check_interval = self.config.get('check_interval', 300)  # 默认5分钟

        while True:
            try:
                self.run_once()
                logger.info(f"等待 {check_interval} 秒后进行下次检查...")
                time.sleep(check_interval)
            except KeyboardInterrupt:
                logger.info("监控程序被用户中断")
                break
            except Exception as e:
                logger.error(f"监控过程中发生错误: {e}")
                time.sleep(60)  # 出错后等待1分钟再重试


def main():
    """主函数"""
    import argparse

    parser = argparse.ArgumentParser(description='博主发言监控工具')
    parser.add_argument('--config', '-c', default='config/blogger_config.yaml', help='配置文件路径')
    parser.add_argument('--once', action='store_true', help='只执行一次检查')
    parser.add_argument('--init-config', action='store_true', help='初始化默认配置文件')

    args = parser.parse_args()

    # 初始化配置文件
    if args.init_config:
        config_path = args.config
        Path(config_path).parent.mkdir(exist_ok=True)

        default_config = {
            'monitors': [
                {
                    'platform': 'weibo',
                    'user_id': 'your_weibo_id',  # 替换为实际的微博ID
                    'keywords': ['AI', '人工智能']
                },
                {
                    'platform': 'zhihu',
                    'user_id': 'your_zhihu_id',  # 替换为实际的知乎ID
                    'keywords': ['技术', '创业']
                }
            ],
            'keywords': ['热点', '新闻'],  # 全局关键词
            'notification': {
                'enable': True,
                'channels': ['console']  # 可扩展: ['console', 'email', 'wechat', 'telegram']
            },
            'check_interval': 300,  # 5分钟检查一次
            'max_posts_per_check': 10
        }

        with open(config_path, 'w', encoding='utf-8') as f:
            yaml.dump(default_config, f, default_flow_style=False, allow_unicode=True)

        print(f"配置文件已创建: {config_path}")
        print("请编辑配置文件，添加要监控的用户ID和关键词")
        return

    # 创建监控器
    monitor = BloggerMonitor(args.config)

    # 运行监控
    if args.once:
        monitor.run_once()
    else:
        monitor.run_daemon()


if __name__ == "__main__":
    main()
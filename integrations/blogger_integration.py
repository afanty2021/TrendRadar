"""
博主监控与 TrendRadar 推送系统集成
将监控到的博主发言通过 TrendRadar 的推送渠道发送通知
"""

import json
import yaml
from pathlib import Path
from datetime import datetime
from typing import Dict, List
import logging

logger = logging.getLogger(__name__)


class BloggerToTrendRadarIntegration:
    """博主监控与 TrendRadar 的集成模块"""

    def __init__(self, trendradar_config: str = "config/config.yaml"):
        """
        初始化集成模块

        Args:
            trendradar_config: TrendRadar 配置文件路径
        """
        self.config = self.load_trendradar_config(trendradar_config)
        self.notification_cache = Path("output/blogger_notifications.json")

    def load_trendradar_config(self, config_path: str) -> Dict:
        """加载 TrendRadar 配置"""
        try:
            with open(config_path, 'r', encoding='utf-8') as f:
                return yaml.safe_load(f)
        except Exception as e:
            logger.error(f"加载 TrendRadar 配置失败: {e}")
            return {}

    def format_blogger_post_for_trendradar(self, post: Dict) -> Dict:
        """
        将博主帖子格式化为 TrendRadar 新闻格式

        Args:
            post: 博主帖子信息

        Returns:
            格式化后的新闻数据
        """
        # 生成唯一ID
        unique_id = f"blogger_{post['platform']}_{post['user_id']}_{hash(post['content'])}"

        return {
            'id': unique_id,
            'title': f"[{post['platform'].upper()}] {post.get('title', '博主新动态')[:50]}",
            'url': post.get('url', ''),
            'platform': f"blogger_{post['platform']}",  # 使用前缀区分
            'platform_name': f"博主({post['platform'].upper()})",
            'rank': 1,  # 博主内容默认 rank=1
            'ranks': [1],
            'count': 1,
            'timestamp': post.get('publish_time', datetime.now().strftime('%Y-%m-%d %H:%M:%S')),
            'is_new': True,
            'author_id': post.get('user_id', ''),
            'author_name': post.get('user_id', ''),  # 可以扩展为获取用户名
            'content': post.get('content', ''),
            'source_type': 'blogger_monitor'  # 标记来源
        }

    def save_to_trendradar_format(self, posts: List[Dict]):
        """
        将博主帖子保存为 TrendRadar 格式

        Args:
            posts: 博主帖子列表
        """
        if not posts:
            return

        # 转换格式
        formatted_posts = [self.format_blogger_post_for_trendradar(post) for post in posts]

        # 生成文件名（使用当前日期）
        date_str = datetime.now().strftime('%Y%m%d')
        output_file = Path(f"output/{date_str}_blogger.json")

        # 读取现有数据（如果有）
        existing_data = []
        if output_file.exists():
            try:
                with open(output_file, 'r', encoding='utf-8') as f:
                    existing_data = json.load(f)
            except:
                existing_data = []

        # 合并新数据
        existing_data.extend(formatted_posts)

        # 保存
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(existing_data, f, ensure_ascii=False, indent=2)

        logger.info(f"已保存 {len(formatted_posts)} 条博主动态到 {output_file}")

    def send_notifications_via_trendradar(self, posts: List[Dict]):
        """
        通过 TrendRadar 的推送系统发送通知

        Args:
            posts: 博主帖子列表
        """
        # 获取推送配置
        webhooks = self.config.get('webhooks', {})

        if not webhooks:
            logger.warning("TrendRadar 配置中未找到推送配置")
            return

        # 构建通知内容
        notification_data = {
            'title': '博主监控提醒',
            'content': self.build_notification_content(posts),
            'posts': posts
        }

        # 发送到各个渠道
        self.send_to_feishu(webhooks.get('feishu_url'), notification_data)
        self.send_to_dingtalk(webhooks.get('dingtalk_webhook_url'), notification_data)
        self.send_to_telegram(webhooks.get('telegram_bot_token'), webhooks.get('telegram_chat_id'), notification_data)

    def build_notification_content(self, posts: List[Dict]) -> str:
        """构建通知内容"""
        content_lines = ["🔔 博主监控发现新动态\n"]

        for post in posts[:5]:  # 最多显示5条
            platform = post.get('platform', '').upper()
            title = post.get('title', '无标题')[:50]
            content = post.get('content', '')[:100]

            content_lines.append(f"\n【{platform}】")
            content_lines.append(f"标题：{title}")
            content_lines.append(f"内容：{content}...")

            if post.get('url'):
                content_lines.append(f"链接：{post['url']}")

        if len(posts) > 5:
            content_lines.append(f"\n... 还有 {len(posts) - 5} 条动态")

        return "\n".join(content_lines)

    def send_to_feishu(self, webhook_url: str, data: Dict):
        """发送到飞书"""
        if not webhook_url:
            return

        try:
            import requests

            payload = {
                "msg_type": "interactive",
                "card": {
                    "config": {
                        "wide_screen_mode": True
                    },
                    "header": {
                        "title": {
                            "tag": "plain_text",
                            "content": "🔔 博主监控提醒"
                        },
                        "template": "blue"
                    },
                    "elements": [
                        {
                            "tag": "div",
                            "text": {
                                "tag": "plain_text",
                                "content": data['content']
                            }
                        }
                    ]
                }
            }

            response = requests.post(webhook_url, json=payload, timeout=10)
            if response.status_code == 200:
                logger.info("飞书通知发送成功")
            else:
                logger.error(f"飞书通知发送失败: {response.text}")

        except Exception as e:
            logger.error(f"发送飞书通知异常: {e}")

    def send_to_dingtalk(self, webhook_url: str, data: Dict):
        """发送到钉钉"""
        if not webhook_url:
            return

        try:
            import requests

            payload = {
                "msgtype": "markdown",
                "markdown": {
                    "title": "博主监控提醒",
                    "text": data['content']
                }
            }

            response = requests.post(webhook_url, json=payload, timeout=10)
            if response.status_code == 200:
                logger.info("钉钉通知发送成功")
            else:
                logger.error(f"钉钉通知发送失败: {response.text}")

        except Exception as e:
            logger.error(f"发送钉钉通知异常: {e}")

    def send_to_telegram(self, bot_token: str, chat_id: str, data: Dict):
        """发送到 Telegram"""
        if not bot_token or not chat_id:
            return

        try:
            import requests

            url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
            payload = {
                "chat_id": chat_id,
                "text": data['content'],
                "parse_mode": "Markdown"
            }

            response = requests.post(url, json=payload, timeout=10)
            if response.status_code == 200:
                logger.info("Telegram 通知发送成功")
            else:
                logger.error(f"Telegram 通知发送失败: {response.text}")

        except Exception as e:
            logger.error(f"发送 Telegram 通知异常: {e}")

    def process_new_notifications(self):
        """处理新的通知并集成到 TrendRadar"""
        if not self.notification_cache.exists():
            return

        try:
            with open(self.notification_cache, 'r', encoding='utf-8') as f:
                notifications = json.load(f)

            # 筛选出未处理的通知
            new_posts = []
            processed_count = 0

            for notification in notifications:
                if notification.get('processed'):
                    processed_count += 1
                    continue

                if notification.get('type') == 'blogger_post':
                    new_posts.append(notification['data'])
                    notification['processed'] = True
                    notification['processed_time'] = datetime.now().isoformat()

            if new_posts:
                logger.info(f"发现 {len(new_posts)} 条未处理的博主动态")

                # 保存为 TrendRadar 格式
                self.save_to_trendradar_format(new_posts)

                # 发送推送通知
                if self.config.get('webhooks'):
                    self.send_notifications_via_trendradar(new_posts)

                # 更新通知缓存
                with open(self.notification_cache, 'w', encoding='utf-8') as f:
                    json.dump(notifications, f, ensure_ascii=False, indent=2)

            else:
                logger.info(f"没有新的博主动态（已处理 {processed_count} 条）")

        except Exception as e:
            logger.error(f"处理通知失败: {e}")


# 使用示例
def main():
    """主函数"""
    integration = BloggerToTrendRadarIntegration()
    integration.process_new_notifications()


if __name__ == "__main__":
    main()
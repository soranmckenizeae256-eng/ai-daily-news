import os
import sys
import json
import logging
from pathlib import Path

current_dir = Path(__file__).parent
sys.path.insert(0, str(current_dir))

import httpx
from config import FEISHU_WEBHOOK_URL

logger = logging.getLogger(__name__)

class FeishuSender:
    def __init__(self, webhook_url=None):
        self.webhook_url = webhook_url or FEISHU_WEBHOOK_URL
        
    def send_rich_text_message(self, content, title="AI新闻日报"):
        """发送富文本消息到飞书"""
        if not self.webhook_url:
            logger.error("未配置飞书Webhook URL")
            return False
            
        url = self.webhook_url.rstrip('/')
        
        payload = {
            "msg_type": "rich_text",
            "rich_text": {
                "elements": [
                    {
                        "tag": "div",
                        "elements": [
                            {
                                "tag": "lark_md",
                                "text": content
                            }
                        ]
                    }
                ]
            }
        }
        
        try:
            logger.info("正在发送消息到飞书...")
            response = httpx.post(
                url,
                json=payload,
                timeout=30.0,
                headers={'Content-Type': 'application/json'}
            )
            response.raise_for_status()
            
            result = response.json()
            if result.get('code') == 0:
                logger.info("✓ 飞书消息发送成功")
                return True
            else:
                logger.error(f"✗ 飞书消息发送失败: {result.get('msg')}")
                return False
                
        except httpx.HTTPStatusError as e:
            logger.error(f"✗ HTTP错误: {e}")
            return False
        except Exception as e:
            logger.error(f"✗ 发送失败: {e}")
            return False
            
    def send_text_message(self, content):
        """发送纯文本消息（备用方案）"""
        if not self.webhook_url:
            logger.error("未配置飞书Webhook URL")
            return False
            
        url = self.webhook_url.rstrip('/')
        
        payload = {
            "msg_type": "text",
            "content": {
                "text": content
            }
        }
        
        try:
            response = httpx.post(
                url,
                json=payload,
                timeout=30.0,
                headers={'Content-Type': 'application/json'}
            )
            response.raise_for_status()
            
            result = response.json()
            if result.get('code') == 0:
                logger.info("✓ 文本消息发送成功")
                return True
            else:
                logger.error(f"✗ 发送失败: {result.get('msg')}")
                return False
                
        except Exception as e:
            logger.error(f"✗ 发送失败: {e}")
            return False

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    
    sender = FeishuSender()
    
    test_message = """━━━━━━━━━━━━━━━━━━━━
📅 2024年1月8日 AI新闻日报
━━━━━━━━━━━━━━━━━━━━

🚀 【产品发布】
1. **OpenAI发布GPT-5预览版**
   📝 OpenAI推出GPT-5 Turbo预览版，上下文窗口扩展至128K，推理速度提升40%
   🔗 https://openai.com/blog/gpt-5-preview

━━━━━━━━━━━━━━━━━━━━
⏰ 测试消息
"""
    
    sender.send_rich_text_message(test_message)

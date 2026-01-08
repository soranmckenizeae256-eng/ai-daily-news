#!/usr/bin/env python3
"""
AI Daily News Collector - Main Entry Point
每日AI新闻收集与推送系统
"""

import os
import sys
import logging
from datetime import datetime
from pathlib import Path

current_dir = Path(__file__).parent
sys.path.insert(0, str(current_dir))

from news_collector import NewsCollector
from feishu_sender import FeishuSender

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def main():
    """主函数"""
    logger.info("=" * 60)
    logger.info("🤖 AI Daily News Collector Started")
    logger.info(f"⏰ 执行时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    logger.info("=" * 60)
    
    collector = NewsCollector()
    
    articles = collector.collect_all_news()
    
    if not articles:
        logger.warning("未收集到任何新闻，退出执行")
        return
        
    processed_articles = collector.process_articles(articles)
    
    date_str = datetime.now().strftime('%Y年%m月%d日')
    report = collector.generate_daily_report(processed_articles, date_str)
    
    logger.info("\n" + "=" * 60)
    logger.info("生成的日报预览:")
    logger.info("=" * 60)
    logger.info("\n" + report)
    
    logger.info(f"飞书Webhook URL配置状态: {'已配置' if os.environ.get('FEISHU_WEBHOOK_URL') else '未配置'}")
    if os.environ.get('FEISHU_WEBHOOK_URL'):
        sender = FeishuSender()
        logger.info("开始发送消息到飞书...")
        # 尝试使用更简单可靠的文本消息格式
        success = sender.send_text_message(report)
        logger.info(f"飞书消息发送结果: {'成功' if success else '失败'}")
    else:
        logger.warning("未配置飞书Webhook URL，跳过发送")
        
    logger.info("\n" + "=" * 60)
    logger.info("✅ 任务执行完成")
    logger.info("=" * 60)

if __name__ == "__main__":
    main()

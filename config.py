import os
import sys
import json
import logging
from datetime import datetime
from pathlib import Path

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

NEWS_CATEGORIES = {
    '🚀 产品发布': ['product', 'launch', 'release', 'announce', 'introduce', 'new feature', 'unveil', 'debut'],
    '💰 投融资': ['funding', 'invest', 'raise', 'round', ' Series', 'acquire', 'acquisition', 'ipo', 'valuation', 'million', 'billion'],
    '🔬 技术突破': ['research', 'paper', 'breakthrough', 'model', 'performance', 'state-of-the-art', 'sota', 'improve', 'accuracy', 'benchmark', 'arxiv'],
    '🎯 行业观点': ['opinion', '观点', 'predict', 'forecast', '未来', '趋势', '专家', 'ceo', 'founder', 'argue', 'concern', '警告'],
    '📊 其他要闻': []
}

CATEGORY_KEYWORDS = {
    '🚀 产品发布': ['product', 'launch', 'release', 'announce', 'introduce', 'new feature', 'unveil', 'debut', 'launch', 'release'],
    '💰 投融资': ['funding', 'invest', 'raise', 'round', 'acquire', 'acquisition', 'ipo', 'valuation', 'series a', 'series b', 'series c', 'strategic investment'],
    '🔬 技术突破': ['research', 'paper', 'breakthrough', 'model', 'performance', 'state-of-the-art', 'sota', 'improve', 'accuracy', 'benchmark', 'arxiv', 'language model', 'llm', 'training', 'inference'],
    '🎯 行业观点': ['opinion', 'predict', 'forecast', 'trend', 'concern', 'warning', 'criticize', 'praise', 'ceo', 'founder', 'expert', 'analyst', 'perspective', 'view'],
    '📊 其他要闻': []
}

FEISHU_WEBHOOK_URL = os.environ.get('FEISHU_WEBHOOK_URL', '')

DATETIME_FORMAT = '%Y年%m月%d日'
NEWS_DATE_FORMAT = '%Y-%m-%d'

MAX_NEWS_PER_CATEGORY = 4
TOTAL_NEWS_COUNT = 20

RSS_SOURCES = {
    '国际': [
        'https://openai.com/blog/rss.xml',
        'https://blog.google/rss/news_ai.xml',
        'https://www.anthropic.com/rss.xml',
        'https://techcrunch.com/feed/',
        'https://venturebeat.com/ai/feed/',
        'https://www.artificialintelligence-news.com/feed/',
    ],
    '国内': [
        'https://www.jiqizhixin.com/rss',
        'https://www.xianjichina.com/rss',
        'http://www.raincent.com/rss',
        'https://www.36kr.com/feed/',
    ]
}

HTTP_SOURCES = {
    '国际': [
        {
            'name': 'Hacker News AI',
            'url': 'https://news.ycombinator.com/',
            'category_keywords': ['AI', 'artificial intelligence', 'machine learning', 'GPT', 'LLM', 'OpenAI', 'Google AI', 'Anthropic']
        },
        {
            'name': 'Reddit Machine Learning',
            'url': 'https://www.reddit.com/r/MachineLearning/new.json?limit=50',
            'category_keywords': ['AI', 'machine learning', 'deep learning', 'NLP', 'computer vision']
        },
    ],
    '国内': [
        {
            'name': '微博AI热搜',
            'url': 'https://weibo.com/ajax/statuses/mymblog?uid=6170256793&feature=0&is_all=1&is_search=0&key_word=AI&starttime=0&endtime=0&is_all=1&is_search=0',
            'category_keywords': ['AI', '人工智能', 'ChatGPT', 'GPT', '大模型', 'AIGC']
        }
    ]
}

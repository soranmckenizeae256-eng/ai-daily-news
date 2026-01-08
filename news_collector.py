import os
import sys
import json
import logging
from datetime import datetime
from pathlib import Path

current_dir = Path(__file__).parent
sys.path.insert(0, str(current_dir))

try:
    import requests
    import feedparser
    from bs4 import BeautifulSoup
    from openai import OpenAI
    import httpx
except ImportError as e:
    logging.error(f"导入依赖失败: {e}")
    logging.info("请运行: pip install -r requirements.txt")
    sys.exit(1)

from config import (
    FEISHU_WEBHOOK_URL,
    NEWS_CATEGORIES,
    CATEGORY_KEYWORDS,
    DATETIME_FORMAT,
    MAX_NEWS_PER_CATEGORY,
    TOTAL_NEWS_COUNT,
    RSS_SOURCES,
    HTTP_SOURCES,
    AI_PROVIDER,
    OPENAI_API_KEY,
    DEEPSEEK_API_KEY,
    DEEPSEEK_API_BASE
)

logger = logging.getLogger(__name__)

class NewsCollector:
    def __init__(self):
        self.articles = []
<<<<<<< HEAD
        self.client = None
        self.ai_provider = AI_PROVIDER.lower()
        
        logger.info(f"AI提供商配置: {self.ai_provider}")
        logger.info(f"DEEPSEEK_API_KEY是否存在: {'是' if DEEPSEEK_API_KEY else '否'}")
        logger.info(f"OPENAI_API_KEY是否存在: {'是' if OPENAI_API_KEY else '否'}")
        
        # 初始化AI客户端
        if self.ai_provider == 'deepseek':
            if DEEPSEEK_API_KEY:
                logger.info("正在初始化DeepSeek客户端...")
                self.client = OpenAI(
                    api_key=DEEPSEEK_API_KEY,
                    base_url=DEEPSEEK_API_BASE
                )
                logger.info("DeepSeek客户端初始化成功")
            else:
                logger.error("DeepSeek API密钥不存在，无法初始化客户端")
        elif self.ai_provider == 'openai':
            if OPENAI_API_KEY:
                logger.info("正在初始化OpenAI客户端...")
                self.client = OpenAI(
                    api_key=OPENAI_API_KEY
                )
                logger.info("OpenAI客户端初始化成功")
            else:
                logger.error("OpenAI API密钥不存在，无法初始化客户端")
        
        if not self.client:
            logger.warning("未配置有效的AI API密钥，将使用原始标题")
=======
        self.client = OpenAI(
            api_key=os.environ.get('OPENAI_API_KEY', ''),
<<<<<<< HEAD
=======
            http_client=httpx(proxies=os.environ.get('HTTP_PROXY', None))
>>>>>>> 8af3ff9 (feat: 初始化AI新闻日报项目)
        )
>>>>>>> a60790c (feat: 添加详细调试日志和配置文件修复)
        
    def parse_rss_feed(self, feed_url, source_name):
        """解析RSS订阅源"""
        try:
            logger.info(f"正在解析RSS源: {source_name}")
            headers = {
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
            }
            response = httpx.get(feed_url, headers=headers, timeout=30.0)
            response.raise_for_status()
            
            feed = feedparser.parse(response.text)
            
            for entry in feed.entries[:10]:
                article = {
                    'title': entry.get('title', '').strip(),
                    'link': entry.get('link', '').strip(),
                    'published': entry.get('published', '').strip() or entry.get('updated', '').strip(),
                    'summary': entry.get('summary', '').strip(),
                    'source': source_name,
                    'language': 'en'
                }
                if article['title'] and article['link']:
                    self.articles.append(article)
                    
            logger.info(f"  ✓ 从 {source_name} 获取 {min(10, len(feed.entries))} 条新闻")
            
        except Exception as e:
            logger.error(f"  ✗ 解析 {source_name} 失败: {e}")
            
    def fetch_hacker_news(self, source_config):
        """获取Hacker News"""
        try:
            logger.info(f"正在获取: {source_config['name']}")
            headers = {
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
            }
            response = httpx.get(source_config['url'], headers=headers, timeout=30.0)
            response.raise_for_status()
            
            data = response.json()
            hn_items = data.get('data', {}).get('children', [])[:30]
            
            for item in hn_items:
                story = item.get('data', {})
                if story.get('score', 0) >= 50:
                    title = story.get('title', '')
                    url = f"https://news.ycombinator.com/item?id={story.get('id')}"
                    
                    article = {
                        'title': title,
                        'link': url,
                        'published': datetime.now().isoformat(),
                        'summary': '',
                        'source': source_config['name'],
                        'language': 'en',
                        'score': story.get('score', 0)
                    }
                    self.articles.append(article)
                    
            logger.info(f"  ✓ 从 {source_config['name']} 获取热门新闻")
            
        except Exception as e:
            logger.error(f"  ✗ 获取 {source_config['name']} 失败: {e}")
            
    def fetch_reddit(self, source_config):
        """获取Reddit数据"""
        try:
            logger.info(f"正在获取: {source_config['name']}")
            headers = {
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
            }
            response = httpx.get(source_config['url'], headers=headers, timeout=30.0)
            response.raise_for_status()
            
            data = response.json()
            posts = data.get('data', {}).get('children', [])[:20]
            
            for post in posts:
                post_data = post.get('data', {})
                title = post_data.get('title', '')
                self_url = f"https://www.reddit.com{post_data.get('permalink', '')}"
                
                article = {
                    'title': title,
                    'link': self_url,
                    'published': datetime.fromtimestamp(post_data.get('created_utc', 0)).isoformat(),
                    'summary': post_data.get('selftext', '')[:500],
                    'source': source_config['name'],
                    'language': 'en',
                    'score': post_data.get('score', 0)
                }
                self.articles.append(article)
                
            logger.info(f"  ✓ 从 {source_config['name']} 获取 {len(posts)} 条新闻")
            
        except Exception as e:
            logger.error(f"  ✗ 获取 {source_config['name']} 失败: {e}")
            
    def fetch_weibo(self, source_config):
        """获取微博数据"""
        try:
            logger.info(f"正在获取: {source_config['name']}")
            headers = {
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36',
                'cookie': os.environ.get('WEIBO_COOKIE', '')
            }
            response = httpx.get(source_config['url'], headers=headers, timeout=30.0)
            response.raise_for_status()
            
            data = response.json()
            if data.get('ok') == 1:
                list_data = data.get('list', [])
                for item in list_data[:10]:
                    text = item.get('text_raw', '') or item.get('text', '')
                    article = {
                        'title': text[:100] + '...' if len(text) > 100 else text,
                        'link': f"https://weibo.com/0/statuses/{item.get('mid', '')}",
                        'published': item.get('created_at', ''),
                        'summary': text,
                        'source': source_config['name'],
                        'language': 'zh',
                        'attitudes_count': item.get('attitudes_count', 0)
                    }
                    if article['title']:
                        self.articles.append(article)
                        
            logger.info(f"  ✓ 从 {source_config['name']} 获取微博动态")
            
        except Exception as e:
            logger.error(f"  ✗ 获取 {source_config['name']} 失败: {e}")
            
    def collect_all_news(self):
        """收集所有新闻"""
        logger.info("=" * 60)
        logger.info("开始收集AI新闻...")
        logger.info("=" * 60)
        
        logger.info("\n📡 解析RSS订阅源...")
        for category, feeds in RSS_SOURCES.items():
            for feed_url in feeds:
                source_name = feed_url.split('//')[1].split('/')[0]
                self.parse_rss_feed(feed_url, source_name)
                
        logger.info("\n🌐 抓取网页新闻源...")
        for category, sources in HTTP_SOURCES.items():
            for source in sources:
                if 'Hacker' in source['name']:
                    self.fetch_hacker_news(source)
                elif 'Reddit' in source['name']:
                    self.fetch_reddit(source)
                elif '微博' in source['name']:
                    self.fetch_weibo(source)
                    
        logger.info(f"\n✅ 共收集到 {len(self.articles)} 条新闻")
        return self.articles
        
    def categorize_article(self, article):
        """为文章分类"""
        title_lower = article['title'].lower()
        summary_lower = (article.get('summary', '') or '').lower()
        text = title_lower + ' ' + summary_lower
        
        for category, keywords in CATEGORY_KEYWORDS.items():
            if category == '📊 其他要闻':
                continue
            for keyword in keywords:
                if keyword.lower() in text:
                    return category
                    
        return '📊 其他要闻'
        
    def translate_to_chinese(self, text):
        """将英文翻译成中文，保持口语化"""
        if not self.client:
            logger.warning("AI客户端未初始化，跳过翻译")
            return text
            
        try:
            logger.info(f"开始翻译文本: {text[:50]}...")
            prompt = f"""
请将以下英文文本翻译成中文，要求：
1. 保持口语化，符合中国人的阅读习惯
2. 不要直译，要流畅自然
3. 保留新闻的核心信息
4. 直接输出翻译结果，不要添加任何解释

文本：{text}
"""
            
            # 根据AI提供商选择合适的模型
            model = "deepseek-chat" if self.ai_provider == 'deepseek' else "gpt-3.5-turbo"
            logger.info(f"使用模型: {model}")
            
            response = self.client.chat.completions.create(
                model=model,
                messages=[{"role": "user", "content": prompt}],
                max_tokens=200,
                temperature=0.7
            )
            
            translation = response.choices[0].message.content.strip()
            logger.info(f"翻译结果: {translation}")
            return translation if translation else text
            
        except Exception as e:
            logger.error(f"翻译失败: {e}")
            return text
            
    def summarize_with_ai(self, article):
        """使用AI总结文章，生成中文口语化摘要"""
        title = article['title']
        summary = article.get('summary', '')[:500]
        
        logger.info(f"处理文章: {title[:50]}...")
        is_chinese = any(ord(c) > 127 for c in title)
        logger.info(f"标题是否为中文: {'是' if is_chinese else '否'}")
        
        # 先将英文标题翻译成中文
        if is_chinese:
            chinese_title = title
            logger.info(f"标题为中文，直接使用: {chinese_title}")
        else:
            chinese_title = self.translate_to_chinese(title)
            article['translated_title'] = chinese_title
            logger.info(f"英文标题翻译为: {chinese_title}")
        
        if not self.client:
            logger.info("AI客户端未初始化，使用原始标题作为摘要")
            return chinese_title
            
        try:
            logger.info("开始生成摘要...")
            prompt = f"""
请用一句大白话总结以下AI新闻标题和摘要（20-30字以内），使其通俗易懂：

标题: {chinese_title}
摘要: {summary}

要求：
1. 用简单的中文口语解释新闻内容
2. 不要包含公司名称
3. 直接输出总结，不要添加任何解释
"""
            
            # 根据AI提供商选择合适的模型
            model = "deepseek-chat" if self.ai_provider == 'deepseek' else "gpt-3.5-turbo"
            logger.info(f"使用模型: {model}")
            
            response = self.client.chat.completions.create(
                model=model,
                messages=[{"role": "user", "content": prompt}],
                max_tokens=50,
                temperature=0.7
            )
            
            summary_text = response.choices[0].message.content.strip()
            logger.info(f"生成的摘要: {summary_text}")
            return summary_text if summary_text else chinese_title
            
        except Exception as e:
            logger.error(f"AI总结失败: {e}")
            return chinese_title
            
    def filter_and_categorize(self, articles):
        """过滤和分类文章"""
        unique_articles = {}
        for article in articles:
            link = article['link']
            if link not in unique_articles:
                unique_articles[link] = article
                
        unique_articles = list(unique_articles.values())
        
        categorized = {cat: [] for cat in NEWS_CATEGORIES.keys()}
        
        for article in unique_articles:
            category = self.categorize_article(article)
            article['category'] = category
            categorized[category].append(article)
            
        for category in categorized:
            categorized[category].sort(
                key=lambda x: x.get('score', 0) if 'score' in x else 0, 
                reverse=True
            )
            
        final_selection = []
        for category, articles in categorized.items():
            final_selection.extend(articles[:MAX_NEWS_PER_CATEGORY])
            
        if len(final_selection) > TOTAL_NEWS_COUNT:
            sorted_articles = sorted(
                final_selection, 
                key=lambda x: x.get('score', 0) if 'score' in x else 0, 
                reverse=True
            )
            final_selection = sorted_articles[:TOTAL_NEWS_COUNT]
            
        return final_selection
        
    def process_articles(self, articles):
        """处理和总结文章"""
        logger.info("\n🔄 正在处理和总结新闻...")
        
        selected_articles = self.filter_and_categorize(articles)
        
        processed_articles = []
        for i, article in enumerate(selected_articles, 1):
            article['index'] = i
            article['summary_ai'] = self.summarize_with_ai(article)
            processed_articles.append(article)
            
        logger.info(f"  ✓ 处理完成 {len(processed_articles)} 条新闻")
        return processed_articles
        
    def generate_daily_report(self, articles, date_str=None):
        """生成每日日报"""
        if not date_str:
            date_str = datetime.now().strftime(DATETIME_FORMAT)
            
        report_lines = []
        report_lines.append("━━━━━━━━━━━━━━━━━━━━")
        report_lines.append(f"📅 {date_str} AI新闻日报")
        report_lines.append("━━━━━━━━━━━━━━━━━━━━")
        report_lines.append("")
        
        categories_order = ['🚀 产品发布', '💰 投融资', '🔬 技术突破', '🎯 行业观点', '📊 其他要闻']
        
        for category in categories_order:
            category_articles = [a for a in articles if a.get('category') == category]
            if category_articles:
                report_lines.append(f"{category}")
                for article in category_articles:
                    # 使用翻译后的标题，如果没有则使用原始标题
                    display_title = article.get('translated_title', article['title'])
                    report_lines.append(f"{article['index']}. **{display_title}**")
                    report_lines.append(f"   📝 {article['summary_ai']}")
                    report_lines.append(f"   🔗 {article['link']}")
                    report_lines.append("")
                    
        report_lines.append("━━━━━━━━━━━━━━━━━━━━")
        report_lines.append(f"⏰ 每天早上8:00自动推送 | 共{len(articles)}条要闻")
        
        return '\n'.join(report_lines)

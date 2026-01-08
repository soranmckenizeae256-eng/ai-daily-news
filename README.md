# 🤖 AI Daily News - 每日AI新闻日报自动收集与推送系统

自动收集国内外AI新闻，翻译整理后每天早上8:00通过飞书群机器人推送给您。

## ✨ 功能特性

- **📡 多源采集**：从20+个权威渠道自动采集AI新闻
- **🔄 自动翻译**：使用AI将英文新闻翻译成中文
- **📊 智能分类**：自动将新闻分类为5个类别
- **📝 通俗总结**：用大白话提炼每条新闻的核心内容
- **⏰ 定时推送**：每天早上8:00自动发送到飞书群
- **🆓 完全免费**：基于GitHub Actions，无需服务器费用

## 📋 新闻来源

### 国际渠道
- 官方博客：OpenAI、Google AI、Anthropic、Meta AI
- 技术社区：Hacker News、Reddit MachineLearning
- 科技媒体：TechCrunch、VentureBeat AI
- AI专业媒体：MIT Technology Review、AI Weekly

### 国内渠道
- 专业媒体：量子位、机器之心、新智元
- 科技媒体：36氪、虎嗅

## 📂 项目结构

```
ai-daily-news/
├── main.py                    # 主入口文件
├── config.py                  # 配置文件
├── news_collector.py          # 新闻采集模块
├── feishu_sender.py          # 飞书发送模块
├── requirements.txt          # Python依赖
├── README.md                 # 项目说明文档
└── .github/
    └── workflows/
        └── daily-news.yml    # GitHub Actions配置
```

## 🚀 快速开始

### 1. Fork本项目

点击右上角 **Fork** 按钮，将项目复制到您的GitHub账户。

### 2. 配置飞书群机器人

#### 创建飞书群机器人：
1. 打开飞书 → 创建或选择一个群聊
2. 点击群设置 → 群机器人 → 添加机器人
3. 选择 **自定义机器人** → 填写信息并添加
4. **保存生成的Webhook URL**

#### 配置GitHub Secrets：
1. 进入您的GitHub仓库
2. 点击 **Settings** → **Secrets and variables** → **Actions**
3. 点击 **New repository secret**
4. 添加以下Secrets：

| Name | Value |
|------|-------|
| `FEISHU_WEBHOOK_URL` | 您的飞书Webhook URL |

#### 可选配置：
| Name | Value | 说明 |
|------|-------|------|
| `OPENAI_API_KEY` | sk-xxx | OpenAI API密钥，用于AI翻译和总结 |
| `HTTP_PROXY` | http://127.0.0.1:7890 | HTTP代理，用于访问外网 |

### 3. 手动测试（可选）

1. 进入 **Actions** 标签页
2. 选择 **AI Daily News** 工作流
3. 点击 **Run workflow** 手动触发测试

### 4. 查看执行结果

- 进入 **Actions** 标签页查看执行日志
- 检查飞书群是否收到测试消息

## ⏰ 定时任务

系统默认配置为每天 **UTC 0:00** 执行（北京时间 8:00）。

如需调整执行时间，编辑 `.github/workflows/daily-news.yml`：

```yaml
schedule:
  - cron: '0 8 * * *'  # 每天北京时间 8:00
```

## 📊 新闻分类

所有新闻自动分为5类：

1. 🚀 **产品发布** - 新AI产品/功能发布
2. 💰 **投融资** - AI公司融资/收购动态
3. 🔬 **技术突破** - 研究论文/技术创新
4. 🎯 **行业观点** - 大佬观点/行业争议
5. 📊 **其他要闻** - 不属于以上类别的要闻

## 📱 消息示例

```
━━━━━━━━━━━━━━━━━━━━
📅 2024年1月8日 AI新闻日报
━━━━━━━━━━━━━━━━━━━━

🚀 【产品发布】
1. **OpenAI发布GPT-5预览版**
   📝 OpenAI推出GPT-5 Turbo预览版，上下文窗口扩展至128K，推理速度提升40%
   🔗 https://openai.com/blog/gpt-5-preview

💰 【投融资动态】
2. **AI搜索公司Perplexity完成新一轮融资**
   📝 AI搜索独角兽Perplexity完成1亿美元融资，估值达90亿美元
   🔗 https://techcrunch.com/perplexity-funding

...（共20条）

━━━━━━━━━━━━━━━━━━━━
⏰ 每天早上8:00自动推送 | 共20条要闻
```

## 🛠️ 本地运行

### 环境要求
- Python 3.11+
- pip

### 安装依赖
```bash
pip install -r requirements.txt
```

### 运行程序
```bash
# 设置环境变量
export FEISHU_WEBHOOK_URL="your-webhook-url"
export OPENAI_API_KEY="your-api-key"

# 运行
python main.py
```

## ⚙️ 自定义配置

编辑 `config.py` 文件：

```python
# 调整每类新闻数量
MAX_NEWS_PER_CATEGORY = 4

# 调整总新闻数量
TOTAL_NEWS_COUNT = 20

# 添加新的RSS源
RSS_SOURCES = {
    '国际': [...],
    '国内': [...]
}

# 调整分类关键词
CATEGORY_KEYWORDS = {...}
```

## ❓ 常见问题

### Q: GitHub Actions执行失败怎么办？
A: 进入 **Actions** 标签页，查看详细错误日志。常见问题：
- Secrets未配置或配置错误
- 网络问题（部分源需要代理）

### Q: 如何添加新的新闻源？
A: 在 `config.py` 中修改 `RSS_SOURCES` 或 `HTTP_SOURCES` 配置。

### Q: 飞书消息发送失败？
A: 检查Webhook URL是否正确，确保URL未过期。

### Q: 想要中文标题加粗但原文是英文？
A: 配置 `OPENAI_API_KEY` 后，系统会自动翻译并总结。

## 📝 更新日志

**v1.0.0** (2024-01-08)
- ✨ 初始版本发布
- 📡 支持多源新闻采集
- 🔄 自动分类和总结
- 📱 飞书群机器人推送

## 🤝 贡献

欢迎提交 Issue 或 Pull Request！

## 📄 License

MIT License

---

💡 **提示**：首次配置后，系统会在第二天早上8:00自动发送第一条日报。在此之前，您可以手动触发测试确保一切正常。

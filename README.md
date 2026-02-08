# Daily Intel

Mako 的日常情报站，记录市场研究、投资情报与行业洞察。

> 不只是资讯，更有技术趋势与多元观点的碰撞

## 🌐 在线访问

https://makoshan.github.io/daily-intel/

---

## 🚀 快速开始（新目录结构）

### 本地开发

```bash
# 进入项目目录
cd workspace/projects/daily-intel

# 安装依赖
bundle install

# 本地预览
bundle exec jekyll serve

# 访问 http://localhost:4000/daily-intel/
```

### 手动生成日报

```bash
cd scripts

# 1. 配置 API Key
cp .env.example .env
# 编辑 .env 填入 OPENAI_API_KEY

# 2. 安装依赖
pip install -r requirements.txt

# 3. 运行生成器
python daily-intel-pipeline.py
```

---

## 📁 目录结构

```
daily-intel/
├── 📁 _posts/              # 文章目录
│   └── YYYY-MM-DD-daily-intel.md
├── 📁 _layouts/            # Jekyll 布局
├── 📁 scripts/             # 自动化脚本
│   ├── daily-intel-pipeline.py   # 主流程
│   ├── rss_fetcher.py            # RSS 抓取
│   ├── hn_comment_analyzer.py    # HN 评论分析
│   ├── content_enhancer.py       # AI 内容增强
│   ├── .env.example              # API Key 配置模板
│   └── SECURITY.md               # 安全指南
├── 📁 .github/workflows/   # GitHub Actions
│   └── daily-intel.yml     # 自动定时任务
├── 📁 assets/              # 静态资源
├── 📄 index.html           # 首页
└── 📄 _config.yml          # Jekyll 配置
```

---

## 🤖 自动化流程

### 功能

1. **数据抓取**
   - News Hacker RSS
   - Hacker Podcast RSS
   - Hacker News Top Stories
   - HN 评论分析

2. **AI 内容增强**
   - 技术背景分析
   - 商业价值评估
   - 多元观点聚合
   - 标签自动生成

3. **自动发布**
   - 生成 Markdown
   - Git 提交
   - 自动推送
   - GitHub Pages 部署

### 定时任务

**GitHub Actions** 每天 08:00 (CST) 自动运行：
- 抓取最新资讯
- AI 分析生成
- 自动提交部署

**手动触发**:
```bash
cd scripts
python daily-intel-pipeline.py
```

---

## 🏷️ 标签体系

### 技术标签
- `#AI` - 人工智能
- `#Agent` - 智能体
- `#编程` - 开发工具
- `#安全` - 网络安全
- `#开源` - 开源项目

### 商业标签
- `#投资` - 投资理财
- `#创业` - 创业产品
- `#市场` - 市场动态

---

## 📝 数据源

| 平台 | 数量 | 重点方向 |
|------|------|----------|
| Product Hunt | 10 条 | AI 编程工具、效率应用 |
| Hacker News | 15 条 | 本地 AI、Agent 范式 |
| GitHub Trending | 10 条 | AI 安全、Skills 生态 |
| 少数派 | 10 条 | 生活方式、科技文化 |
| 华尔街见闻 | 10 条 | 太空经济、投资市场 |
| 虎扑 | 10 条 | 体育动态 |

---

## 🔐 安全配置

**⚠️ 重要**: API Key 不要提交到 GitHub！

1. 本地开发: 使用 `scripts/.env` 文件（已忽略）
2. GitHub Actions: 使用 Secrets (`OPENAI_API_KEY`)

详见: `scripts/SECURITY.md`

---

## 📊 统计

- 总文章数：{{ site.posts | size }}
- 最新更新：{{ site.time | date: "%Y-%m-%d %H:%M" }}
- 数据源：6 个平台
- 自动化：AI 增强 + 定时发布

---

## 📜 License

MIT

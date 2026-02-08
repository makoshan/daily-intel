# Daily Intel 数据源配置

## 新闻来源平台

| 平台 | 数量 | 重点方向 | 抓取方式 |
|------|------|----------|----------|
| **Product Hunt** | 10 条 | AI 编程工具、效率应用 | RSS/API |
| **Hacker News** | 15 条 | 本地 AI、Agent 范式、开源项目 | Firebase API |
| **GitHub Trending** | 10 条 | AI 安全、Skills 生态、系统工具 | GitHub API |
| **少数派** | 10 条 | 生活方式、科技文化 | RSS |
| **华尔街见闻** | 10 条 | 太空经济、投资市场、宏观政治 | RSS |
| **虎扑** | 10 条 | 体育动态 | RSS |

**总计**: 65 条资讯/天

---

## 新增 RSS 源

| 源名称 | URL | 类型 |
|--------|-----|------|
| News Hacker | https://api.newshacker.me/rss | 极客洞察 |
| Hacker Podcast | https://hacker-podcast.agi.li/rss.xml | 播客 |

---

## 平台分类标签

### 技术类
- `#AI` - 人工智能
- `#Agent` - 智能体
- `#编程` - 开发工具
- `#开源` - 开源项目
- `#安全` - 网络安全

### 商业类
- `#投资` - 投资理财
- `#创业` - 创业产品
- `#市场` - 市场动态

### 生活类
- `#生活方式` - 效率、工具
- `#科技文化` - 科技人文
- `#体育` - 体育动态

---

## 抓取频率

| 平台 | 频率 | 时间 |
|------|------|------|
| Product Hunt | 每日 | 08:00 CST |
| Hacker News | 每日 | 08:00 CST |
| GitHub Trending | 每日 | 08:00 CST |
| 少数派 | 每日 | 08:00 CST |
| 华尔街见闻 | 每日 | 08:00 CST |
| 虎扑 | 每日 | 08:00 CST |
| News Hacker | 每日 | 08:00 CST |

---

## 数据存储

- **原始数据**: `data/raw/YYYYMMDD/`
- **处理后**: `_posts/YYYY-MM-DD-daily-intel.md`
- **历史归档**: `archive/`

---

*最后更新: 2026-02-08*

---
layout: default
title: 首页
---

## 🚀 欢迎来到 Daily Intel

每日科技资讯自动收集与 AI 总结

---

## 📊 最新情报

{% for post in site.posts limit:5 %}
### [{{ post.title }}]({{ post.url | relative_url }})
*{{ post.date | date: "%Y年%m月%d日" }}*

{{ post.excerpt | strip_html | truncate: 100 }}

[阅读全文 →]({{ post.url | relative_url }})

---
{% endfor %}

## 📡 数据来源

Daily Intel 每天自动从以下平台收集资讯：

| 平台 | 类型 | 说明 |
|------|------|------|
| Product Hunt | 产品发布 | 最新科技产品 |
| Hacker News | 技术社区 | 开发者热点讨论 |
| GitHub Trending | 开源项目 | 热门代码仓库 |
| 少数派 | 中文媒体 | 深度科技文章 |
| 华尔街见闻 | 财经新闻 | 科技与商业 |
| 虎扑 | 社区讨论 | 多元视角 |

## 🔄 自动化流程

```
每天 08:00 (北京时间)
    ↓
自动抓取 6 个平台
    ↓
AI 生成中文总结
    ↓
发布到本页面
```

## 📈 报告内容

每份日报包含：

- 📈 **数据概览** — 各平台资讯数量统计
- 🔥 **今日热点** — 最受欢迎的资讯
- 💡 **技术趋势** — 热门技术标签分析
- 📰 **平台精选** — 各平台重点内容
- ✅ **行动建议** — 值得关注的内容
- 🎯 **一句话总结** — 今日科技圈精华

---

[查看历史归档 →](/archive/)

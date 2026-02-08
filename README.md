# Daily Intel

Mako 的日常情报站，记录市场研究、投资情报与行业洞察。

## 🌐 在线访问

https://makoshan.github.io/daily-intel/

## 📝 写作指南

### 新建日报

在 `_posts/` 目录下创建文件，文件名格式：

```
YYYY-MM-DD-title.md
```

例如：
```
2026-02-08-daily-intel.md
```

### 文章模板

```yaml
---
layout: post
title: "2026年2月8日情报日报"
date: 2026-02-08 08:00:00 +0800
categories: daily
tags: [Web3, AI, Market]
---

## 🪙 加密市场

内容...

## 🤖 AI 动态

内容...

## 📊 宏观观察

内容...
```

## 🚀 本地预览

```bash
bundle install
bundle exec jekyll serve
```

访问 http://localhost:4000/daily-intel/

## 📊 统计

- 总文章数：{{ site.posts | size }}
- 最新更新：{{ site.time | date: "%Y-%m-%d %H:%M" }}

---
layout: default
title: 历史归档
permalink: /archive/
---

## 📚 历史归档

{% assign posts_by_year = site.posts | group_by_exp: "post", "post.date | date: '%Y'" %}

{% for year in posts_by_year %}
### {{ year.name }}年

{% assign posts_by_month = year.items | group_by_exp: "post", "post.date | date: '%m'" %}

{% for month in posts_by_month %}
**{{ month.name }}月**

{% for post in month.items %}
- [{{ post.date | date: "%m月%d日" }} - {{ post.title }}]({{ post.url | relative_url }})
{% endfor %}

{% endfor %}
{% endfor %}

---

[← 返回首页](/)

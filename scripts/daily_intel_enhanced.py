#!/usr/bin/env python3
"""
Daily Intel 增强版生成器
整合功能:
1. HN 评论抓取与 AI 分析
2. AI 内容增强
3. RSS 数据源抓取

用法:
    export OPENAI_API_KEY="your-key"
    python daily_intel_enhanced.py
"""

import os
import sys
import json
from datetime import datetime
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

# 导入模块
from hn_comment_analyzer import HNCommentAnalyzer, analyze_hn_story
from content_enhancer import ContentEnhancer, enhance_article
from rss_fetcher import RSSFetcher, fetch_rss_sources


class DailyIntelGenerator:
    """Daily Intel 增强版生成器"""
    
    def __init__(self):
        self.api_key = os.getenv("OPENAI_API_KEY")
        self.api_base = os.getenv("OPENAI_BASE_URL", "https://api.openai.com/v1")
        
        if not self.api_key:
            raise ValueError("OPENAI_API_KEY not set!")
        
        self.hn_analyzer = HNCommentAnalyzer(self.api_key, self.api_base)
        self.content_enhancer = ContentEnhancer(self.api_key, self.api_base)
        self.rss_fetcher = RSSFetcher()
    
    def generate_enhanced_post(self, date_str: str = None) -> str:
        """
        生成增强版 Daily Intel 文章
        """
        if date_str is None:
            date_str = datetime.now().strftime("%Y-%m-%d")
        
        print(f"🚀 Generating Daily Intel for {date_str}...\n")
        
        # 1. 抓取 RSS 数据源
        print("📡 Fetching RSS sources...")
        rss_data = self.rss_fetcher.fetch_all_sources(limit_per_source=5)
        
        # 2. 处理 RSS 文章（内容增强）
        print("\n🤖 Enhancing articles with AI...")
        enhanced_articles = []
        
        for source_key, source_data in rss_data.items():
            for article in source_data["articles"][:3]:  # 每源取前3篇
                print(f"  Enhancing: {article['title'][:50]}...")
                enhanced = self.content_enhancer.enhance_article(
                    article["title"],
                    article.get("description", ""),
                    article["link"]
                )
                enhanced["source"] = source_data["name"]
                enhanced_articles.append(enhanced)
        
        # 3. 查找 HN 上的相关讨论
        print("\n💬 Fetching HN discussions...")
        hn_discussions = []
        
        # 基于文章标题在 HN 搜索（简化版：取 Top Stories）
        top_stories = self.hn_analyzer.fetch_top_stories(limit=10)
        for story_id in top_stories[:3]:  # 取前3篇
            try:
                story_data = self.hn_analyzer.fetch_story_with_comments(story_id)
                if story_data and story_data.get("comments"):
                    print(f"  Analyzing HN comments for: {story_data['story']['title'][:50]}...")
                    analysis = self.hn_analyzer.analyze_comments_with_ai(story_data)
                    if "analysis" in analysis:
                        hn_discussions.append(analysis)
            except Exception as e:
                print(f"  Error analyzing story {story_id}: {e}")
        
        # 4. 生成 Markdown 内容
        print("\n📝 Generating Markdown...")
        markdown = self._generate_markdown(date_str, enhanced_articles, hn_discussions, rss_data)
        
        return markdown
    
    def _generate_markdown(self, date_str: str, enhanced_articles: list, hn_discussions: list, rss_data: dict) -> str:
        """生成 Markdown 格式的文章"""
        
        formatted_date = datetime.strptime(date_str, "%Y-%m-%d").strftime("%Y年%m月%d日")
        
        md = f"""---
layout: post
title: "每日科技情报 - {formatted_date}"
date: {date_str} 08:00:00 +0800
categories: daily
tags: [科技, AI, 增强版]
permalink: /{date_str.replace('-', '')}.html
---

# 📊 每日科技情报 | {formatted_date}

> 不只是资讯，更有技术趋势与多元观点的碰撞
> 
> 🤖 **AI 增强版** | 自动分析 HN 评论 | 内容深度解读 | RSS 聚合

---

## 🔥 AI 深度分析文章

"""
        
        # 添加 AI 增强的文章
        for i, article in enumerate(enhanced_articles[:5], 1):
            if article.get("status") == "success":
                md += f"""### {i}. {article['title']}

#来自 {article['source']}

{article['enhanced_analysis']}

🔗 [查看原文]({article['url']})

---

"""
        
        # 添加 HN 讨论分析
        if hn_discussions:
            md += """## 💬 HN 社区讨论精选

"""
            for disc in hn_discussions:
                story = disc.get("story", {})
                md += f"""### {story.get('title', '')}

📊 **{disc.get('comment_count', 0)} 条评论** | 🔥 {story.get('score', 0)} 分

{disc.get('analysis', '分析生成中...')}

🔗 [查看 HN 讨论](https://news.ycombinator.com/item?id={story.get('id', '')})

---

"""
        
        # 添加 RSS 源汇总
        md += """## 📡 更多资讯

"""
        for source_key, source_data in rss_data.items():
            md += f"""### {source_data['name']} | {source_data['category']}

"""
            for article in source_data["articles"][3:6]:  # 取第4-6篇
                md += f"""- [{article['title']}]({article['link']})
"""
            md += "\n"
        
        # 添加页脚
        md += f"""---

*报告由 AI 自动生成 | 数据截止 {date_str} 08:00 CST*
*包含 HN 评论分析、AI 内容增强、RSS 聚合*
"""
        
        return md
    
    def save_post(self, markdown: str, date_str: str = None):
        """保存文章到 _posts 目录"""
        if date_str is None:
            date_str = datetime.now().strftime("%Y-%m-%d")
        
        filename = f"{date_str}-daily-intel-enhanced.md"
        filepath = os.path.join("_posts", filename)
        
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(markdown)
        
        print(f"\n✅ Saved to {filepath}")
        return filepath


def main():
    """主函数"""
    print("="*60)
    print("Daily Intel 增强版生成器")
    print("="*60)
    
    # 检查 API Key
    if not os.getenv("OPENAI_API_KEY"):
        print("\n❌ Error: OPENAI_API_KEY not set!")
        print("Please set your OpenAI API key:")
        print("  export OPENAI_API_KEY='your-key'")
        sys.exit(1)
    
    # 生成文章
    generator = DailyIntelGenerator()
    
    # 可以指定日期，默认今天
    date_str = sys.argv[1] if len(sys.argv) > 1 else None
    
    markdown = generator.generate_enhanced_post(date_str)
    
    # 保存
    filepath = generator.save_post(markdown, date_str)
    
    print(f"\n🎉 Done! Preview: {filepath}")
    print("\nNext steps:")
    print("  1. Review the generated content")
    print("  2. git add & commit")
    print("  3. git push to deploy")


if __name__ == "__main__":
    main()

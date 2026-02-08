#!/usr/bin/env python3
"""
Daily Intel 完整自动化流程

功能：
1. 抓取多数据源（HN、RSS、Product Hunt、GitHub）
2. AI 分析生成深度内容
3. 生成 Jekyll 格式文章
4. 自动 Git 提交推送

用法：
    export OPENAI_API_KEY="sk-xxx"
    python daily_intel_pipeline.py
"""

import os
import sys
import json
import subprocess
from datetime import datetime, timedelta
from typing import List, Dict, Optional
from pathlib import Path

# 加载环境变量
from dotenv import load_dotenv
load_dotenv()

# 导入同目录模块
from rss_fetcher import fetch_rss_sources, fetch_single_feed
from content_enhancer import ContentEnhancer
from hn_comment_analyzer import HNCommentAnalyzer


class DailyIntelPipeline:
    """Daily Intel 完整自动化流程"""
    
    def __init__(self):
        self.api_key = os.getenv("OPENAI_API_KEY")
        self.api_base = os.getenv("OPENAI_BASE_URL", "https://api.openai.com/v1")
        
        if not self.api_key:
            raise ValueError("OPENAI_API_KEY not set!")
        
        self.enhancer = ContentEnhancer(self.api_key, self.api_base)
        self.hn_analyzer = HNCommentAnalyzer(self.api_key, self.api_base)
        
        self.date = datetime.now()
        self.date_str = self.date.strftime("%Y-%m-%d")
        self.date_display = self.date.strftime("%Y年%m月%d日")
    
    def run_full_pipeline(self) -> str:
        """运行完整流程"""
        print("=" * 70)
        print(f"Daily Intel 自动化流程 - {self.date_display}")
        print("=" * 70)
        
        # Step 1: 抓取数据
        print("\n[1/5] 抓取数据源...")
        data = self.fetch_all_sources()
        
        # Step 2: AI 内容增强
        print("\n[2/5] AI 内容增强...")
        enhanced = self.enhance_content(data)
        
        # Step 3: 生成文章
        print("\n[3/5] 生成 Markdown 文章...")
        markdown = self.generate_markdown(enhanced)
        
        # Step 4: 保存文件
        print("\n[4/5] 保存文章...")
        filepath = self.save_article(markdown)
        
        # Step 5: Git 提交
        print("\n[5/5] Git 提交...")
        self.git_commit_push(filepath)
        
        print("\n" + "=" * 70)
        print("✅ 流程完成!")
        print(f"文章地址: https://makoshan.github.io/daily-intel/{self.date.strftime('%Y%m%d')}.html")
        print("=" * 70)
        
        return filepath
    
    def fetch_all_sources(self) -> Dict:
        """抓取所有数据源"""
        data = {
            "rss": {},
            "hn_top": [],
            "hn_discussions": [],
            "github_trending": []
        }
        
        # 1. RSS 源
        print("  - 抓取 News Hacker RSS...")
        data["rss"]["newshacker"] = fetch_single_feed("https://api.newshacker.me/rss", 5)
        
        print("  - 抓取 Hacker Podcast RSS...")
        data["rss"]["hacker_podcast"] = fetch_single_feed("https://hacker-podcast.agi.li/rss.xml", 3)
        
        # 2. HN Top Stories
        print("  - 抓取 HN Top Stories...")
        top_ids = self.hn_analyzer.fetch_top_stories(limit=10)
        
        for story_id in top_ids[:5]:  # 取前5篇
            try:
                story = self.hn_analyzer.fetch_item(story_id)
                if story and story.get("type") == "story":
                    data["hn_top"].append({
                        "id": story_id,
                        "title": story.get("title", ""),
                        "url": story.get("url", ""),
                        "score": story.get("score", 0),
                        "descendants": story.get("descendants", 0)
                    })
            except Exception as e:
                print(f"    错误: {e}")
        
        # 3. HN 评论分析（取评论最多的2篇）
        print("  - 分析 HN 评论...")
        sorted_by_comments = sorted(data["hn_top"], 
                                   key=lambda x: x.get("descendants", 0), 
                                   reverse=True)
        
        for story in sorted_by_comments[:2]:
            try:
                story_data = self.hn_analyzer.fetch_story_with_comments(story["id"])
                if story_data.get("comments"):
                    analysis = self.hn_analyzer.analyze_comments_with_ai(story_data)
                    data["hn_discussions"].append(analysis)
            except Exception as e:
                print(f"    分析失败: {e}")
        
        print(f"\n  抓取结果:")
        print(f"    - RSS 文章: {len(data['rss'].get('newshacker', []))} 篇")
        print(f"    - HN Top: {len(data['hn_top'])} 篇")
        print(f"    - HN 评论分析: {len(data['hn_discussions'])} 篇")
        
        return data
    
    def enhance_content(self, data: Dict) -> Dict:
        """AI 内容增强"""
        enhanced = {
            "articles": [],
            "hn_discussions": data.get("hn_discussions", [])
        }
        
        # 增强 RSS 文章
        all_articles = []
        for source, articles in data.get("rss", {}).items():
            for article in articles[:3]:  # 每源取3篇
                all_articles.append({
                    **article,
                    "source": source
                })
        
        # 添加 HN Top Stories
        for story in data.get("hn_top", [])[:3]:
            all_articles.append({
                "title": story["title"],
                "link": f"https://news.ycombinator.com/item?id={story['id']}",
                "description": f"HN Top Story - {story['score']} points, {story['descendants']} comments",
                "source": "Hacker News"
            })
        
        # AI 增强
        for i, article in enumerate(all_articles[:5], 1):
            print(f"  增强文章 {i}/5: {article['title'][:40]}...")
            try:
                enhanced_article = self.enhancer.enhance_article(
                    article["title"],
                    article.get("description", ""),
                    article["link"]
                )
                enhanced_article["source"] = article.get("source", "Unknown")
                enhanced["articles"].append(enhanced_article)
            except Exception as e:
                print(f"    失败: {e}")
        
        return enhanced
    
    def generate_markdown(self, enhanced: Dict) -> str:
        """生成 Markdown 文章"""
        
        # 提取标签
        all_tags = ["科技", "AI"]
        for article in enhanced.get("articles", []):
            if article.get("status") == "success":
                tags = self.enhancer.extract_tags(
                    article["title"], 
                    article.get("enhanced_analysis", "")
                )
                all_tags.extend([t.replace("#", "") for t in tags])
        
        # 去重并限制
        unique_tags = list(dict.fromkeys(all_tags))[:5]
        tags_str = ", ".join([f'"{t}"' for t in unique_tags])
        
        md = f"""---
layout: post
title: "每日科技情报 - {self.date_display}"
date: {self.date_str} 08:00:00 +0800
categories: daily
tags: [{tags_str}]
permalink: /{self.date.strftime('%Y%m%d')}.html
---

# 每日科技情报 | {self.date_display}

> 不只是资讯，更有技术趋势与多元观点的碰撞
> 
> 自动生成 | AI 增强 | HN 评论分析 | RSS 聚合

---

## 今日热点

"""
        
        # AI 增强的文章
        for i, article in enumerate(enhanced.get("articles", [])[:5], 1):
            if article.get("status") == "success":
                tags = self.enhancer.extract_tags(article["title"], article.get("enhanced_analysis", ""))
                tags_line = " ".join(tags[:3])
                
                md += f"""### {i}. {article['title']}

{tags_line} #来自 {article['source']}

{article['enhanced_analysis']}

---

"""
        
        # HN 讨论
        if enhanced.get("hn_discussions"):
            md += """## HN 社区观点

"""
            for disc in enhanced["hn_discussions"]:
                story = disc.get("story", {})
                md += f"""### {story.get('title', '')}

{disc.get('comment_count', 0)} 条评论 | {story.get('score', 0)} 分

{disc.get('analysis', '')}

[查看讨论](https://news.ycombinator.com/item?id={story.get('id', '')})

---

"""
        
        # 数据概览
        md += f"""## 数据概览

| 来源 | 数量 | 重点 |
|------|------|------|
| RSS 聚合 | {len([a for a in enhanced.get('articles', []) if a.get('source') != 'Hacker News'])} 篇 | AI、技术趋势 |
| HN Top | {len([a for a in enhanced.get('articles', []) if a.get('source') == 'Hacker News'])} 篇 | 社区热点 |
| HN 讨论 | {len(enhanced.get('hn_discussions', []))} 篇 | 多元观点 |

---

*自动生成于 {self.date.strftime('%Y-%m-%d %H:%M')}*
"""
        
        return md
    
    def save_article(self, markdown: str) -> str:
        """保存文章"""
        filename = f"_posts/{self.date_str}-daily-intel.md"
        
        with open(filename, "w", encoding="utf-8") as f:
            f.write(markdown)
        
        print(f"  已保存: {filename}")
        return filename
    
    def git_commit_push(self, filepath: str):
        """Git 提交并推送"""
        try:
            # 检查 git 状态
            result = subprocess.run(
                ["git", "status", "--short"],
                capture_output=True, text=True, cwd="."
            )
            
            if not result.stdout.strip():
                print("  无变更，跳过提交")
                return
            
            # 添加文件
            subprocess.run(["git", "add", filepath], check=True)
            
            # 提交
            commit_msg = f"Add Daily Intel - {self.date_display}"
            subprocess.run(["git", "commit", "-m", commit_msg], check=True)
            
            # 推送
            subprocess.run(["git", "push", "origin", "master"], check=True)
            
            print("  Git 提交并推送成功")
            
        except subprocess.CalledProcessError as e:
            print(f"  Git 操作失败: {e}")
        except Exception as e:
            print(f"  错误: {e}")


def main():
    """主函数"""
    try:
        pipeline = DailyIntelPipeline()
        pipeline.run_full_pipeline()
    except Exception as e:
        print(f"\n错误: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()

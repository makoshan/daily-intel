#!/usr/bin/env python3
"""
Daily Intel Pipeline - Enhanced Version
整合了多平台数据抓取和 AI 内容增强
"""

import os
import sys
import subprocess
from datetime import datetime
from pathlib import Path

# 添加 src 目录到路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from dotenv import load_dotenv
load_dotenv()

# 导入脚本模块
from rss_fetcher import fetch_single_feed
from content_enhancer import ContentEnhancer
from hn_comment_analyzer import HNCommentAnalyzer

# 导入 src 模块
try:
    from fetcher import IntelAggregator
    USE_ENHANCED_FETCHER = True
except ImportError:
    print("⚠️  Warning: Could not import enhanced fetcher from src/")
    USE_ENHANCED_FETCHER = False


class DailyIntelPipeline:
    """Daily Intel 完整自动化流程 - 增强版"""
    
    def __init__(self):
        self.api_key = os.getenv("OPENAI_API_KEY")
        self.api_base = os.getenv("OPENAI_BASE_URL", "https://api.openai.com/v1")
        
        if not self.api_key:
            raise ValueError("OPENAI_API_KEY not set! Please set it in .env file")
        
        self.enhancer = ContentEnhancer(self.api_key, self.api_base)
        self.hn_analyzer = HNCommentAnalyzer(self.api_key, self.api_base)
        
        self.date = datetime.now()
        self.date_str = self.date.strftime("%Y-%m-%d")
        self.date_display = self.date.strftime("%Y年%m月%d日")
        
        # 初始化增强型抓取器
        if USE_ENHANCED_FETCHER:
            self.aggregator = IntelAggregator()
        else:
            self.aggregator = None
    
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
    
    def fetch_all_sources(self) -> dict:
        """抓取所有数据源 - 使用增强型抓取器"""
        data = {
            "rss": {},
            "hn_top": [],
            "hn_discussions": [],
            "platforms": {}
        }
        
        if USE_ENHANCED_FETCHER and self.aggregator:
            # 使用增强型多平台抓取器
            print("  使用增强型多平台抓取器...")
            try:
                platform_data = self.aggregator.fetch_all()
                data["platforms"] = platform_data
                
                # 统计
                total = sum(len(items) for items in platform_data.values())
                print(f"\n  ✓ 增强型抓取完成: {total} 篇文章")
                for platform, items in platform_data.items():
                    if items:
                        print(f"    - {platform}: {len(items)} 篇")
            except Exception as e:
                print(f"  ✗ 增强型抓取失败: {e}")
                print(f"  回退到基础 RSS 抓取...")
        
        # RSS 源（作为补充或备用）
        print("\n  抓取 RSS 源...")
        try:
            print("    - News Hacker RSS...")
            data["rss"]["newshacker"] = fetch_single_feed("https://api.newshacker.me/rss", 5)
        except Exception as e:
            print(f"      错误: {e}")
        
        try:
            print("    - Hacker Podcast RSS...")
            data["rss"]["hacker_podcast"] = fetch_single_feed("https://hacker-podcast.agi.li/rss.xml", 3)
        except Exception as e:
            print(f"      错误: {e}")
        
        # HN Top Stories
        print("\n  - 抓取 HN Top Stories...")
        try:
            top_ids = self.hn_analyzer.fetch_top_stories(limit=10)
            
            for story_id in top_ids[:5]:
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
        except Exception as e:
            print(f"  HN 抓取失败: {e}")
        
        # HN 评论分析
        print("\n  - 分析 HN 评论...")
        try:
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
        except Exception as e:
            print(f"  HN 评论分析失败: {e}")
        
        # 打印统计
        print(f"\n  抓取结果汇总:")
        print(f"    - RSS 文章: {sum(len(v) for v in data['rss'].values())} 篇")
        print(f"    - HN Top: {len(data['hn_top'])} 篇")
        print(f"    - HN 评论分析: {len(data['hn_discussions'])} 篇")
        if data["platforms"]:
            print(f"    - 其他平台: {sum(len(v) for v in data['platforms'].values())} 篇")
        
        return data
    
    def enhance_content(self, data: dict) -> dict:
        """AI 内容增强"""
        enhanced = {
            "articles": [],
            "hn_discussions": data.get("hn_discussions", [])
        }
        
        # 收集所有文章
        all_articles = []
        
        # 从平台数据收集
        for platform, items in data.get("platforms", {}).items():
            for item in items[:3]:  # 每个平台取前3篇
                all_articles.append({
                    "title": item.get("title", ""),
                    "link": item.get("url", ""),
                    "description": item.get("description", ""),
                    "source": item.get("platform", platform)
                })
        
        # 从 RSS 收集
        for source, articles in data.get("rss", {}).items():
            for article in articles[:3]:
                all_articles.append({
                    **article,
                    "source": source
                })
        
        # 从 HN Top Stories 收集
        for story in data.get("hn_top", [])[:3]:
            all_articles.append({
                "title": story["title"],
                "link": f"https://news.ycombinator.com/item?id={story['id']}",
                "description": f"HN Top Story - {story['score']} points, {story['descendants']} comments",
                "source": "Hacker News"
            })
        
        # AI 增强（限制数量以控制成本）
        max_articles = int(os.getenv("MAX_ARTICLES_PER_RUN", "10"))
        for i, article in enumerate(all_articles[:max_articles], 1):
            print(f"  增强文章 {i}/{min(len(all_articles), max_articles)}: {article['title'][:40]}...")
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
        
        print(f"\n  ✓ 增强完成: {len(enhanced['articles'])} 篇")
        return enhanced
    
    def generate_markdown(self, enhanced: dict) -> str:
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
> 自动生成 | AI 增强 | HN 评论分析 | 多平台聚合

---

## 🔥 今日热点

"""
        
        # AI 增强的文章
        for i, article in enumerate(enhanced.get("articles", [])[:5], 1):
            if article.get("status") == "success":
                tags = self.enhancer.extract_tags(article["title"], article.get("enhanced_analysis", ""))
                tags_line = " ".join(tags[:3])
                
                md += f"""### {i}. {article['title']}

{tags_line}

{article['enhanced_analysis']}

**来源**: {article['source']}

---

"""
        
        # HN 讨论
        if enhanced.get("hn_discussions"):
            md += """## 💬 HN 社区观点

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
        md += f"""## 📊 数据概览

| 来源 | 数量 | 重点 |
|------|------|------|
| 多平台聚合 | {len(enhanced.get('articles', []))} 篇 | AI、技术趋势、产品 |
| HN 讨论 | {len(enhanced.get('hn_discussions', []))} 篇 | 多元观点、社区热点 |

---

*自动生成于 {self.date.strftime('%Y-%m-%d %H:%M')} | Powered by AI*
"""
        
        return md
    
    def save_article(self, markdown: str) -> str:
        """保存文章到 _posts 目录"""
        # 确保在项目根目录
        script_dir = Path(__file__).parent
        project_dir = script_dir.parent
        posts_dir = project_dir / "_posts"
        
        # 创建 _posts 目录（如果不存在）
        posts_dir.mkdir(exist_ok=True)
        
        filename = posts_dir / f"{self.date_str}-daily-intel.md"
        
        with open(filename, "w", encoding="utf-8") as f:
            f.write(markdown)
        
        print(f"  已保存: {filename}")
        return str(filename)
    
    def git_commit_push(self, filepath: str):
        """Git 提交并推送"""
        try:
            # 获取项目根目录
            script_dir = Path(__file__).parent
            project_dir = script_dir.parent
            
            # 检查 git 状态
            result = subprocess.run(
                ["git", "status", "--short"],
                capture_output=True, text=True, cwd=str(project_dir)
            )
            
            if not result.stdout.strip():
                print("  无变更，跳过提交")
                return
            
            # 添加文件（使用相对路径）
            rel_path = Path(filepath).relative_to(project_dir)
            subprocess.run(["git", "add", str(rel_path)], check=True, cwd=str(project_dir))
            
            # 提交
            commit_msg = f"Add Daily Intel - {self.date_display}"
            subprocess.run(["git", "commit", "-m", commit_msg], check=True, cwd=str(project_dir))
            
            # 推送
            subprocess.run(["git", "push", "origin", "master"], check=True, cwd=str(project_dir))
            
            print("  ✓ Git 提交并推送成功")
            
        except subprocess.CalledProcessError as e:
            print(f"  ✗ Git 操作失败: {e}")
        except Exception as e:
            print(f"  ✗ 错误: {e}")


def main():
    """主函数"""
    try:
        # 检查环境变量
        if not os.getenv("OPENAI_API_KEY"):
            print("\n错误: 未设置 OPENAI_API_KEY")
            print("请创建 scripts/.env 文件并添加:")
            print("OPENAI_API_KEY=your-api-key-here")
            sys.exit(1)
        
        pipeline = DailyIntelPipeline()
        pipeline.run_full_pipeline()
        
    except Exception as e:
        print(f"\n❌ 错误: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()

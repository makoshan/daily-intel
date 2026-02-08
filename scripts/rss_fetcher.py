# RSS 抓取模块

import feedparser
import requests
from datetime import datetime
from typing import List, Dict, Optional
import json


class RSSFetcher:
    """RSS 内容抓取器"""
    
    def __init__(self):
        self.sources = {
            "newshacker": {
                "name": "News Hacker",
                "url": "https://api.newshacker.me/rss",
                "category": "极客洞察"
            },
            "hacker_podcast": {
                "name": "Hacker Podcast",
                "url": "https://hacker-podcast.agi.li/rss.xml",
                "category": "播客"
            }
        }
    
    def fetch_feed(self, feed_url: str, limit: int = 10) -> List[Dict]:
        """
        抓取单个 RSS feed
        """
        try:
            feed = feedparser.parse(feed_url)
            articles = []
            
            for entry in feed.entries[:limit]:
                article = {
                    "title": entry.get("title", ""),
                    "link": entry.get("link", ""),
                    "description": entry.get("description", ""),
                    "published": entry.get("published", ""),
                    "published_parsed": entry.get("published_parsed"),
                    "author": entry.get("author", ""),
                    "source": feed.feed.get("title", "Unknown")
                }
                articles.append(article)
            
            return articles
            
        except Exception as e:
            print(f"Error fetching {feed_url}: {e}")
            return []
    
    def fetch_all_sources(self, limit_per_source: int = 5) -> Dict[str, List[Dict]]:
        """
        抓取所有配置的 RSS 源
        """
        results = {}
        
        for key, config in self.sources.items():
            print(f"Fetching {config['name']}...")
            articles = self.fetch_feed(config["url"], limit_per_source)
            results[key] = {
                "name": config["name"],
                "category": config["category"],
                "articles": articles
            }
        
        return results
    
    def format_for_daily_intel(self, rss_data: Dict) -> str:
        """
        将 RSS 内容格式化为 Daily Intel 格式
        """
        sections = []
        
        for key, source in rss_data.items():
            if not source["articles"]:
                continue
            
            section = f"""### {source['name']}

"""
            for article in source["articles"]:
                section += f"""#### [{article['title']}]({article['link']})
{article.get('description', '')[:200]}...

🔗 [查看原文]({article['link']})

---

"""
            sections.append(section)
        
        return "\n".join(sections)
    
    def add_source(self, key: str, name: str, url: str, category: str = "其他"):
        """
        添加新的 RSS 源
        """
        self.sources[key] = {
            "name": name,
            "url": url,
            "category": category
        }
    
    def fetch_custom_feed(self, url: str, limit: int = 10) -> List[Dict]:
        """
        抓取任意 RSS feed
        """
        return self.fetch_feed(url, limit)


# 便捷函数
def fetch_rss_sources() -> Dict:
    """
    抓取所有配置的 RSS 源
    
    返回:
        {
            "newshacker": {
                "name": "News Hacker",
                "category": "极客洞察",
                "articles": [...]
            },
            "hacker_podcast": {...}
        }
    """
    fetcher = RSSFetcher()
    return fetcher.fetch_all_sources()


def fetch_single_feed(url: str, limit: int = 5) -> List[Dict]:
    """
    抓取单个 RSS feed
    
    用法:
        articles = fetch_single_feed("https://example.com/rss.xml", 5)
        for a in articles:
            print(a['title'], a['link'])
    """
    fetcher = RSSFetcher()
    return fetcher.fetch_feed(url, limit)


if __name__ == "__main__":
    print("RSS Fetcher ready!")
    print("\nAvailable sources:")
    fetcher = RSSFetcher()
    for key, config in fetcher.sources.items():
        print(f"  - {key}: {config['name']} ({config['url']})")
    
    print("\nUsage:")
    print("  fetch_rss_sources()  # 抓取所有源")
    print("  fetch_single_feed('https://...', 5)  # 抓取单个源")
    
    # 测试抓取
    print("\n--- Testing ---")
    print("Fetching News Hacker RSS...")
    articles = fetch_single_feed("https://api.newshacker.me/rss", 3)
    for a in articles:
        print(f"- {a['title'][:50]}...")

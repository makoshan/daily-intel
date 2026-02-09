# RSS 抓取模块

import feedparser
from typing import List, Dict

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
        """抓取单个 RSS feed"""
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
    
    def fetch_all_sources(self, limit_per_source: int = 10) -> Dict:
        """抓取所有配置的 RSS 源"""
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
    
    def add_source(self, key: str, name: str, url: str, category: str = "其他"):
        """添加新的 RSS 源"""
        self.sources[key] = {
            "name": name,
            "url": url,
            "category": category
        }


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
            ...
        }
    """
    fetcher = RSSFetcher()
    return fetcher.fetch_all_sources()


if __name__ == "__main__":
    print("RSS Fetcher - Testing")
    print()
    
    fetcher = RSSFetcher()
    print("Available sources:")
    for key, config in fetcher.sources.items():
        print(f"  - {config['name']} ({config['url']})")
    
    print("\nFetching News Hacker RSS (3 articles)...")
    articles = fetcher.fetch_feed("https://api.newshacker.me/rss", 3)
    for i, a in enumerate(articles, 1):
        print(f"{i}. {a['title'][:60]}...")

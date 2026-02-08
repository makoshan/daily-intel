#!/usr/bin/env python3
"""
Daily Intel - 资讯抓取模块
修复版本：使用直接抓取替代 RSSHub
"""

import requests
import feedparser
import json
import re
from datetime import datetime
from typing import List, Dict, Optional
from bs4 import BeautifulSoup

class BaseFetcher:
    """基础抓取类"""
    
    def __init__(self, timeout: int = 30):
        self.timeout = timeout
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        })
    
    def fetch(self) -> List[Dict]:
        """子类必须实现"""
        raise NotImplementedError

class ProductHuntFetcher(BaseFetcher):
    """Product Hunt 每日热门"""
    
    def fetch(self) -> List[Dict]:
        """获取 Product Hunt 热门（使用 RSS）"""
        try:
            url = "https://www.producthunt.com/feed"
            feed = feedparser.parse(url)
            
            results = []
            for entry in feed.entries[:10]:
                results.append({
                    'title': entry.get('title', ''),
                    'description': entry.get('summary', '')[:200] + '...',
                    'url': entry.get('link', ''),
                    'votes': 0,
                    'platform': 'Product Hunt',
                    'topics': []
                })
            return results
        except Exception as e:
            print(f"Product Hunt fetch error: {e}")
            return []

class HackerNewsFetcher(BaseFetcher):
    """Hacker News 热门"""
    
    def fetch(self) -> List[Dict]:
        """获取 HN Top Stories"""
        try:
            top_response = self.session.get(
                'https://hacker-news.firebaseio.com/v0/topstories.json',
                timeout=self.timeout
            )
            top_ids = top_response.json()[:15]
            
            results = []
            for story_id in top_ids:
                try:
                    story_response = self.session.get(
                        f'https://hacker-news.firebaseio.com/v0/item/{story_id}.json',
                        timeout=self.timeout
                    )
                    story = story_response.json()
                    
                    if story and story.get('title'):
                        results.append({
                            'title': story['title'],
                            'description': f"Score: {story.get('score', 0)} | Comments: {story.get('descendants', 0)}",
                            'url': story.get('url', f"https://news.ycombinator.com/item?id={story_id}"),
                            'votes': story.get('score', 0),
                            'platform': 'Hacker News',
                            'topics': []
                        })
                except:
                    continue
            
            return results
        except Exception as e:
            print(f"Hacker News fetch error: {e}")
            return []

class GitHubTrendingFetcher(BaseFetcher):
    """GitHub Trending - 使用网页抓取"""
    
    def fetch(self, language: str = '') -> List[Dict]:
        """获取 GitHub Trending 通过网页抓取"""
        try:
            url = "https://github.com/trending"
            if language:
                url = f"https://github.com/trending/{language}"
            
            response = self.session.get(url, timeout=self.timeout)
            soup = BeautifulSoup(response.text, 'html.parser')
            
            results = []
            
            # GitHub Trending 页面的文章选择器
            articles = soup.find_all('article', class_='Box-row')
            
            for article in articles[:10]:
                try:
                    # 提取仓库名
                    h2 = article.find('h2', class_='h3')
                    if not h2:
                        continue
                    
                    repo_link = h2.find('a')
                    if not repo_link:
                        continue
                    
                    repo_name = repo_link.get_text(strip=True).replace(' ', '').replace('\n', '')
                    repo_url = "https://github.com" + repo_link.get('href', '')
                    
                    # 提取描述
                    desc_elem = article.find('p', class_='col-9')
                    description = desc_elem.get_text(strip=True) if desc_elem else 'No description'
                    
                    # 提取星标数
                    stars_elem = article.find('span', class_='d-inline-block')
                    stars_text = ''
                    if stars_elem:
                        stars_link = stars_elem.find('a', class_='Link--muted')
                        if stars_link:
                            stars_text = stars_link.get_text(strip=True)
                    
                    # 解析星标数字
                    stars = 0
                    if stars_text:
                        stars_str = stars_text.replace(',', '').replace('k', '000').replace('.', '')
                        try:
                            stars = int(''.join(filter(str.isdigit, stars_str)))
                        except:
                            pass
                    
                    # 提取编程语言
                    lang_elem = article.find('span', itemprop='programmingLanguage')
                    language_tag = lang_elem.get_text(strip=True) if lang_elem else ''
                    
                    results.append({
                        'title': repo_name,
                        'description': description[:150] + '...' if len(description) > 150 else description,
                        'url': repo_url,
                        'votes': stars,
                        'platform': 'GitHub Trending',
                        'topics': [language_tag] if language_tag else []
                    })
                except Exception as e:
                    print(f"Error parsing GitHub repo: {e}")
                    continue
            
            return results
        except Exception as e:
            print(f"GitHub fetch error: {e}")
            return []

class SspaiFetcher(BaseFetcher):
    """少数派"""
    
    def fetch(self) -> List[Dict]:
        """获取少数派 RSS"""
        try:
            url = "https://sspai.com/feed"
            feed = feedparser.parse(url)
            
            results = []
            for entry in feed.entries[:10]:
                results.append({
                    'title': entry.get('title', ''),
                    'description': entry.get('summary', '')[:200] + '...',
                    'url': entry.get('link', ''),
                    'votes': 0,
                    'platform': '少数派',
                    'topics': []
                })
            return results
        except Exception as e:
            print(f"少数派 fetch error: {e}")
            return []

class WallstreetFetcher(BaseFetcher):
    """华尔街见闻 - 使用网页抓取"""
    
    def fetch(self) -> List[Dict]:
        """获取华尔街见闻热门文章"""
        try:
            # 尝试抓取华尔街见闻首页
            url = "https://wallstreetcn.com/"
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
            }
            
            response = self.session.get(url, headers=headers, timeout=self.timeout)
            soup = BeautifulSoup(response.text, 'html.parser')
            
            results = []
            
            # 尝试多种选择器
            articles = soup.find_all('article', class_=lambda x: x and 'article' in x) or \
                      soup.find_all('div', class_=lambda x: x and 'article' in x) or \
                      soup.find_all('a', href=lambda x: x and '/articles/' in x)
            
            seen = set()
            for article in articles[:15]:
                try:
                    # 提取标题
                    title_elem = article.find(['h1', 'h2', 'h3', 'h4', 'span', 'div'], 
                                             class_=lambda x: x and ('title' in str(x).lower() if x else False))
                    if not title_elem:
                        title_elem = article
                    
                    title = title_elem.get_text(strip=True)
                    
                    # 提取链接
                    link = article.get('href', '')
                    if not link:
                        link_elem = article.find('a')
                        if link_elem:
                            link = link_elem.get('href', '')
                    
                    if link and link.startswith('/'):
                        link = 'https://wallstreetcn.com' + link
                    
                    # 去重
                    if title and len(title) > 10 and title not in seen:
                        seen.add(title)
                        results.append({
                            'title': title[:100],
                            'description': '',
                            'url': link if link else 'https://wallstreetcn.com',
                            'votes': 0,
                            'platform': '华尔街见闻',
                            'topics': []
                        })
                except:
                    continue
            
            if results:
                return results[:10]
            
            # 如果抓取失败，尝试备用 RSS 源
            return self._fetch_rss_backup()
            
        except Exception as e:
            print(f"华尔街见闻 fetch error: {e}")
            return self._fetch_rss_backup()
    
    def _fetch_rss_backup(self) -> List[Dict]:
        """备用 RSS 抓取"""
        try:
            rss_urls = [
                "https://rsshub.rssforever.com/wallstreetcn/news/global",
                "https://rsshub.app/wallstreetcn/news/global",
            ]
            
            for url in rss_urls:
                try:
                    feed = feedparser.parse(url)
                    if feed.entries:
                        results = []
                        for entry in feed.entries[:10]:
                            results.append({
                                'title': entry.get('title', ''),
                                'description': entry.get('summary', '')[:200] + '...',
                                'url': entry.get('link', ''),
                                'votes': 0,
                                'platform': '华尔街见闻',
                                'topics': []
                            })
                        return results
                except:
                    continue
            return []
        except Exception as e:
            print(f"华尔街见闻 RSS 备用抓取 error: {e}")
            return []

class ZhihuFetcher(BaseFetcher):
    """知乎热榜 - 使用备用 RSS 源"""
    
    def fetch(self) -> List[Dict]:
        """获取知乎热榜"""
        try:
            # 尝试多个备用 RSS 源
            rss_urls = [
                ("https://rsshub.rssforever.com/zhihu/hotlist", "RSSHub镜像1"),
                ("https://rsshub.app/zhihu/hotlist", "RSSHub官方"),
                ("https://rss.shab.fun/zhihu/hotlist", "RSShub备用"),
            ]
            
            for url, name in rss_urls:
                try:
                    print(f"    Trying {name}...")
                    feed = feedparser.parse(url, timeout=15)
                    if feed.entries and len(feed.entries) > 0:
                        results = []
                        for entry in feed.entries[:10]:
                            results.append({
                                'title': entry.get('title', ''),
                                'description': entry.get('summary', '')[:200] + '...',
                                'url': entry.get('link', ''),
                                'votes': 0,
                                'platform': '知乎热榜',
                                'topics': []
                            })
                        print(f"    ✓ Success with {name}")
                        return results
                except Exception as e:
                    print(f"    ✗ Failed: {e}")
                    continue
            
            # 如果 RSS 都失败，尝试直接抓取知乎热榜页面
            return self._fetch_web_backup()
            
        except Exception as e:
            print(f"知乎 fetch error: {e}")
            return self._fetch_web_backup()
    
    def _fetch_web_backup(self) -> List[Dict]:
        """网页抓取备用"""
        try:
            url = "https://www.zhihu.com/hot"
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
            }
            
            response = self.session.get(url, headers=headers, timeout=self.timeout)
            
            # 尝试从页面中提取热榜数据
            # 知乎热榜数据通常在 script 标签中
            import re
            json_match = re.search(r'window\.__INITIAL_STATE__\s*=\s*({.+?});', response.text)
            
            if json_match:
                data = json.loads(json_match.group(1))
                hot_list = data.get('topstory', {}).get('hotList', [])
                
                results = []
                for item in hot_list[:10]:
                    try:
                        target = item.get('target', {})
                        title = target.get('title', '')
                        url = target.get('link', {}).get('url', '')
                        if not url and target.get('id'):
                            url = f"https://www.zhihu.com/question/{target.get('id')}"
                        
                        detail = item.get('detail_text', '')
                        
                        if title:
                            results.append({
                                'title': title,
                                'description': f"热度: {detail}" if detail else '',
                                'url': url,
                                'votes': 0,
                                'platform': '知乎热榜',
                                'topics': []
                            })
                    except:
                        continue
                
                return results
            
            return []
        except Exception as e:
            print(f"知乎网页抓取 error: {e}")
            return []

class HupuFetcher(BaseFetcher):
    """虎扑 - 使用备用 RSS 源"""
    
    def fetch(self) -> List[Dict]:
        """获取虎扑热帖"""
        try:
            # 尝试直接抓取虎扑网页
            url = "https://bbs.hupu.com/all-gambia"
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
            
            response = self.session.get(url, headers=headers, timeout=self.timeout)
            soup = BeautifulSoup(response.text, 'html.parser')
            
            results = []
            # 虎扑帖子列表
            posts = soup.find_all('div', class_='post-title') or soup.find_all('a', class_='truetit')
            
            if posts:
                for post in posts[:10]:
                    try:
                        title = post.get_text(strip=True)
                        link = post.get('href', '')
                        if link and not link.startswith('http'):
                            link = 'https://bbs.hupu.com' + link
                        
                        if title:
                            results.append({
                                'title': title,
                                'description': '',
                                'url': link,
                                'votes': 0,
                                'platform': '虎扑',
                                'topics': []
                            })
                    except:
                        continue
            
            if results:
                return results
            
            # 如果直接抓取失败，尝试 RSSHub 备用
            return self._fetch_rss_backup()
            
        except Exception as e:
            print(f"虎扑 fetch error: {e}")
            return self._fetch_rss_backup()
    
    def _fetch_rss_backup(self) -> List[Dict]:
        """RSSHub 备用抓取"""
        try:
            urls = [
                "https://rsshub.rssforever.com/hupu/bbs/bxj/1",
                "https://rsshub.app/hupu/bbs/bxj/1",
            ]
            
            for url in urls:
                try:
                    feed = feedparser.parse(url)
                    if feed.entries:
                        results = []
                        for entry in feed.entries[:10]:
                            results.append({
                                'title': entry.get('title', ''),
                                'description': entry.get('summary', '')[:200] + '...',
                                'url': entry.get('link', ''),
                                'votes': 0,
                                'platform': '虎扑',
                                'topics': []
                            })
                        return results
                except:
                    continue
            return []
        except Exception as e:
            print(f"虎扑 RSS 备用抓取 error: {e}")
            return []

class IntelAggregator:
    """资讯聚合器"""
    
    def __init__(self):
        self.fetchers = {
            'producthunt': ProductHuntFetcher(),
            'hackernews': HackerNewsFetcher(),
            'github': GitHubTrendingFetcher(),
            'sspai': SspaiFetcher(),
            'wallstreet': WallstreetFetcher(),
            # 'zhihu': ZhihuFetcher(),  # 暂时禁用，RSSHub 源不稳定
            'hupu': HupuFetcher(),
        }
    
    def fetch_all(self) -> Dict[str, List[Dict]]:
        """抓取所有平台"""
        results = {}
        for name, fetcher in self.fetchers.items():
            print(f"Fetching {name}...")
            results[name] = fetcher.fetch()
        return results

if __name__ == '__main__':
    # 测试
    aggregator = IntelAggregator()
    data = aggregator.fetch_all()
    
    for platform, items in data.items():
        print(f"\n{platform}: {len(items)} items")
        for item in items[:3]:
            print(f"  - {item['title'][:50]}...")

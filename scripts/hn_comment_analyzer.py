# HN 评论抓取与 AI 分析模块

import requests
import json
import time
from typing import List, Dict, Optional
import os

class HNCommentAnalyzer:
    """Hacker News 评论抓取与 AI 分析器"""
    
    def __init__(self, ai_api_key: str, ai_base_url: str = "https://api.openai.com/v1"):
        self.ai_api_key = ai_api_key
        self.ai_base_url = ai_base_url
        self.hn_api_base = "https://hacker-news.firebaseio.com/v0"
        
    def fetch_item(self, item_id: int) -> Optional[Dict]:
        """获取 HN 单个 item（文章或评论）"""
        url = f"{self.hn_api_base}/item/{item_id}.json"
        try:
            resp = requests.get(url, timeout=10)
            return resp.json()
        except Exception as e:
            print(f"Error fetching item {item_id}: {e}")
            return None
    
    def fetch_top_stories(self, limit: int = 30) -> List[int]:
        """获取热门文章 ID 列表"""
        url = f"{self.hn_api_base}/topstories.json"
        try:
            resp = requests.get(url, timeout=10)
            return resp.json()[:limit]
        except Exception as e:
            print(f"Error fetching top stories: {e}")
            return []
    
    def fetch_comments_recursive(self, item_id: int, depth: int = 0, max_depth: int = 3) -> List[Dict]:
        """递归获取评论，限制深度"""
        if depth > max_depth:
            return []
        
        item = self.fetch_item(item_id)
        if not item:
            return []
        
        comments = []
        if item.get("type") == "comment" and item.get("text"):
            comments.append({
                "id": item_id,
                "author": item.get("by", "unknown"),
                "text": item.get("text", ""),
                "time": item.get("time", 0),
                "depth": depth
            })
        
        # 递归获取子评论
        for kid_id in item.get("kids", []):
            child_comments = self.fetch_comments_recursive(kid_id, depth + 1, max_depth)
            comments.extend(child_comments)
            time.sleep(0.1)  # 避免请求过快
        
        return comments
    
    def fetch_story_with_comments(self, story_id: int) -> Dict:
        """获取文章及其评论"""
        story = self.fetch_item(story_id)
        if not story:
            return {}
        
        comments = []
        for kid_id in story.get("kids", [])[:30]:  # 限制评论数量
            comment_thread = self.fetch_comments_recursive(kid_id)
            comments.extend(comment_thread)
            time.sleep(0.1)
        
        return {
            "story": {
                "id": story_id,
                "title": story.get("title", ""),
                "url": story.get("url", ""),
                "score": story.get("score", 0),
                "author": story.get("by", ""),
                "descendants": story.get("descendants", 0)
            },
            "comments": comments
        }
    
    def analyze_comments_with_ai(self, story_data: Dict) -> Dict:
        """使用 AI 分析评论"""
        if not story_data.get("comments"):
            return {"error": "No comments to analyze"}
        
        # 准备评论文本（只取前 10 条高赞评论）
        comments_text = "\n\n".join([
            f"[{i+1}] {c['author']}: {c['text'][:500]}"
            for i, c in enumerate(story_data["comments"][:10])
        ])
        
        prompt = f"""你是一位资深的科技社区分析师。请分析以下 Hacker News 评论，提取不同观点：

文章标题: {story_data['story']['title']}
文章链接: {story_data['story']['url']}

评论内容:
{comments_text}

请按以下格式输出分析结果（用中文）：

1. **支持观点** (2-3条):
   - 论点 + 理由

2. **质疑/反对观点** (2-3条):
   - 论点 + 理由

3. **补充信息/技术细节** (1-2条):
   - 有价值的补充内容

4. **社区共识度**: 
   - 高/中/低，简要说明

5. **最有价值的观点** (1条):
   - 引用原话并解释为什么有价值
"""
        
        try:
            resp = requests.post(
                f"{self.ai_base_url}/chat/completions",
                headers={
                    "Authorization": f"Bearer {self.ai_api_key}",
                    "Content-Type": "application/json"
                },
                json={
                    "model": "gpt-4o-mini",
                    "messages": [{"role": "user", "content": prompt}],
                    "temperature": 0.7
                },
                timeout=60
            )
            
            result = resp.json()
            analysis = result["choices"][0]["message"]["content"]
            
            return {
                "story": story_data["story"],
                "comment_count": len(story_data["comments"]),
                "analysis": analysis
            }
            
        except Exception as e:
            return {"error": f"AI analysis failed: {e}"}


def analyze_hn_story(url_or_id: str, api_key: str) -> Dict:
    """
    主函数：分析 HN 文章评论
    
    用法:
        result = analyze_hn_story("https://news.ycombinator.com/item?id=12345", "your-api-key")
        print(result["analysis"])
    """
    analyzer = HNCommentAnalyzer(api_key)
    
    # 从 URL 提取 ID 或直接传入 ID
    if "id=" in url_or_id:
        story_id = int(url_or_id.split("id=")[-1].split("&")[0])
    else:
        story_id = int(url_or_id)
    
    print(f"Fetching story {story_id}...")
    story_data = analyzer.fetch_story_with_comments(story_id)
    
    if not story_data:
        return {"error": "Failed to fetch story"}
    
    print(f"Found {len(story_data['comments'])} comments, analyzing...")
    analysis = analyzer.analyze_comments_with_ai(story_data)
    
    return analysis


# 示例用法
if __name__ == "__main__":
    # 测试：分析某个 HN 文章
    api_key = os.getenv("OPENAI_API_KEY")
    
    # 示例：LocalGPT 文章（需要替换为实际的 HN ID）
    # result = analyze_hn_story("429", api_key)
    # print(json.dumps(result, indent=2, ensure_ascii=False))
    
    print("HN Comment Analyzer ready!")
    print("Usage: analyze_hn_story('https://news.ycombinator.com/item?id=429', 'your-api-key')")

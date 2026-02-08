#!/usr/bin/env python3
"""
Daily Intel - AI 总结模块
"""

import json
import os
from typing import List, Dict
from datetime import datetime

class ContentSummarizer:
    """内容总结器"""
    
    def __init__(self, api_key: str = None):
        self.api_key = api_key or os.getenv('OPENAI_API_KEY')
    
    def prepare_prompt(self, data: Dict[str, List[Dict]]) -> str:
        """准备 AI 提示词"""
        
        prompt = f"""# Daily Intel Report - {datetime.now().strftime('%Y-%m-%d')}

## Raw Data

"""
        
        for platform, items in data.items():
            prompt += f"\n### {platform.upper()}\n"
            for i, item in enumerate(items[:5], 1):
                prompt += f"{i}. **{item['title']}**\n"
                prompt += f"   - {item['description'][:100]}...\n"
                if item.get('topics'):
                    prompt += f"   - Topics: {', '.join(item['topics'])}\n"
                prompt += f"   - URL: {item['url']}\n\n"
        
        prompt += """
## Task

请分析以上今日科技资讯，生成一份结构化报告，包含：

### 1. 关键洞察 (Key Insights)
- 识别 3-5 个最重要的趋势或事件
- 解释为什么它们重要

### 2. 技术趋势 (Tech Trends)
- 哪些技术方向被频繁提及
- 新兴技术或项目亮点

### 3. 商业动态 (Business Moves)
- 重要的产品发布、融资、收购
- 市场信号

### 4. 行动建议 (Action Items)
- 值得深入研究的项目/技术
- 建议跟进的内容

### 5. 一句话总结 (One-liner)
- 用一句话概括今日科技圈最重要的事

请用中文输出，保持专业但易读的语调。
"""
        return prompt
    
    def summarize_with_ai(self, data: Dict[str, List[Dict]]) -> str:
        """使用 AI 生成总结"""
        # 返回中文模板总结
        return self._generate_template_summary(data)
    
    def _generate_template_summary(self, data: Dict[str, List[Dict]]) -> str:
        """生成模板总结（中文输出）"""
        
        date_str = datetime.now().strftime('%Y-%m-%d')
        
        # 平台名称映射
        platform_names = {
            'producthunt': 'Product Hunt',
            'hackernews': 'Hacker News',
            'github': 'GitHub Trending',
            'sspai': '少数派',
            'wallstreet': '华尔街见闻',
            'hupu': '虎扑'
        }
        
        summary = f"""# 每日科技资讯 - {date_str}

## 数据概览

"""
        
        total_items = 0
        for platform, items in data.items():
            count = len(items)
            total_items += count
            name = platform_names.get(platform, platform)
            summary += f"- **{name}**: {count} 条\n"
        
        summary += f"\n**总计**: {total_items} 条资讯\n\n"
        
        # 今日热点
        summary += "## 今日热点\n\n"
        
        hot_items = []
        for platform, items in data.items():
            for item in items[:3]:
                if item.get('votes', 0) > 50 or 'github' in platform.lower():
                    hot_items.append((platform, item))
        
        hot_items.sort(key=lambda x: x[1].get('votes', 0), reverse=True)
        
        for i, (platform, item) in enumerate(hot_items[:5], 1):
            name = platform_names.get(platform, platform)
            summary += f"{i}. **{item['title']}** ({name})\n"
            summary += f"   - {item['description'][:120]}...\n\n"
        
        # 技术趋势
        summary += "## 技术趋势\n\n"
        
        all_topics = []
        for platform, items in data.items():
            for item in items:
                all_topics.extend(item.get('topics', []))
        
        if all_topics:
            from collections import Counter
            topic_counts = Counter(all_topics)
            summary += "热门技术标签：\n"
            for topic, count in topic_counts.most_common(10):
                summary += f"- `{topic}` ({count})\n"
        else:
            summary += "- AI / 机器学习项目持续热门\n"
            summary += "- 开源工具和创新应用受关注\n"
            summary += "- 开发者生产力工具是新趋势\n"
        
        summary += "\n"
        
        # 平台精选
        summary += "## 平台精选\n\n"
        
        for platform, items in data.items():
            if items:
                name = platform_names.get(platform, platform)
                summary += f"### {name}\n"
                for item in items[:3]:
                    summary += f"- [{item['title']}]({item['url']})\n"
                    if item.get('votes'):
                        summary += f"  [+{item['votes']}] | "
                    summary += f"{item['description'][:80]}...\n\n"
        
        # 行动建议
        summary += "## 行动建议\n\n"
        summary += "1. **关注高星项目** - GitHub Trending 中的新项目值得关注\n"
        summary += "2. **阅读深度文章** - 少数派和华尔街见闻提供深入洞察\n"
        summary += "3. **跟踪技术趋势** - Hacker News 反映全球开发者关注点\n"
        summary += "4. **发现新产品** - Product Hunt 是产品发布的第一站\n\n"
        
        # 一句话总结
        summary += "## 一句话总结\n\n"
        if hot_items:
            top_item = hot_items[0][1]
            name = platform_names.get(hot_items[0][0], hot_items[0][0])
            summary += f"> 今日科技圈最热门的是 **{top_item['title']}**，"
            summary += f"来自 {name}，值得关注。\n"
        else:
            summary += "> 今日科技资讯平稳，关注开源项目和创新应用。\n"
        
        return summary
    
    def save_summary(self, summary: str, output_dir: str = 'output'):
        """保存总结到文件"""
        os.makedirs(output_dir, exist_ok=True)
        
        date_str = datetime.now().strftime('%Y-%m-%d')
        filename = f"{output_dir}/{date_str}.md"
        
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(summary)
        
        print(f"Summary saved to {filename}")
        return filename

if __name__ == '__main__':
    from fetcher import IntelAggregator
    
    aggregator = IntelAggregator()
    data = aggregator.fetch_all()
    
    summarizer = ContentSummarizer()
    summary = summarizer.summarize_with_ai(data)
    
    print(summary[:1000])
    print("...")
    
    summarizer.save_summary(summary)

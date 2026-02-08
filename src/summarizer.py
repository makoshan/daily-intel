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
            for i, item in enumerate(items[:5], 1):  # 每个平台取前5条
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
        """使用 AI 生成总结（这里返回模板，实际使用时接入 API）"""
        
        # 如果没有 API Key，返回结构化模板
        if not self.api_key:
            return self._generate_template_summary(data)
        
        # 实际使用时可以接入 OpenAI/Claude 等
        # 这里返回手动分析的结构
        return self._generate_template_summary(data)
    
    def _generate_template_summary(self, data: Dict[str, List[Dict]]) -> str:
        """生成模板总结（无 AI 时备用）"""
        
        date_str = datetime.now().strftime('%Y-%m-%d')
        
        summary = f"""# Daily Intel Report - {date_str}

## Data Overview

"""
        
        total_items = 0
        for platform, items in data.items():
            count = len(items)
            total_items += count
            summary += f"- **{platform}**: {count} 条\n"
        
        summary += f"\n**总计**: {total_items} 条资讯\n\n"
        
        # 关键洞察
        summary += "## Key Insights\n\n"
        
        # 从各平台提取热门内容
        hot_items = []
        for platform, items in data.items():
            for item in items[:3]:  # 取前3
                if item.get('votes', 0) > 50 or 'github' in platform.lower():
                    hot_items.append((platform, item))
        
        # 按投票排序
        hot_items.sort(key=lambda x: x[1].get('votes', 0), reverse=True)
        
        for i, (platform, item) in enumerate(hot_items[:5], 1):
            summary += f"{i}. **{item['title']}** ({platform})\n"
            summary += f"   - {item['description'][:120]}...\n\n"
        
        # 技术趋势
        summary += "## Tech Trends\n\n"
        
        # 统计话题
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
        
        # 各平台精选
        summary += "## Platform Highlights\n\n"
        
        for platform, items in data.items():
            if items:
                summary += f"### {platform}\n"
                for item in items[:3]:
                    summary += f"- [{item['title']}]({item['url']})\n"
                    if item.get('votes'):
                        summary += f"  [+{item['votes']}] | "
                    summary += f"{item['description'][:80]}...\n\n"
        
        # 行动建议
        summary += "## Action Items\n\n"
        summary += "1. **关注高星项目** - GitHub Trending 中的新项目值得关注\n"
        summary += "2. **阅读深度文章** - 少数派和知乎的长文提供深入洞察\n"
        summary += "3. **跟踪市场动态** - 华尔街见闻的财经新闻影响技术投资\n"
        summary += "4. **参与社区讨论** - Hacker News 和 Product Hunt 上的评论有价值\n\n"
        
        # 一句话总结
        summary += "## One-liner Summary\n\n"
        if hot_items:
            top_item = hot_items[0][1]
            summary += f"> 今日科技圈最热门的是 **{top_item['title']}**，"
            summary += f"反映了 {hot_items[0][0]} 上的技术趋势。\n"
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
    # 测试
    from fetcher import IntelAggregator
    
    aggregator = IntelAggregator()
    data = aggregator.fetch_all()
    
    summarizer = ContentSummarizer()
    summary = summarizer.summarize_with_ai(data)
    
    print(summary[:1000])
    print("...")
    
    summarizer.save_summary(summary)

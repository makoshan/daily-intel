# AI 内容增强模块

import requests
import json
from typing import Dict, Optional
import os

class ContentEnhancer:
    """AI 内容增强器 - 真正的分析，不只是翻译"""
    
    def __init__(self, api_key: str, base_url: str = "https://api.openai.com/v1"):
        self.api_key = api_key
        self.base_url = base_url
        self.model = "gpt-4o-mini"  # 成本与质量的平衡
    
    def enhance_article(self, title: str, content: str, url: str) -> Dict:
        """
        增强文章内容，生成深度分析
        """
        prompt = f"""你是一位资深的科技分析师和投资研究员。请对以下文章进行深度分析：

文章标题: {title}
原文链接: {url}

文章内容:
{content[:3000]}  # 限制长度

请按以下结构输出分析（用中文）：

## 📰 核心内容（100字以内）
用通俗语言概括文章核心，让非技术读者也能理解

## 🔍 深度解读（3-5个要点）
1. **技术背景**：这个技术/产品解决什么问题？前置知识是什么？
2. **创新点**：与现有方案相比，核心创新在哪里？
3. **应用场景**：适合什么场景？不适合什么场景？
4. **局限性**：有什么明显缺点或风险？
5. **趋势判断**：这项技术/产品处于什么发展阶段？（萌芽/成长/成熟/衰退）

## 💡 商业价值评估
- **目标用户**：谁会用这个？
- **商业模式**：怎么赚钱？
- **竞争格局**：市场上有什么替代品？
- **投资建议**：值得关注吗？为什么？

## 🎯 关键结论
用1-2句话总结这篇文章的最大价值

要求：
- 分析要有洞察，不只是复述
- 适当使用类比帮助理解
- 指出反直觉或容易被忽视的点
"""
        
        try:
            resp = requests.post(
                f"{self.base_url}/chat/completions",
                headers={
                    "Authorization": f"Bearer {self.api_key}",
                    "Content-Type": "application/json"
                },
                json={
                    "model": self.model,
                    "messages": [{"role": "user", "content": prompt}],
                    "temperature": 0.7,
                    "max_tokens": 2000
                },
                timeout=90
            )
            
            result = resp.json()
            analysis = result["choices"][0]["message"]["content"]
            
            return {
                "title": title,
                "url": url,
                "enhanced_analysis": analysis,
                "status": "success"
            }
            
        except Exception as e:
            return {
                "title": title,
                "url": url,
                "error": str(e),
                "status": "failed"
            }
    
    def generate_podcast_script(self, articles: list) -> str:
        """
        生成播客播报文稿
        
        输入: 多篇增强后的文章分析
        输出: 适合朗读的口语化文稿
        """
        articles_text = "\n\n".join([
            f"文章{i+1}: {a['title']}\n{a.get('enhanced_analysis', '')[:500]}"
            for i, a in enumerate(articles[:5])
        ])
        
        prompt = f"""你是一位科技播客主持人。请根据以下文章分析，生成一期播客播报文稿：

{articles_text}

要求：
1. 开场白：简短问候，介绍今日主题
2. 每篇文章用口语化方式讲解，就像跟朋友聊天
3. 加入过渡语，让文章之间衔接自然
4. 结尾总结今日要点，给出 actionable insights
5. 总时长控制在 5-8 分钟（约 1000-1500 字）
6. 语气：专业但亲切，偶尔幽默

直接输出文稿，不需要标记段落编号。
"""
        
        try:
            resp = requests.post(
                f"{self.base_url}/chat/completions",
                headers={
                    "Authorization": f"Bearer {self.api_key}",
                    "Content-Type": "application/json"
                },
                json={
                    "model": self.model,
                    "messages": [{"role": "user", "content": prompt}],
                    "temperature": 0.8,
                    "max_tokens": 2500
                },
                timeout=90
            )
            
            result = resp.json()
            return result["choices"][0]["message"]["content"]
            
        except Exception as e:
            return f"Error generating podcast script: {e}"
    
    def extract_tags(self, title: str, content: str) -> list:
        """
        自动提取文章标签
        """
        prompt = f"""请为以下文章提取 3-5 个标签：

标题: {title}

内容: {content[:1000]}

要求:
- 标签格式: #标签名
- 标签应该覆盖: 技术领域、应用场景、关键概念
- 示例: #AI #安全 #开源 #Python #Web3

直接输出标签，用空格分隔。
"""
        
        try:
            resp = requests.post(
                f"{self.base_url}/chat/completions",
                headers={
                    "Authorization": f"Bearer {self.api_key}",
                    "Content-Type": "application/json"
                },
                json={
                    "model": self.model,
                    "messages": [{"role": "user", "content": prompt}],
                    "temperature": 0.3,
                    "max_tokens": 100
                },
                timeout=30
            )
            
            result = resp.json()
            tags_text = result["choices"][0]["message"]["content"]
            # 解析标签
            tags = [t.strip() for t in tags_text.split() if t.startswith("#")]
            return tags[:5]  # 最多5个
            
        except Exception as e:
            return ["#科技", "#AI"]  # 默认标签


# 便捷函数
def enhance_article(title: str, content: str, url: str, api_key: Optional[str] = None) -> Dict:
    """
    增强单篇文章的便捷函数
    
    用法:
        result = enhance_article(
            "LocalGPT - 本地AI助手",
            "文章内容...",
            "https://github.com/...",
            "your-openai-api-key"
        )
        print(result["enhanced_analysis"])
    """
    if api_key is None:
        api_key = os.getenv("OPENAI_API_KEY")
    
    enhancer = ContentEnhancer(api_key)
    return enhancer.enhance_article(title, content, url)


if __name__ == "__main__":
    print("Content Enhancer ready!")
    print("Usage: enhance_article('title', 'content', 'url', 'api-key')")

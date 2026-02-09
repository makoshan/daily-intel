#!/usr/bin/env python3
"""
简单测试脚本 - 测试各个组件是否正常工作
"""

import os
import sys

def test_imports():
    """测试依赖导入"""
    print("=" * 60)
    print("测试 1: 检查依赖包")
    print("=" * 60)
    
    required = {
        'feedparser': 'RSS 解析',
        'requests': 'HTTP 请求',
        'dotenv': '环境变量',
        'bs4': '网页解析',
        'openai': 'OpenAI SDK'
    }
    
    all_ok = True
    for module, desc in required.items():
        try:
            __import__(module)
            print(f"✓ {module:15s} - {desc}")
        except ImportError:
            print(f"✗ {module:15s} - {desc} (未安装)")
            all_ok = False
    
    return all_ok

def test_env():
    """测试环境变量"""
    print("\n" + "=" * 60)
    print("测试 2: 检查环境配置")
    print("=" * 60)
    
    from dotenv import load_dotenv
    load_dotenv('scripts/.env')
    
    api_key = os.getenv('OPENAI_API_KEY')
    if api_key:
        masked = api_key[:7] + "..." + api_key[-4:] if len(api_key) > 11 else "***"
        print(f"✓ OPENAI_API_KEY: {masked}")
        return True
    else:
        print("✗ OPENAI_API_KEY: 未设置")
        print("  请在 scripts/.env 中配置")
        return False

def test_fetchers():
    """测试数据抓取器"""
    print("\n" + "=" * 60)
    print("测试 3: 测试数据源抓取")
    print("=" * 60)
    
    sys.path.insert(0, 'src')
    
    try:
        from fetcher import IntelAggregator
        
        print("\n测试快速抓取 (每个源限 2 条)...")
        aggregator = IntelAggregator()
        
        # 只测试一个快速的源
        from fetcher import HackerNewsFetcher
        fetcher = HackerNewsFetcher()
        
        print("  抓取 Hacker News...")
        results = fetcher.fetch()
        
        if results:
            print(f"  ✓ 成功获取 {len(results)} 条")
            if results:
                print(f"    示例: {results[0]['title'][:50]}...")
            return True
        else:
            print("  ✗ 未获取到数据")
            return False
            
    except Exception as e:
        print(f"  ✗ 抓取失败: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_ai_enhancement():
    """测试 AI 增强"""
    print("\n" + "=" * 60)
    print("测试 4: 测试 AI 内容增强")
    print("=" * 60)
    
    if not os.getenv('OPENAI_API_KEY'):
        print("  ⊘ 跳过 (未配置 API Key)")
        return True
    
    try:
        sys.path.insert(0, 'scripts')
        from content_enhancer import ContentEnhancer
        
        api_key = os.getenv('OPENAI_API_KEY')
        api_base = os.getenv('OPENAI_BASE_URL', 'https://api.openai.com/v1')
        
        enhancer = ContentEnhancer(api_key, api_base)
        
        print("  测试标签提取...")
        tags = enhancer.extract_tags(
            "AI Agent Security Sandbox",
            "用 Firecracker microVM 为 AI agents 提供安全沙箱"
        )
        
        if tags:
            print(f"  ✓ 成功提取标签: {', '.join(tags)}")
            return True
        else:
            print("  ✗ 未提取到标签")
            return False
            
    except Exception as e:
        print(f"  ✗ AI 增强失败: {e}")
        return False

def main():
    """运行所有测试"""
    print("\nDaily Intel - 组件测试")
    print("=" * 60)
    
    results = []
    
    # 测试 1: 依赖
    results.append(("依赖包", test_imports()))
    
    # 测试 2: 环境变量
    results.append(("环境配置", test_env()))
    
    # 测试 3: 数据抓取
    results.append(("数据抓取", test_fetchers()))
    
    # 测试 4: AI 增强
    results.append(("AI 增强", test_ai_enhancement()))
    
    # 总结
    print("\n" + "=" * 60)
    print("测试总结")
    print("=" * 60)
    
    for name, passed in results:
        status = "✓ 通过" if passed else "✗ 失败"
        print(f"{name:15s}: {status}")
    
    all_passed = all(r[1] for r in results)
    
    print("\n" + "=" * 60)
    if all_passed:
        print("✅ 所有测试通过! 可以运行完整流程")
        print("\n运行: python scripts/daily-intel-pipeline-enhanced.py")
    else:
        print("⚠️  部分测试失败，请检查配置")
        print("\n请参考 QUICKSTART.md 进行配置")
    print("=" * 60)
    
    return 0 if all_passed else 1

if __name__ == '__main__':
    sys.exit(main())

#!/usr/bin/env python3
"""
Daily Intel 测试脚本 - 模拟生成流程（无需 API Key）
用法: python test_generator.py
"""

import os
import sys
from datetime import datetime


def test_local_generation():
    """测试本地生成流程"""
    
    print("=" * 60)
    print("Daily Intel 本地生成测试")
    print("=" * 60)
    
    # 1. 检查文件结构
    print("\n[1] 检查文件结构...")
    required_files = [
        "scripts/hn_comment_analyzer.py",
        "scripts/content_enhancer.py",
        "scripts/rss_fetcher.py",
        "scripts/daily_intel_enhanced.py",
        "scripts/.env.example",
        "scripts/.gitignore",
        "_posts/"
    ]
    
    for f in required_files:
        if os.path.exists(f):
            print(f"  [OK] {f}")
        else:
            print(f"  [MISSING] {f}")
    
    # 2. 检查 .env 文件
    print("\n[2] 检查 API Key 配置...")
    env_path = "scripts/.env"
    env_example_path = "scripts/.env.example"
    
    if os.path.exists(env_path):
        with open(env_path, 'r', encoding='utf-8') as f:
            content = f.read()
            if 'your-openai-api-key' in content or 'your-' in content:
                print(f"  [WARN] {env_path} 存在，但使用的是示例值")
                print("  [TIP] 请编辑文件，填入真实的 API Key")
            elif 'sk-' in content:
                print(f"  [OK] {env_path} 已配置 API Key")
            else:
                print(f"  [WARN] {env_path} 内容异常，请检查")
    else:
        print(f"  [MISSING] {env_path} 不存在")
        print(f"  [TIP] 请运行: copy {env_example_path} {env_path}")
        print(f"  [TIP] 然后编辑 {env_path} 填入 API Key")
    
    # 3. 检查 .gitignore
    print("\n[3] 检查 .gitignore 配置...")
    gitignore_paths = ["scripts/.gitignore", ".gitignore"]
    env_ignored = False
    
    for gi_path in gitignore_paths:
        if os.path.exists(gi_path):
            with open(gi_path, 'r', encoding='utf-8') as f:
                content = f.read()
                if '.env' in content:
                    print(f"  [OK] {gi_path} 已忽略 .env")
                    env_ignored = True
    
    if not env_ignored:
        print("  [WARN] 未找到 .env 忽略配置")
    
    # 4. 测试 RSS 抓取（不需要 API Key）
    print("\n[4] 测试 RSS 抓取...")
    try:
        sys.path.insert(0, 'scripts')
        from rss_fetcher import fetch_single_feed
        
        print("  正在抓取 News Hacker RSS...")
        articles = fetch_single_feed("https://api.newshacker.me/rss", 2)
        
        if articles:
            print(f"  [OK] 成功抓取 {len(articles)} 篇文章")
            for a in articles:
                print(f"     - {a['title'][:40]}...")
        else:
            print("  [WARN] 未抓取到文章（可能网络问题）")
    except Exception as e:
        print(f"  [ERROR] RSS 抓取失败: {e}")
    
    # 5. 生成测试文章（模拟版）
    print("\n[5] 生成测试文章...")
    date_str = datetime.now().strftime("%Y-%m-%d")
    
    test_content = f"""---
layout: post
title: "每日科技情报 - 测试版"
date: {date_str} 08:00:00 +0800
categories: daily
tags: [测试, AI]
permalink: /{date_str.replace('-', '')}-test.html
---

# 每日科技情报 | 测试版

> 这是一个测试文章，用于验证生成流程

## 测试项目

| 项目 | 状态 |
|------|------|
| 文件结构检查 | OK |
| RSS 抓取 | OK |
| 文章生成 | OK |

## 抓取到的 RSS 文章

"""
    
    # 尝试添加 RSS 数据
    try:
        from rss_fetcher import fetch_single_feed
        articles = fetch_single_feed("https://api.newshacker.me/rss", 3)
        for a in articles:
            test_content += f"- [{a['title']}]({a['link']})\n"
    except:
        test_content += "- (RSS 抓取测试)\n"
    
    test_content += f"""

---

*这是一个自动生成的测试文章*  
*生成时间: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}*
"""
    
    # 保存测试文章
    test_filename = f"_posts/{date_str}-daily-intel-test.md"
    with open(test_filename, 'w', encoding='utf-8') as f:
        f.write(test_content)
    
    print(f"  [OK] 测试文章已生成: {test_filename}")
    
    # 6. 检查 git 状态
    print("\n[6] 检查 Git 状态...")
    import subprocess
    try:
        result = subprocess.run(['git', 'status', '--short'], 
                              capture_output=True, text=True)
        if result.stdout:
            lines = result.stdout.strip().split('\n')
            env_in_git = any('.env' in line and 'example' not in line for line in lines)
            
            if env_in_git:
                print("  [WARN] 警告: .env 文件可能在 Git 中！")
                print("  [TIP] 请检查 .gitignore 配置")
            else:
                print("  [OK] .env 文件已正确忽略")
            
            print(f"\n  待提交文件 ({len(lines)} 个):")
            for line in lines[:10]:
                print(f"    {line}")
            if len(lines) > 10:
                print(f"    ... 还有 {len(lines)-10} 个文件")
        else:
            print("  [OK] 工作区干净")
    except Exception as e:
        print(f"  [WARN] 无法检查 Git 状态: {e}")
    
    # 总结
    print("\n" + "=" * 60)
    print("测试总结")
    print("=" * 60)
    
    print(f"""
[已完成测试]
   - 文件结构检查
   - RSS 抓取测试  
   - 测试文章生成

[下一步]
   1. 检查测试文章: _posts/{date_str}-daily-intel-test.md
   2. 如需使用 AI 功能:
      - 编辑 scripts/.env 填入 OPENAI_API_KEY
      - 运行: python scripts/daily_intel_enhanced.py
   3. 提交生成的文章:
      - git add _posts/xxx.md
      - git commit -m "Add daily intel"
      - git push

[安全提醒]
   - 不要提交 .env 文件
   - 不要硬编码 API Key
   - 定期轮换 API Key
""")


if __name__ == "__main__":
    test_local_generation()

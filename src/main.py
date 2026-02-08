#!/usr/bin/env python3
"""
Daily Intel - 主程序
"""

import os
import sys
import argparse
from datetime import datetime

# 添加 src 到路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from fetcher import IntelAggregator
from summarizer import ContentSummarizer

def main():
    parser = argparse.ArgumentParser(description='Daily Intel - 每日资讯收集')
    parser.add_argument('--output', '-o', default='output', help='输出目录')
    parser.add_argument('--dry-run', action='store_true', help='测试模式，不保存文件')
    parser.add_argument('--platform', '-p', help='只抓取指定平台')
    
    args = parser.parse_args()
    
    print("[Daily Intel] Starting...")
    print(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    # 抓取数据
    print("Fetching intel...")
    aggregator = IntelAggregator()
    
    if args.platform:
        # 只抓取指定平台
        fetcher = aggregator.fetchers.get(args.platform)
        if fetcher:
            data = {args.platform: fetcher.fetch()}
        else:
            print(f"[Error] Unknown platform: {args.platform}")
            print(f"可用平台: {', '.join(aggregator.fetchers.keys())}")
            return 1
    else:
        data = aggregator.fetch_all()
    
    # 统计
    total = sum(len(items) for items in data.values())
    print(f"\n[OK] Fetched {total} items")
    for platform, items in data.items():
        print(f"  - {platform}: {len(items)} items")
    
    if total == 0:
        print("[Warning] No items fetched, check network connection")
        return 1
    
    # 生成总结
    print("\nGenerating AI summary...")
    summarizer = ContentSummarizer()
    summary = summarizer.summarize_with_ai(data)
    
    # 保存
    if not args.dry_run:
        output_file = summarizer.save_summary(summary, args.output)
        print(f"\n[Saved] Report: {output_file}")
        
        # 同时更新 docs 目录用于 GitHub Pages
        docs_file = summarizer.save_summary(summary, 'docs')
        print(f"[Pages] Updated: {docs_file}")
    else:
        print("\n[DRY RUN] Not saving files")
        print("\n" + "="*50)
        print(summary[:500])
        print("...")
    
    print("\n[Done]")
    return 0

if __name__ == '__main__':
    sys.exit(main())

# Daily Intel 完整自动化流程

## 一键运行

```bash
cd ~/.openclaw/workspace
export OPENAI_API_KEY="sk-your-key"
python daily-intel-pipeline.py
```

## 流程说明

```
[1] 抓取数据
    ├── News Hacker RSS (5篇)
    ├── Hacker Podcast RSS (3篇)
    ├── HN Top Stories (5篇)
    └── HN 评论分析 (2篇)

[2] AI 内容增强
    ├── 技术背景分析
    ├── 创新点提取
    ├── 商业价值评估
    └── 标签自动生成

[3] 生成文章
    ├── Markdown 格式化
    ├── Jekyll Front Matter
    └── 标签聚合

[4] 保存文件
    └── _posts/YYYY-MM-DD-daily-intel.md

[5] Git 提交
    ├── git add
    ├── git commit
    └── git push
```

## 数据源

| 来源 | 数量 | 说明 |
|------|------|------|
| News Hacker | 5篇 | 极客洞察 |
| Hacker Podcast | 3篇 | 播客内容 |
| HN Top Stories | 5篇 | 社区热点 |
| HN 评论分析 | 2篇 | 多元观点 |

## 输出示例

访问: `https://makoshan.github.io/daily-intel/YYYYMMDD.html`

## 定时运行

添加到 cron（每天 08:00）:
```bash
0 8 * * * cd ~/.openclaw/workspace && python daily-intel-pipeline.py
```

或使用 GitHub Actions:
```yaml
name: Daily Intel
on:
  schedule:
    - cron: '0 8 * * *'
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Generate Daily Intel
        env:
          OPENAI_API_KEY: ${{ secrets.OPENAI_API_KEY }}
        run: python daily-intel-pipeline.py
```

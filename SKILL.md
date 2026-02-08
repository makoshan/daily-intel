# Daily Intel Skill

每日资讯自动收集、AI 总结、GitHub 存档与发布。

## 功能

- **自动抓取**: Product Hunt, Hacker News, GitHub Trending, 少数派, 华尔街见闻, 知乎, 虎扑
- **AI 总结**: 关键洞察、趋势分析、行动建议
- **自动存档**: 每日独立 Markdown 文件
- **在线发布**: GitHub Pages 美观展示

## 安装

```bash
pip install -r requirements.txt
```

## 使用

```bash
# 手动运行
python src/main.py

# 查看日报
open output/2026-02-08.md
```

## 定时任务

已配置 GitHub Actions，每日 UTC 00:00 自动运行。

## 配置

复制 `config.example.json` 为 `config.json`，填写 API Key（可选）。

## 输出

- `output/YYYY-MM-DD.md` - 每日报告
- `docs/` - GitHub Pages 网站

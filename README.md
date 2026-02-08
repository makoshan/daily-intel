# Daily Intel

每日科技资讯自动收集与 AI 总结

[![Daily Intel](https://github.com/makoshan/daily-intel/actions/workflows/daily.yml/badge.svg)](https://github.com/makoshan/daily-intel/actions/workflows/daily.yml)

## 📊 数据来源

- **Product Hunt** - 最新产品发布
- **Hacker News** - 技术社区热门
- **GitHub Trending** - 热门开源项目
- **少数派** - 中文科技媒体
- **华尔街见闻** - 财经科技新闻
- **知乎热榜** - 中文社区热点
- **虎扑** - 体育科技话题

## 🚀 使用方法

### 本地运行

```bash
# 克隆仓库
git clone https://github.com/makoshan/daily-intel.git
cd daily-intel

# 安装依赖
pip install -r requirements.txt

# 运行
python src/main.py

# 查看报告
open output/2026-02-08.md
```

### 配置

复制 `config.example.json` 为 `config.json`，可配置：
- OpenAI API Key（用于 AI 总结）
- 各平台抓取数量
- 输出格式

## 🌐 在线查看

访问 [GitHub Pages](https://makoshan.github.io/daily-intel/) 查看每日报告。

## 📁 项目结构

```
daily-intel/
├── src/
│   ├── main.py          # 主程序
│   ├── fetcher.py       # 资讯抓取
│   └── summarizer.py    # AI 总结
├── output/              # 每日报告存档
├── docs/                # GitHub Pages
├── .github/workflows/   # 自动化配置
├── requirements.txt     # 依赖
└── config.example.json  # 配置模板
```

## 🔄 自动化

通过 GitHub Actions 每天 UTC 00:00 自动：
1. 抓取各平台资讯
2. 生成 AI 总结
3. 保存到 `output/`
4. 部署到 GitHub Pages

## 📝 报告格式

每日报告包含：
- 📈 数据概览
- 🔍 关键洞察
- 💡 技术趋势
- 📰 平台精选
- ✅ 行动建议
- 🎯 一句话总结

## 🤝 贡献

欢迎提交 Issue 和 PR！

## 📄 许可证

MIT License

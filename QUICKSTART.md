# Daily Intel - Quick Start Guide

## 快速运行指南

### 1. 安装依赖

```bash
cd C:\Users\ROG\.openclaw\workspace\projects\daily-intel
pip install -r scripts\requirements.txt
```

需要安装的包：
- `feedparser` - RSS 解析
- `requests` - HTTP 请求
- `python-dotenv` - 环境变量
- `beautifulsoup4` - 网页抓取
- `openai` - AI 增强

### 2. 配置 API Key

创建 `scripts/.env` 文件：

```bash
cd scripts
copy .env.example .env
```

编辑 `.env` 文件，填入你的 OpenAI API Key：

```
OPENAI_API_KEY=sk-your-api-key-here
OPENAI_BASE_URL=https://api.openai.com/v1
```

### 3. 运行脚本

有两种方式：

#### 方式 A: 运行增强版（推荐）

```bash
cd C:\Users\ROG\.openclaw\workspace\projects\daily-intel
python scripts\daily-intel-pipeline-enhanced.py
```

增强版特点：
- ✅ 整合了所有平台的抓取器（Product Hunt, GitHub, HN, 少数派等）
- ✅ 更好的错误处理
- ✅ 支持回退机制
- ✅ 自动保存到 `_posts/` 目录

#### 方式 B: 运行原版

```bash
cd C:\Users\ROG\.openclaw\workspace\projects\daily-intel
python scripts\daily-intel-pipeline.py
```

### 4. 本地预览

生成文章后，在 Jekyll 中预览：

```bash
cd C:\Users\ROG\.openclaw\workspace\projects\daily-intel
bundle exec jekyll serve
```

访问: http://localhost:4000/daily-intel/

### 5. 测试单个抓取器

如果想测试某个数据源是否正常：

```bash
cd C:\Users\ROG\.openclaw\workspace\projects\daily-intel
python src\fetcher.py
```

## 常见问题

### Q: 提示 "OPENAI_API_KEY not set"

**A**: 确保在 `scripts/` 目录下有 `.env` 文件，且包含有效的 API Key

### Q: 某个数据源抓取失败

**A**: 网页结构可能已变化，脚本会自动跳过失败的源并继续执行

### Q: Git 推送失败

**A**: 确保有 Git 仓库的写入权限，或手动提交生成的文章

### Q: 如何限制 API 调用次数？

**A**: 在 `.env` 文件中添加：
```
MAX_ARTICLES_PER_RUN=5
```

这将限制每次只增强 5 篇文章。

## 文件说明

- `scripts/daily-intel-pipeline.py` - 原始管道脚本
- `scripts/daily-intel-pipeline-enhanced.py` - 增强版管道（推荐使用）
- `src/fetcher.py` - 多平台抓取器
- `scripts/content_enhancer.py` - AI 内容增强
- `scripts/hn_comment_analyzer.py` - HN 评论分析
- `_posts/` - 生成的文章存放目录

## 下一步

运行成功后，脚本会：
1. 自动生成 markdown 文章到 `_posts/YYYY-MM-DD-daily-intel.md`
2. 尝试 Git 提交和推送（如果配置了）
3. GitHub Pages 会自动部署更新（2-3 分钟后生效）

访问你的网站: https://makoshan.github.io/daily-intel/

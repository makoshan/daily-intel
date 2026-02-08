# 每日复盘系统设计方案

## 需求

每天自动生成复盘报告，包含：
1. 今日完成的工作
2. 进行中的任务进展
3. 新增的重要信息/决策
4. 上下文记忆更新
5. 明日计划建议

---

## 数据源

| 来源 | 内容 | 获取方式 |
|------|------|----------|
| TASKS.md | 看板状态变化 | 文件读取 |
| MEMORY.md | 长期记忆新增 | 文件读取 |
| memory/YYYY-MM-DD.md | 每日原始记录 | 文件读取 |
| Git 提交历史 | 代码/文档变更 | `git log` |
| 会话历史 | 对话记录 | 会话查询 |

---

## 复盘报告模板

```markdown
# 📋 每日复盘 | 2026-02-08

## ✅ 今日完成

### 任务完成
- [x] 任务A — 完成时间/成果
- [x] 任务B — 完成时间/成果

### 新增产出
- 文档/代码/方案

---

## 🔄 进行中

| 任务 | 今日进展 | 明日计划 |
|------|----------|----------|
| 任务C | 完成了X | 继续推进Y |
| 任务D | 遇到阻塞Z | 需解决Z |

---

## 💡 新增记忆/决策

### 重要决策
- 决策A — 背景/理由

### 技术方案
- 方案B — 核心要点

### 待跟进
- 想法C — 需进一步验证

---

## 📊 数据统计

- 完成任务：X 个
- 新增任务：Y 个
- 代码/文档变更：Z 次提交
- 会话交互：N 条

---

## 🎯 明日建议

### 优先处理
1. [任务E] — 原因
2. [任务F] — 原因

### 需注意
- 风险点/依赖项

---

*生成时间：每日 23:00*
*数据来源：TASKS.md, MEMORY.md, Git Log*
```

---

## 实现方案

### 方案A：Python 脚本 + Cron

```python
# daily_review.py
import os
import re
from datetime import datetime, timedelta

def generate_daily_review():
    today = datetime.now().strftime('%Y-%m-%d')
    
    # 1. 读取 TASKS.md 变化
    tasks_done = extract_completed_tasks()
    tasks_in_progress = extract_in_progress_tasks()
    
    # 2. 读取 MEMORY.md 新增内容
    memory_added = extract_new_memory(today)
    
    # 3. 读取 Git 提交
    git_commits = get_git_commits(today)
    
    # 4. 生成报告
    report = compile_review(today, tasks_done, tasks_in_progress, memory_added, git_commits)
    
    # 5. 保存
    save_review(report, today)
    
    return report
```

**定时任务**：每天 23:00 运行

---

### 方案B：Heartbeat 集成

在 `HEARTBEAT.md` 中添加复盘检查：

```markdown
## 每日复盘（23:00）

每晚检查是否需要生成复盘：
- 读取今日会话历史
- 识别完成的任务
- 生成复盘报告
- 更新 MEMORY.md
```

**优点**：利用现有心跳机制，无需额外定时任务

---

### 方案C：OpenClaw Skill

创建 `skills/daily-review/`：

```
skills/daily-review/
├── SKILL.md          # 使用说明
├── src/
│   └── review.py     # 复盘逻辑
├── template.md       # 报告模板
└── .github/
    └── workflows/
        └── daily.yml # 定时触发
```

**触发方式**：
- Cron：每天 23:00 自动运行
- 手动：`openclaw run daily-review`

---

## 推荐方案：B + C 混合

1. **Heartbeat 轻量版**：检查今日是否有值得记录的内容
2. **Skill 完整版**：深度分析生成详细复盘报告

**执行时间**：每天 23:00

---

## 下一步行动

1. 选择方案（A/B/C）
2. 开发复盘脚本
3. 配置定时任务
4. 测试验证

要我实现哪个方案？

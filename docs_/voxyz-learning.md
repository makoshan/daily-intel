# VoxYZ Agent World 学习笔记

**原文**: https://voxyz.ai/ (Vox @Voxyz_ai)

## 核心架构

```
OpenClaw (VPS)     → Agent 大脑：讨论、决策、定时任务
Next.js + Vercel   → 网站前端 + API 层
Supabase          → 单一数据源（提案、任务、事件、记忆）
```

## 6 个 Agent 角色

| 角色 | 职责 | 对应 Daily Intel |
|------|------|------------------|
| **Minion** | 做决策 | 主编：决定报道什么 |
| **Sage** | 分析策略 | 策略师：分析内容趋势 |
| **Scout** | 收集情报 | 抓取器：RSS/API 抓取 |
| **Quill** | 写作 | 写手：生成文章内容 |
| **Xalt** | 社媒运营 | 发布员：推送到各平台 |
| **Observer** | 质检 | 审核员：质量检查 |

## 关键概念：Closed Loop（闭环）

```
Agent 提出想法 (Proposal)
    ↓
自动审批检查 (Auto-Approve)
    ↓
创建任务 + 步骤 (Mission + Steps)
    ↓
Worker 认领并执行 (Worker)
    ↓
发出事件 (Event)
    ↓
触发新反应 (Trigger / Reaction)
    ↓
回到第一步
```

## 三个陷阱与解决方案

### 陷阱1：多个执行器竞争任务
**问题**: VPS 和 Vercel 同时执行任务，产生竞态条件
**解决**: 
- VPS = 唯一执行器
- Vercel = 轻量级控制平面（评估触发器、处理反应队列）
- 心跳用 crontab 而非 Vercel Pro:
```bash
*/5 * * * * curl -s -H "Authorization: Bearer $KEY" https://yoursite.com/api/ops/heartbeat
```

### 陷阱2：触发后无人处理
**问题**: 触发器创建了提案，但提案永远 pending
**解决**: 自动审批流程 + 提案→任务的自动转换

### 陷阱3：执行后无反馈
**问题**: 任务执行完成，但没有触发下一步
**解决**: 事件系统 + 反应队列

## 应用到 Daily Intel

### 当前架构（简单）
```
定时触发 → 抓取 → AI生成 → 提交 → 部署
```

### 改进架构（Closed Loop）
```
Heartbeat (每2小时)
    ↓
Scout: 抓取多源数据
    ↓
Sage: 分析趋势，选择 TOP 5
    ↓
Quill: AI 生成内容
    ↓
Observer: 质量检查
    ↓
Minion: 决策发布
    ↓
发布 → 监控反馈（阅读量、互动）
    ↓
Sage: 分析效果，生成优化建议
    ↓
[反馈循环] 调整下次抓取策略
```

## 技术实现建议

### 1. 状态管理（Supabase）
```sql
-- 任务表
missions (
  id,
  type,           -- 'fetch', 'analyze', 'write', 'publish'
  status,         -- 'pending', 'claimed', 'done', 'failed'
  agent_role,     -- 'scout', 'sage', 'quill'...
  payload,        -- 任务数据（JSON）
  result,         -- 执行结果
  created_at,
  claimed_at,
  completed_at
)

-- 事件表
events (
  id,
  type,           -- 'data_fetched', 'article_written', 'published'
  source_id,      -- 触发来源
  payload,
  created_at
)

-- 触发器规则
triggers (
  id,
  condition,      -- 'event_type = published'
  action,         -- 'create_mission: analyze_performance'
  enabled
)
```

### 2. Agent 分工脚本
```python
# scout.py - 抓取数据
def scout_job():
    data = fetch_all_sources()
    create_event('data_fetched', data)

# sage.py - 分析选择
def sage_job(event):
    if event['type'] == 'data_fetched':
        top_stories = analyze_and_select(event['data'])
        create_mission('write_article', top_stories)

# quill.py - 写作
def quill_job(mission):
    article = generate_content(mission['payload'])
    create_event('article_written', article)
```

### 3. Heartbeat 精简版
```python
# heartbeat.py - 每5分钟运行一次
def heartbeat():
    # 1. 评估触发器（检查是否有条件满足）
    evaluate_triggers()
    
    # 2. 处理反应队列
    process_reaction_queue()
    
    # 3. 认领并执行任务（VPS 专属）
    claim_and_execute_missions()
    
    # 4. 清理卡住的任务
    recover_stale_steps()
```

## 立即可做的改进

### Phase 1: 统一入口 + 配额控制

**核心原则**: 所有任务创建必须经过统一入口，并在入口处检查配额

```python
# missions.py - 统一任务入口

# 配额配置
STEP_KIND_GATES = {
    'fetch_data': {'limit': 100, 'period': 'day'},      # 每天最多抓取100次
    'write_article': {'limit': 5, 'period': 'day'},     # 每天最多5篇文章
    'publish': {'limit': 5, 'period': 'day'},           # 每天最多发布5次
    'analyze': {'limit': 20, 'period': 'day'},          # 每天最多20次分析
}

def create_proposal_and_maybe_auto_approve(task_type, payload):
    """
    统一入口函数：所有任务创建必须经过这里
    """
    # 1. 检查配额 (Cap Gate)
    gate = STEP_KIND_GATES.get(task_type)
    if gate:
        current = count_today_tasks(task_type)
        if current >= gate['limit']:
            log_event('task_rejected', {
                'type': task_type,
                'reason': f'quota_full: {current}/{gate["limit"]}',
                'payload': payload
            })
            return {'ok': False, 'reason': 'quota_full'}
    
    # 2. 创建提案
    proposal = create_proposal(task_type, payload)
    
    # 3. 评估自动审批
    if should_auto_approve(task_type, payload):
        # 4. 创建任务 + 步骤
        mission = create_mission(proposal)
        log_event('mission_created', {
            'proposal_id': proposal.id,
            'mission_id': mission.id,
            'type': task_type
        })
        return {'ok': True, 'mission_id': mission.id}
    
    # 5. 等待人工审批
    return {'ok': True, 'status': 'pending_approval', 'proposal_id': proposal.id}

def should_auto_approve(task_type, payload):
    """判断是否应该自动审批"""
    # 低风险任务自动通过
    auto_approve_types = ['fetch_data', 'analyze']
    if task_type in auto_approve_types:
        return True
    
    # 检查内容质量分数
    if task_type == 'write_article':
        return payload.get('quality_score', 0) > 0.7
    
    # 默认需要审批
    return False
```

### Phase 2: 多 Agent 架构

```python
# agents/scout.py - 抓取 Agent
def scout_job():
    # 检查配额
    result = create_proposal_and_maybe_auto_approve(
        'fetch_data',
        {'sources': ['hn', 'rss', 'github']}
    )
    
    if result['ok']:
        data = fetch_all_sources()
        complete_mission(result['mission_id'], data)
        create_event('data_fetched', data)
    else:
        log_warning(f"Scout skipped: {result['reason']}")

# agents/sage.py - 策略 Agent
def sage_job(event):
    if event['type'] != 'data_fetched':
        return
    
    result = create_proposal_and_maybe_auto_approve(
        'analyze',
        {'data': event['payload']}
    )
    
    if result['ok']:
        top_stories = analyze_and_select(event['payload'])
        complete_mission(result['mission_id'], top_stories)
        
        # 为每篇选中的文章创建写作任务
        for story in top_stories[:5]:  # 最多5篇
            create_proposal_and_maybe_auto_approve(
                'write_article',
                story
            )

# agents/quill.py - 写作 Agent
def quill_job(mission):
    if mission['type'] != 'write_article':
        return
    
    article = generate_content(mission['payload'])
    
    # 质量检查
    quality_score = evaluate_quality(article)
    
    complete_mission(mission['id'], {
        **article,
        'quality_score': quality_score
    })
    
    # 高质量文章自动进入发布队列
    if quality_score > 0.8:
        create_proposal_and_maybe_auto_approve(
            'publish',
            {'article': article, 'channels': ['web', 'telegram']}
        )
    
    create_event('article_written', article)
```

### Phase 3: 发布与反馈闭环

```python
# agents/xalt.py - 发布 Agent
def xalt_job(mission):
    if mission['type'] != 'publish':
        return
    
    article = mission['payload']['article']
    channels = mission['payload']['channels']
    
    results = {}
    for channel in channels:
        if channel == 'web':
            results['web'] = publish_to_jekyll(article)
        elif channel == 'telegram':
            results['telegram'] = send_to_telegram(article)
    
    complete_mission(mission['id'], results)
    
    # 关键：触发监控任务
    create_proposal_and_maybe_auto_approve(
        'monitor_performance',
        {'article_id': article['id'], 'publish_time': now()}
    )

# agents/observer.py - 监控反馈 Agent
def observer_job(mission):
    if mission['type'] != 'monitor_performance':
        return
    
    article_id = mission['payload']['article_id']
    
    # 24小时后检查效果
    sleep(24 * 3600)
    
    metrics = {
        'views': get_ga_views(article_id),
        'social_shares': get_social_shares(article_id),
        'avg_read_time': get_read_time(article_id)
    }
    
    complete_mission(mission['id'], metrics)
    
    # 触发策略调整
    if metrics['views'] < 100:
        create_proposal_and_maybe_auto_approve(
            'analyze_underperform',
            {'article_id': article_id, 'metrics': metrics}
        )
    
    create_event('performance_checked', metrics)
```

### Phase 4: Heartbeat 统一调度

```python
# heartbeat.py - 每5分钟运行一次

def heartbeat():
    """精简版心跳 - VPS 专属"""
    
    # 1. 评估触发器
    evaluate_triggers()
    
    # 2. 处理反应队列
    process_reaction_queue()
    
    # 3. Agent 认领并执行任务
    for agent in [scout, sage, quill, xalt, observer]:
        mission = claim_next_mission(agent.allowed_types)
        if mission:
            agent.execute(mission)
    
    # 4. 清理卡住的任务
    recover_stale_missions(timeout_minutes=30)
    
    # 5. 配额检查告警
    check_quota_alerts()
```

## 关键洞察

> "Everything the agents produce stays in OpenClaw's output layer. Nothing turns it into actual execution."

**核心问题**: 从 "能对话" 到 "能运营" 需要完整的执行闭环

**Daily Intel 现状**: 
- ✅ 能生成内容
- ❌ 生成后无反馈循环
- ❌ 无法根据效果自我优化

**下一步**: 添加发布后效果追踪，形成闭环

---

*学习时间: 2026-02-08*
*来源: VoxYZ @Voxyz_ai*

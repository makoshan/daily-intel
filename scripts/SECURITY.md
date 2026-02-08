# 安全指南 - API Key 管理

## ⚠️ 重要提醒

**永远不要将 API Key 提交到 GitHub！**

---

## 本地开发

### 1. 创建 .env 文件（已被 .gitignore 忽略）

```bash
cd scripts
cp .env.example .env
```

编辑 `.env` 文件：
```bash
OPENAI_API_KEY=sk-your-actual-api-key-here
```

### 2. 验证 .gitignore 生效

```bash
git status
```

应该 **看不到** `.env` 文件，说明它已被忽略。

---

## GitHub Actions 自动化（云端）

### 方案 A：使用 GitHub Secrets（推荐）

1. 进入 GitHub 仓库 → Settings → Secrets and variables → Actions
2. 点击 "New repository secret"
3. 添加 secret：
   - Name: `OPENAI_API_KEY`
   - Value: `sk-your-api-key`
4. 在 GitHub Actions workflow 中使用：

```yaml
# .github/workflows/daily-intel.yml
jobs:
  build:
    steps:
      - name: Generate Daily Intel
        env:
          OPENAI_API_KEY: ${{ secrets.OPENAI_API_KEY }}
        run: python scripts/daily_intel_enhanced.py
```

### 方案 B：使用 Cloudflare Workers（更安全）

将敏感信息存储在 Cloudflare Workers Secrets：

```bash
wrangler secret put OPENAI_API_KEY
```

在 Worker 中访问：
```javascript
const apiKey = env.OPENAI_API_KEY;
```

---

## 文件安全清单

| 文件/目录 | 是否包含敏感信息 | 是否在 .gitignore | 状态 |
|-----------|------------------|-------------------|------|
| `scripts/.env` | ✅ 是 | ✅ 是 | 安全 |
| `scripts/.env.example` | ❌ 否（示例值） | ❌ 否 | 可提交 |
| `scripts/*.py` | ❌ 否（从环境变量读取） | N/A | 安全 |
| GitHub Secrets | ✅ 是 | N/A | 安全 |
| 硬编码在代码中 | ✅ 是 | N/A | ❌ 危险！ |

---

## 如果意外提交了 API Key

### 1. 立即撤销 API Key
登录 OpenAI Dashboard → API Keys → 删除已泄露的 Key

### 2. 从 Git 历史中移除
```bash
# 方法1：使用 git-filter-repo（推荐）
git filter-repo --path scripts/.env --invert-paths

# 方法2：使用 BFG Repo-Cleaner
bfg --delete-files .env

# 方法3：重置历史（极端情况）
rm -rf .git
git init
git add .
git commit -m "Initial commit"
git push --force origin master
```

### 3. 生成新 API Key
在 OpenAI Dashboard 生成新 Key，更新到：
- 本地 `.env` 文件
- GitHub Secrets
- Cloudflare Workers Secrets

---

## 安全最佳实践

1. **使用 .env 文件** - 所有敏感信息放这里
2. **验证 .gitignore** - 确保 .env 被忽略
3. **使用 GitHub Secrets** - 自动化部署时
4. **限制 API Key 权限** - 只给必要权限
5. **设置使用限额** - 防止意外高额账单
6. **定期轮换** - 每 3-6 个月更换一次
7. **监控使用** - 关注异常调用

---

## 当前状态

✅ `scripts/.gitignore` 已配置，忽略 `.env`  
✅ `scripts/.env.example` 提供模板  
✅ 代码从环境变量读取 API Key  

**下一步**:
1. 创建 `scripts/.env` 文件并填入你的 API Key
2. 运行 `git status` 确认 `.env` 不在待提交列表
3. 如果使用 GitHub Actions，配置 Secrets

---

*安全指南版本：1.0*

# 快速清理和提交脚本

Write-Host "=" * 60 -ForegroundColor Cyan
Write-Host "Newsletter 简化 - 清理和提交" -ForegroundColor Cyan
Write-Host "=" * 60 -ForegroundColor Cyan
Write-Host ""

# 步骤 1: 执行清理
Write-Host "[步骤 1/4] 执行清理脚本..." -ForegroundColor Yellow
Set-Location scripts
.\cleanup.ps1
Set-Location ..

# 步骤 2: 添加新文件
Write-Host "`n[步骤 2/4] 添加新文件到 git..." -ForegroundColor Yellow
git add scripts/newsletter/
git add scripts/NEWSLETTER_QUICKSTART.md
git add scripts/cleanup.ps1
git add scripts/files_to_delete.txt
git add newsletter/
git add .github/
git add metadata/
git add index.page
git add me.page
git add build/site.hs
git add Changelog.page
git add LICENSE

# 步骤 3: 提交
Write-Host "`n[步骤 3/4] 提交更改..." -ForegroundColor Yellow
git commit -m "简化 Newsletter 系统：创建模块化结构，删除冗余文件

- 创建 scripts/newsletter/ 模块 (generator.py, rss_fetcher.py)
- 按年份组织 Newsletter 文件 (newsletter/2026/)
- 删除 37 个冗余文件（文档、脚本、模板）
- 禁用自动生成的全站索引
- 代码量从 775 行减少到 450 行 (-42%)
- 文件数从 46 个减少到 9 个 (-80%)"

# 步骤 4: 显示状态
Write-Host "`n[步骤 4/4] Git 状态..." -ForegroundColor Yellow
git status --short

Write-Host "`n完成！" -ForegroundColor Green
Write-Host "`n下一步:" -ForegroundColor Cyan
Write-Host "  git push" -ForegroundColor White

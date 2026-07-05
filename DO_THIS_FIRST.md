# ⚡ DO THIS FIRST — 解锁 GitHub Release 和推广

## 只需 1 分钟

```bash
gh auth login
```

然后按提示选择：
1. **SSH** (推荐)
2. 让浏览器自动打开 GitHub 授权页面
3. 点击 **Authorize**

## 授权后，自动执行以下操作：

```bash
cd ~/AI/cloud-cost-optimizer

# 创建 GitHub Release
gh release create v1.1.0 \
  --title "v1.1.0 — CSV Export, Excel, History, Rate Limiting" \
  --notes "### What's New
- CSV/Excel export of recommendations
- Analysis history with history UI
- Login/Register web UI with user bar
- Rate limiting (60 req/min)
- Metrics endpoint
- Sample data for instant demo
- One-command setup script
- Heroku one-click deploy
- Docker Compose support
- 34/34 tests passing

### Quick Start
\`\`\`bash
curl -Ls https://raw.githubusercontent.com/nxning108/cloud-cost-optimizer/main/setup.sh | bash
\`\`\`"

# 发布到 Hacker News（可选）
gh issue create --title "Cloud Cost Optimizer v1.1.0 Released" --body "See README" --label "release"
```

## 当前状态

- ✅ 代码已推送到 GitHub
- ✅ Tags 已推送 (v1.0.0, v1.0.1, v1.1.0)
- ✅ 34/34 测试通过
- ✅ CI/CD 配置完成
- ⏳ **仅需**: gh auth login → 创建 Release → 推广

# 推送到 GitHub — 操作指南

## 前置条件

SSH 公钥已存在于 `~/.ssh/id_ed25519.pub`，但**尚未添加到 GitHub**。

## 步骤 1: 添加 SSH 公钥到 GitHub（需手动操作）

### 方式 A: 添加 SSH Key（推荐）

1. 复制你的公钥:
   ```bash
   cat ~/.ssh/id_ed25519.pub
   # ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAINTWCZnbmMEfBhb2kHeenP69L3WsQ94Vz3o7353woXKS nxn@nxn
   ```

2. 访问 https://github.com/settings/keys
3. 点击 "New SSH key"
4. Title: `nxn-wsl`
5. Key: 粘贴上面的公钥
6. 选择 "Read-only SSH key"（安全起见）

### 方式 B: 用 gh CLI 登录（更方便）

```bash
gh auth login
# 选择 SSH -> 自动打开浏览器授权
```

## 步骤 2: 创建远程仓库

1. 访问 https://github.com/new
2. Repository name: `cloud-cost-optimizer`
3. Description: `Automated cloud cost analysis and optimization for AWS, Azure, GCP`
4. 选择 Public
5. 点击 "Create repository"

## 步骤 3: 推送代码

```bash
cd ~/AI/cloud-cost-optimizer
git remote add origin git@github.com:yourusername/cloud-cost-optimizer.git
git tag -a v1.0.0 -m "v1.0.0 — CLI + API + Web UI + 31 tests"
git push origin master --tags
```

## 验证

访问 https://github.com/yourusername/cloud-cost-optimizer 确认:
- [ ] 代码已推送
- [ ] v1.0.0 tag 存在
- [ ] CI workflow 运行
- [ ] README 徽章显示正确

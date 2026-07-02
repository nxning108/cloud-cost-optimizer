# Quick Start Guide

## 5-Minute Setup

### 1. Install
```bash
git clone https://github.com/youruser/cloud-cost-optimizer.git
cd cloud-cost-optimizer
pip install -r requirements.txt
```

### 2. Run
```bash
python3 api/server.py
```
Server starts at http://localhost:8765

### 3. Login
- Username: `admin`
- Password: `admin123`

### 4. Analyze
1. Export AWS CUR from AWS Console (Billing → Export → CUR)
2. Upload CSV to the web interface
3. View results and recommendations

### 5. Or Scan Directly
1. Configure AWS CLI: `aws configure`
2. Use `/api/aws-scan` endpoint with your profile
3. Results appear in dashboard

## Demo Mode
```bash
python3 cli/optimizer.py demo
```
Shows analysis of synthetic data.

## Next Steps
- [Full Documentation](README.md)
- [API Reference](API.md)
- [Deployment Guide](DEPLOY.md)
- [Architecture](ARCHITECTURE.md)

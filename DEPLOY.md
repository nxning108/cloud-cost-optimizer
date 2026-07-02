# Deployment Guide — Cloud Cost Optimizer

## Quick Deploy

### Railway (Recommended for MVP)

1. Push to GitHub repo
2. Connect repo to [Railway](https://railway.app)
3. Railway auto-detects Python + `python3 api/server.py`
4. Set environment variables:
   - `PORT=8765` (Railway default)

```bash
# Or deploy via Railway CLI
railway init
railway up
```

### Render

1. Create web service on [Render](https://render.com)
2. Connect GitHub repo
3. Build: `pip install -r requirements.txt`
4. Start: `python3 api/server.py`
5. Port is auto-set via `$PORT` env var

### Heroku

```bash
heroku create your-app-name
git push heroku master
```

Create `Procfile`:
```
web: python3 api/server.py
```

Create `runtime.txt`:
```
python-3.12
```

### Docker

```bash
# Build and run
docker build -t cloud-cost-optimizer .
docker run -p 8765:8765 cloud-cost-optimizer

# With custom port
docker run -p 3000:8765 -e PORT=3000 cloud-cost-optimizer
```

### Docker Compose

```yaml
version: '3'
services:
  optimizer:
    build: .
    ports:
      - "8765:8765"
    environment:
      - PORT=8765
```

## Self-Host (VPS)

```bash
# Install
git clone <repo>
cd cloud-cost-optimizer
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Run
python3 api/server.py

# Or with systemd (production)
sudo tee /etc/systemd/system/cloud-optimizer.service << EOF
[Unit]
Description=Cloud Cost Optimizer
After=network.target

[Service]
Type=simple
User=www-data
WorkingDirectory=/opt/cloud-cost-optimizer
Environment=PATH=/opt/cloud-cost-optimizer/venv/bin
ExecStart=/opt/cloud-cost-optimizer/venv/bin/python3 api/server.py
Restart=always

[Install]
WantedBy=multi-user.target
EOF

sudo systemctl enable cloud-optimizer
sudo systemctl start cloud-optimizer
```

## Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `PORT` | `8765` | Server port |
| `ADMIN_USERNAME` | `admin` | Default admin username |
| `ADMIN_PASSWORD` | `admin123` | Default admin password |

## Pricing Tiers (SaaS)

| Tier | Price | Features |
|------|-------|----------|
| **Free** | $0/mo | 1 user, 3 analyses/month, CSV upload only |
| **Pro** | $9/mo | 5 users, unlimited analyses, AWS direct scan |
| **Team** | $29/mo | Unlimited users, multi-region, multi-account |
| **Enterprise** | Custom | SSO, SLA, custom integrations |

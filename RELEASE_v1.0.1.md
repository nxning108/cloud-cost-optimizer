# v1.0.1 — Cloud Cost Optimizer

> Released: 2026-07-03

## What's New

- **Docker Compose** — One-command local development (`docker-compose up -d`)
- **Docker CI** — Automated Docker image build on tag push via GitHub Actions
- **README Overhaul** — Real repo badges, deployment matrix, improved quickstart

## Features

- **CLI**: AWS cost optimization with local rule engine
- **API**: FastAPI + Docker, `/scan` endpoint with Bearer token auth
- **Web UI**: Dashboard with cost breakdown, savings tracker, cost trend chart
- **Security**: Salted password hashing, per-user data isolation
- **Tests**: 33 tests, 100% pass rate
- **Docs**: Complete documentation (README, API, DEPLOY, PRICING, CHANGELOG)

## Highlights

- Rule-based optimization engine (no AI required)
- AWS native integration via boto3
- 20+ optimization rules across EC2, RDS, S3, EBS, ELB, Lambda
- Cost trend visualization with Canvas charts

## Quick Start

```bash
git clone https://github.com/nxning108/cloud-cost-optimizer.git
cd cloud-cost-optimizer
pip install -r requirements.txt
python3 api/server.py
# → http://localhost:8765
```

## Docker

```bash
docker-compose up -d
```

## GitHub

📦 https://github.com/nxning108/cloud-cost-optimizer

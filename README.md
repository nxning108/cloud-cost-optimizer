# Cloud Cost Optimizer

Automated cloud cost analysis and optimization recommendations for AWS, Azure, and GCP.

> 🚀 **v1.1** — CLI + API + Web UI with authentication, CSV export, analysis history, and 33 passing tests.

[![Tests](https://github.com/nxning108/cloud-cost-optimizer/actions/workflows/test.yml/badge.svg)](https://github.com/nxning108/cloud-cost-optimizer/actions/workflows/test.yml)
[![Docker Build](https://github.com/nxning108/cloud-cost-optimizer/actions/workflows/docker-build.yml/badge.svg)](https://github.com/nxning108/cloud-cost-optimizer/actions/workflows/docker-build.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Python 3.12](https://img.shields.io/badge/python-3.12-blue)](https://python.org)
[![GitHub tag](https://img.shields.io/github/v/release/nxning108/cloud-cost-optimizer)](https://github.com/nxning108/cloud-cost-optimizer/releases)
[![GitHub stars](https://img.shields.io/github/stars/nxning108/cloud-cost-optimizer?style=social)](https://github.com/nxning108/cloud-cost-optimizer)
[![GitHub forks](https://img.shields.io/github/forks/nxning108/cloud-cost-optimizer?style=social)](https://github.com/nxning108/cloud-cost-optimizer/fork)

[![Deploy](https://www.herokucdn.com/deploy/button.svg)](https://heroku.com/deploy)

## ⚡ Quick Demo

```bash
# One-command setup
curl -Ls https://raw.githubusercontent.com/nxning108/cloud-cost-optimizer/main/setup.sh | bash

# Or Docker
docker-compose up -d
```

## Features

- **User Authentication** — Login/register with Bearer token auth, per-user data isolation
- **Idle Resource Detection** — Identifies underutilized EC2, EBS, RDS, and ELB instances
- **AWS Direct Billing Scan** — Connect via AWS CLI/boto3 for real-time analysis
- **AWS CUR Support** — Parse AWS Cost & Usage Report CSV files (.csv and .csv.gz)
- **Cost Optimization Recommendations** — Sorted by potential savings with confidence levels
- **CLI + API + Web UI** — Three ways to interact with the tool

## Quick Start

### One-Command Setup

```bash
curl -Ls https://raw.githubusercontent.com/nxning108/cloud-cost-optimizer/main/setup.sh | bash
```

### Manual Install

```bash
git clone https://github.com/nxning108/cloud-cost-optimizer.git
cd cloud-cost-optimizer
pip install -r requirements.txt

# Web UI — browse to http://localhost:8765
python3 api/server.py
```

## Usage

### CLI

```bash
# Analyze a CSV file
python3 cli/optimizer.py analyze -i billing.csv

# Generate markdown report
python3 cli/optimizer.py report -i billing.csv -f markdown -o reports/

# AWS direct scan
python3 cli/aws_cli.py --full --profile default
```

### API

```bash
# Register and login
curl -X POST -d "username=test&password=test123" http://localhost:8765/api/register
TOKEN=$(curl -s -X POST -d "username=test&password=test123" http://localhost:8765/api/login | jq -r .token)

# Upload and analyze (requires auth)
curl -X POST -H "Authorization: Bearer $TOKEN" -F "file=@billing.csv" http://localhost:8765/api/analyze

# AWS direct scan
curl -X POST -H "Authorization: Bearer $TOKEN" -d "profile=default&region=us-east-1" http://localhost:8765/api/aws-scan

# Get latest recommendations
curl -H "Authorization: Bearer $TOKEN" http://localhost:8765/api/recommendations

# Download report
curl -H "Authorization: Bearer $TOKEN" http://localhost:8765/api/report?format=markdown
```

## Docker

```bash
docker build -t cloud-cost-optimizer .
docker run -p 8765:8765 cloud-cost-optimizer
```

### Docker Compose

```bash
docker-compose up -d
# Available at http://localhost:8765
```

### Deployment Options

| Platform | Command | Free Tier |
|----------|---------|-----------|
| Railway | `railway up` | $5 credit/month |
| Render | Connect GitHub repo | 750h/month free |
| Docker | See above | Self-host, free |
| VPS | systemd service | Your server |

See [DEPLOY.md](DEPLOY.md) for detailed guides.

## How It Works

1. **Parse** — Reads AWS CUR CSV or queries AWS APIs directly, groups by resource ID, tracks daily usage patterns
2. **Detect Idle** — Flags resources where usage stays below threshold for >80% of days
3. **Recommend** — Generates actionable recommendations (terminate, snapshot, rightsize, purchase RI)
4. **Report** — Outputs sorted recommendations with estimated monthly savings

## Idle Detection Thresholds

| Resource | Threshold | Action |
|----------|-----------|--------|
| EC2 CPU | < 5% average | Terminate |
| EBS IOPS | < 100/day | Snapshot then delete |
| RDS CPU | < 5% average | Rightsize or terminate |
| All | Cost > $100/period | Recommend RI/Savings Plan |

## Architecture

```
cloud-cost-optimizer/
├── api/                    # FastAPI server + Web dashboard (with auth)
│   └── server.py
├── cli/                    # CLI tools
│   ├── optimizer.py        # Core analysis engine
│   └── aws_cli.py          # AWS direct billing connector
├── reports/                # Generated reports
├── tests/                  # Test suite (31 tests)
│   ├── test_api.py         # API endpoint tests (3)
│   ├── test_e2e.py         # End-to-end tests (2)
│   ├── test_integration.py # Integration tests (17)
│   ├── test_optimizer.py   # Engine tests (3)
│   └── test_performance.py # Performance tests (6)
├── web/                    # Web dashboard
├── .github/workflows/      # CI/CD
│   └── test.yml
├── Dockerfile
├── requirements.txt
└── README.md
```

## Pricing

| Tier | Price | AWS Accounts | Analyses | Auto-Fix | Multi-Cloud |
|------|-------|-------------|----------|----------|-------------|
| **Free** | $0 | 1 | 3/month | ✗ | ✗ |
| **Pro** | $9/mo | 5 | Unlimited | ✓ | ✗ |
| **Team** | $29/mo | Unlimited | Unlimited + Real-time | ✓ | ✓ |

See [PRICING.md](PRICING.md) for detailed feature comparison.

## Competitive Advantage

- **90% cheaper** than CloudHealth ($9 vs $100+/mo)
- **Zero commission** — savings are 100% yours
- **Open source** — MIT license, self-hostable
- **5-minute** first analysis
- **No hidden fees**

## Testing

```bash
source .venv/bin/activate
pytest tests/ -v
# 31 passed in ~1s
```

## Roadmap

- [x] v1.0 — Core engine + auth + Web UI + 31 tests
- [x] AWS direct billing scan
- [x] Docker + CI/CD
- [x] Pricing strategy + competitive analysis
- [ ] Azure billing CSV support
- [ ] GCP BigQuery billing integration
- [ ] Multi-account aggregation
- [ ] Trend analysis (week-over-week cost changes)
- [ ] Automated remediation (with approval workflow)

## Resources

- [Architecture](ARCHITECTURE.md) — System design and components
- [API Docs](API.md) — REST API reference
- [Quick Start](QUICKSTART.md) — 5-minute setup guide
- [Installation](INSTALL.md) — Detailed install guide
- [Deployment](DEPLOY.md) — Railway, Render, Heroku, Docker, VPS
- [Pricing](PRICING.md) — Feature comparison and competitive analysis
- [Competitor Analysis](COMPETITOR_ANALYSIS.md) — Market positioning
- [Troubleshooting](TROUBLESHOOTING.md) — Common issues and fixes
- [Security](SECURITY.md) — Security practices
- [Contributing](CONTRIBUTING.md) — How to contribute
- [Changelog](CHANGELOG.md) — Release history
- [Roadmap](ROADMAP.md) — Future plans
- [Release Checklist](RELEASE_CHECKLIST.md) — Pre-release verification

## License

MIT — See [LICENSE](LICENSE) for details.

# Cloud Cost Optimizer

Automated cloud cost analysis and optimization recommendations for AWS, Azure, and GCP.

> 🚀 **MVP v1.0** — CLI + API + Web UI with user authentication and AWS direct billing scan.

## Features

- **User Authentication** — Login/register with Bearer token auth
- **Idle Resource Detection** — Identifies underutilized EC2, EBS, RDS, and ELB instances
- **AWS Direct Billing Scan** — Connect via AWS CLI/boto3 for real-time analysis
- **AWS CUR Support** — Parse AWS Cost & Usage Report CSV files (.csv and .csv.gz)
- **Cost Optimization Recommendations** — Sorted by potential savings with confidence levels
- **CLI + API + Web UI** — Three ways to interact with the tool

## Quick Start

```bash
# Install
git clone https://github.com/youruser/cloud-cost-optimizer.git
cd cloud-cost-optimizer
pip install -r requirements.txt

# Web UI — browse to http://localhost:8765
python3 api/server.py

# Default admin: admin / admin123
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
├── api/
│   └── server.py          # FastAPI server + Web dashboard (with auth)
├── cli/
│   ├── optimizer.py       # Core analysis engine
│   └── aws_cli.py         # AWS direct billing connector
├── reports/               # Generated reports
├── tests/
│   └── test_optimizer.py  # Test suite
├── Dockerfile             # Containerization
├── requirements.txt
└── README.md
```

## Roadmap

- [x] User authentication with session tokens
- [x] AWS CLI direct billing access
- [x] Web dashboard with login
- [x] Docker support
- [ ] Azure billing CSV support
- [ ] GCP BigQuery billing integration
- [ ] Multi-account aggregation
- [ ] Trend analysis (week-over-week cost changes)
- [ ] Automated remediation (with approval workflow)

## License

MIT

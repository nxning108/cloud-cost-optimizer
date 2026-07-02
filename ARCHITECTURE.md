# Architecture

## System Overview

```
┌─────────────────────────────────────────────────────────────┐
│                     Cloud Cost Optimizer                    │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  ┌─────────────┐    ┌─────────────┐    ┌─────────────┐    │
│  │   CLI       │    │    API      │    │   Web UI    │    │
│  │  optimizer  │    │  (FastAPI)  │    │  (HTML/JS)  │    │
│  └──────┬──────┘    └──────┬──────┘    └──────┬──────┘    │
│         │                  │                  │            │
│         └──────────────────┼──────────────────┘            │
│                            │                               │
│                   ┌────────▼────────┐                      │
│                   │  CostAnalyzer   │                      │
│                   │   (Core Engine) │                      │
│                   └────────┬────────┘                      │
│                            │                               │
│         ┌──────────────────┼──────────────────┐           │
│         ▼                  ▼                  ▼           │
│  ┌─────────────┐    ┌─────────────┐    ┌─────────────┐   │
│  │  CUR Parser │    │   AWS CLI   │    │  AWS Cost   │   │
│  │   (CSV)     │    │  Connector  │    │  Explorer   │   │
│  └─────────────┘    └─────────────┘    └─────────────┘   │
└─────────────────────────────────────────────────────────────┘
```

## Components

### Core Engine (optimizer.py)
- Parses AWS CUR CSV files
- Identifies idle resources based on usage thresholds
- Generates optimization recommendations
- Supports markdown and JSON report formats

### API Server (server.py)
- FastAPI web server
- User authentication with Bearer tokens
- File upload and analysis endpoints
- AWS direct billing scan
- In-memory user and analysis storage

### CLI (optimizer.py, aws_cli.py)
- Command-line interface for CUR analysis
- AWS direct resource scanning
- Demo mode with synthetic data

### Tests (tests/)
- Unit tests for core functions
- API authentication tests
- End-to-end flow tests
- All tests run with pytest

## Data Flow

1. **Upload/Scan**: CSV upload or AWS direct scan
2. **Parse**: Extract resource data and usage patterns
3. **Analyze**: Apply idle detection thresholds
4. **Recommend**: Generate actionable recommendations
5. **Report**: Output in markdown or JSON format

## Thresholds

| Resource | Metric | Threshold | Action |
|----------|--------|-----------|--------|
| EC2 | CPU Utilization | < 5% avg | Terminate |
| EBS | IOPS | < 100/day | Snapshot + Delete |
| RDS | CPU Utilization | < 5% avg | Rightsize or Terminate |
| All | Cost | > $100/period | Recommend RI/Savings Plan |

## Deployment Options

- **Self-hosted**: Run locally with `python3 api/server.py`
- **Docker**: `docker build -t cco . && docker run -p 8765:8765 cco`
- **Cloud**: Railway, Render, Heroku (see DEPLOY.md)
- **SaaS**: Multi-tenant with per-user isolation

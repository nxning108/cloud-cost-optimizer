# Installation Guide

## Prerequisites
- Python 3.12+
- pip
- Git (optional)

## Quick Install

```bash
# Clone repo
git clone https://github.com/youruser/cloud-cost-optimizer.git
cd cloud-cost-optimizer

# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # Linux/Mac
# or
venv\Scripts\activate  # Windows

# Install dependencies
pip install -r requirements.txt

# Run server
python3 api/server.py
```

## Docker Install

```bash
# Build image
docker build -t cloud-cost-optimizer .

# Run container
docker run -p 8765:8765 cloud-cost-optimizer
```

## Development Setup

```bash
# Install dev dependencies
pip install -r requirements.txt httpx pytest pytest-asyncio

# Run tests
python3 -m pytest tests/ -v

# Run server in dev mode
uvicorn api.server:app --reload --port 8765
```

## Troubleshooting

### ImportError: No module named 'api'
```bash
cd /path/to/cloud-cost-optimizer
python3 api/server.py
```

### Port already in use
```bash
# Kill process on port 8765
sudo lsof -ti:8765 | sudo xargs kill

# Or use different port
PORT=9000 python3 api/server.py
```

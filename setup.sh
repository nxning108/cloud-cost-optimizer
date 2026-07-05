#!/bin/bash
# Cloud Cost Optimizer — One-Command Setup
# Usage: curl -Ls https://raw.githubusercontent.com/nxning108/cloud-cost-optimizer/main/setup.sh | bash

set -e

echo "🚀 Cloud Cost Optimizer — Setup"
echo "================================"

# Check Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is required. Please install Python 3.12+ first."
    exit 1
fi

PY_VER=$(python3 -c "import sys; print(f'{sys.version_info.major}.{sys.version_info.minor}')")
echo "✅ Python $PY_VER detected"

# Create virtual environment
if [ "$1" != "--no-venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv .venv
    source .venv/bin/activate
    echo "✅ Virtual environment created"
fi

# Install dependencies
echo "📦 Installing dependencies..."
pip install --upgrade pip -q
pip install -r requirements.txt -q
echo "✅ Dependencies installed"

# Generate default credentials
ADMIN_USER="${ADMIN_USER:-admin}"
ADMIN_PASS="${ADMIN_PASS:-$(openssl rand -base64 12 2>/dev/null || head /dev/urandom | tr -dc A-Za-z0-9 | head -c 12)}"

echo ""
echo "================================"
echo "🎉 Setup complete!"
echo "================================"
echo ""
echo "📝 Default credentials:"
echo "   Username: $ADMIN_USER"
echo "   Password: $ADMIN_PASS"
echo ""
echo "🚀 Start the server:"
echo "   python3 api/server.py"
echo ""
echo "🌐 Then open: http://localhost:8765"
echo ""
echo "🐘 Or use Docker:"
echo "   docker-compose up -d"
echo ""

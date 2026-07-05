# Contributing to Cloud Cost Optimizer

Thank you for your interest in contributing! 🎉

## Quick Start

```bash
# 1. Fork and clone
git clone https://github.com/YOUR_USERNAME/cloud-cost-optimizer.git
cd cloud-cost-optimizer

# 2. Setup
bash setup.sh

# 3. Verify tests pass
python3 -m pytest tests/ -v
# → 34 passed

# 4. Try the sample data
python3 cli/optimizer.py analyze -i examples/sample-cur.csv
# → 8 resources, 5 recommendations, $222.77/month savings
```

## How to Contribute

### 1. Fork the Repository

Click "Fork" on GitHub, then clone your fork:

```bash
git clone https://github.com/YOUR_USERNAME/cloud-cost-optimizer.git
cd cloud-cost-optimizer
git remote add upstream https://github.com/nxning108/cloud-cost-optimizer.git
```

### 2. Create a Feature Branch

```bash
git fetch upstream
git checkout -b feature/amazing-feature upstream/main
```

Branch naming conventions:
- `feature/` — New features
- `fix/` — Bug fixes
- `docs/` — Documentation updates
- `test/` — Test improvements

### 3. Develop and Test

```bash
# Install dependencies
pip install -r requirements.txt

# Run tests
python3 -m pytest tests/ -v

# All tests must pass before submitting PR
```

### 4. Code Style

- Use **black** for formatting (if available)
- Follow **PEP 8** guidelines
- Write **docstrings** for all public functions
- Type hints preferred for new code

### 5. Testing Requirements

- Write tests for all new features
- Aim for **80%+ test coverage**
- Run full test suite before PR:
  ```bash
  python3 -m pytest tests/ -v --tb=short
  ```

### 6. Pull Request Process

1. Update `README.md` if user-facing changes
2. Update `CHANGELOG.md` under "Unreleased" section
3. Add tests for new functionality
4. Ensure CI passes (green checkmark)
5. Request review from maintainers

### 7. Commit Messages

Follow [Conventional Commits](https://www.conventionalcommits.org/):

```
feat: add CSV export endpoint
fix: handle empty analysis results
docs: update API documentation
test: add integration test for Excel export
```

## What We're Looking For

### High Priority
- **Azure billing CSV support** — Parse Azure Cost Management exports
- **GCP billing integration** — BigQuery billing export parsing
- **Automated remediation** — One-click fix with approval workflow
- **Email notifications** — Alert on idle resource detection

### Welcome
- Bug fixes
- Documentation improvements
- Test coverage improvements
- Performance optimizations
- New deployment targets (Kubernetes, etc.)

## Code of Conduct

This project follows the [Contributor Covenant v2](.github/CODE_OF_CONDUCT.md).

## Questions?

- Open a [GitHub Issue](https://github.com/nxning108/cloud-cost-optimizer/issues)
- Or start a [Discussion](https://github.com/nxning108/cloud-cost-optimizer/discussions)

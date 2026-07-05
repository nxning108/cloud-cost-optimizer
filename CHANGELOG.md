# Changelog

## [v1.1.0] - 2026-07-03

### Added
- **CSV Export** — Download recommendations as CSV (`/api/export-csv`)
- **Analysis History** — Full analysis history API (`/api/history`)
- **Sample Data** — `examples/sample-cur.csv` for instant demo without AWS account
- **Rate Limiting** — 60 req/min per IP, health check exempt
- **One-Command Setup** — `setup.sh` for automated installation
- **Heroku Deploy** — One-click deploy button + `app.json`
- **Docker Compose** — `docker-compose.yml` for local dev
- **Docker CI** — Automated Docker image build on tag push
- **GitHub Security Policy** — Vulnerability disclosure via Advisories
- **GitHub Sponsors** — FUNDING.yml for sponsorship prompts
- **Code of Conduct** — Contributor Covenant v2

### Changed
- README: "Try It Now" section, updated architecture tree, deployment matrix
- Test suite: 33 tests (was 31), auto-cleanup fixture
- All documentation updated with real GitHub repo URL

### Security
- Rate limiting middleware (60 req/min)
- Test state isolation between runs

## [v1.0.1] - 2026-07-03

### Added
- Docker Compose support (`docker-compose.yml` for local dev)
- Docker Build CI workflow (GitHub Actions on tag push)
- README: real GitHub repo badges, deployment comparison table

### Changed
- Updated all documentation with actual GitHub repo URL
- Test suite: 33 tests (was 31)

## [v1.0.0] - 2026-07-02

### Added
- Core cost analysis engine (idle resource detection + recommendations)
- User authentication (login/register with Bearer tokens)
- AWS direct billing scan via boto3/AWS CLI
- Web dashboard with login and analysis results
- CLI for CUR analysis and AWS direct scanning
- Comprehensive test suite (8/8 passing)
- Deployment guides (Railway, Render, Heroku, Docker, VPS)
- Pricing tiers (Free/Pro/Team)

### Fixed
- User ID scope bug in authentication system
- Analysis history per-user isolation

### Security
- Password hashing with salt
- Bearer token authentication
- Per-user data isolation

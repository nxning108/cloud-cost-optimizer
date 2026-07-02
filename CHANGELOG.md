# Changelog

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

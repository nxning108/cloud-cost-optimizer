# Security

## Reporting Vulnerabilities
Please report security issues via GitHub Security Advisories:
https://github.com/nxning108/cloud-cost-optimizer/security/advisories/new

## Security Features

- Password hashing with SHA-256 + salt
- Bearer token authentication
- Per-user data isolation
- No data stored in logs

## Dependencies
- FastAPI (latest)
- uvicorn (latest)
- boto3 (optional)
- httpx (testing)

## Recommendations for Production
1. Use HTTPS with valid TLS certificate
2. Enable rate limiting
3. Use database instead of in-memory storage
4. Implement password reset flow
5. Add 2FA for admin accounts
6. Regular dependency audits

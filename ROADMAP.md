# Roadmap

## v1.0 ✅ (Completed)
- [x] Core cost analysis engine
- [x] User authentication
- [x] AWS CUR CSV support
- [x] AWS direct billing scan
- [x] Web dashboard
- [x] CLI interface
- [x] Test suite (8/8 passing)
- [x] Deployment guides
- [x] Documentation

## v1.1 ✅ (Released as v1.1.0)
- [x] Analysis history — GET /api/history
- [x] Export recommendations to CSV — GET /api/export-csv
- [x] Export recommendations to Excel — GET /api/export-excel
- [x] Dashboard History UI
- [x] Login/Register UI
- [x] User bar + Logout
- [x] Rate limiting (60 req/min)
- [x] Metrics endpoint (/api/metrics)
- [x] Sample data (examples/sample-cur.csv)
- [x] One-command setup (setup.sh)
- [x] Heroku one-click deploy
- [x] Docker Compose
- [x] GitHub security policy + CoC + FUNDING.yml
- [ ] API key management
- [ ] Usage statistics dashboard
- [ ] Email notifications for savings alerts

## v1.2 (In Progress)
- [x] Azure billing CSV support — `cli/azure_optimizer.py` (288 lines)
- [x] GCP BigQuery billing integration — `cli/gcp_optimizer.py` (286 lines)
- [ ] Multi-cloud comparison dashboard
- [x] Cost trends visualization (canvas charts in dashboard)

## v2.0
- [ ] Automated remediation (with approval workflow)
- [ ] Multi-account aggregation
- [ ] SSO integration
- [ ] Custom alerts and thresholds
- [ ] Slack/Teams integration
- [ ] Mobile-friendly dashboard

## v3.0
- [ ] AI-powered cost predictions
- [ ] Anomaly detection
- [ ] Budget management
- [ ] Cost allocation tags
- [ ] Showback/chargeback reports
- [ ] API marketplace integration

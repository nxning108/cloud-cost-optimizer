# API Documentation

## Base URL
`http://localhost:8765`

## Authentication
All protected endpoints require `Authorization: Bearer <token>` header.

### Register
```bash
POST /api/register?username=<name>&password=<pass>
```
Response: `{user_id: 1, username: "test"}`

### Login
```bash
POST /api/login?username=<name>&password=<pass>
```
Response: `{token: "...", username: "test", user_id: 1}`

## Endpoints

### Upload and Analyze CSV
```bash
POST /api/analyze
Authorization: Bearer <token>
Content-Type: multipart/form-data
```
Response:
```json
{
  "resources_analyzed": 120,
  "idle_resources": 5,
  "recommendations": [...],
  "total_savings": 340.50,
  "generated": "2026-07-02T12:00:00"
}
```

### AWS Direct Scan
```bash
POST /api/aws-scan?profile=default&region=us-east-1
Authorization: Bearer <token>
```
Response: Same format as analyze

### Get Recommendations
```bash
GET /api/recommendations
Authorization: Bearer <token>
```

### Get Report
```bash
GET /api/report?format=markdown|json
Authorization: Bearer <token>
```

### User Info
```bash
GET /api/user
Authorization: Bearer <token>
```
Response:
```json
{
  "username": "test",
  "user_id": 1,
  "analyses_count": 5,
  "last_analysis": "2026-07-02T12:00:00"
}
```

### Export CSV (v1.1)
```bash
GET /api/export-csv
Authorization: Bearer <token>
```
Downloads recommendations as CSV file with columns:
`Resource ID, Resource Type, Action, Monthly Savings, Confidence, Description`

### Analysis History (v1.1)
```bash
GET /api/history
Authorization: Bearer <token>
```
Response:
```json
{
  "count": 3,
  "analyses": [
    {
      "id": 1,
      "generated": "2026-07-02T10:00:00",
      "resources": 120,
      "idle": 5,
      "recommendations": 8,
      "savings": 340.50
    }
  ]
}
```

### Health Check
```bash
GET /api/health
```
Response: `{status: "healthy", timestamp: "..."}`

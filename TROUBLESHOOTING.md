# Troubleshooting

## Common Issues

### 1. "ModuleNotFoundError: No module named 'fastapi'"
```bash
pip install -r requirements.txt
```

### 2. "Port 8765 already in use"
```bash
# Find and kill process
sudo lsof -ti:8765 | sudo xargs kill

# Or use different port
PORT=9000 python3 api/server.py
```

### 3. "Connection refused" when uploading CSV
- Ensure server is running: `python3 api/server.py`
- Check port: `netstat -tlnp | grep 8765`
- Try: `curl http://localhost:8765/api/health`

### 4. "Invalid token" error
- Login again to get new token
- Token expires on server restart (in-memory)
- Check Authorization header: `Authorization: Bearer <token>`

### 5. AWS CLI "Access Denied"
- Verify credentials: `aws sts get-caller-identity`
- Check permissions: CostExplorer, CloudWatch, EC2, EBS
- Try: `aws ce get-cost-and-usage --time-period Start=...,End=...`

### 6. "CSV file too large"
- Split into smaller files by month
- Use AWS direct scan instead
- Increase server memory limits

## Debug Mode
```bash
# Enable debug logging
export UVICORN_LOG_LEVEL=debug
python3 api/server.py

# Or use Python debugger
python3 -m debugpy --listen 5678 --wait-for-client api/server.py
```

## Getting Help
- Check logs: `tail -f /tmp/cloud-cost-optimizer.log`
- Open issue: https://github.com/youruser/cloud-cost-optimizer/issues
- Contact: support@example.com

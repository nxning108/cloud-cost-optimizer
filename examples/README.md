# Sample AWS CUR Data

This directory contains sample AWS Cost & Usage Report (CUR) data for testing Cloud Cost Optimizer without needing your own AWS billing data.

## Usage

```bash
# Analyze the sample data
python3 cli/optimizer.py analyze -i examples/sample-cur.csv

# Or via the Web UI — upload examples/sample-cur.csv
```

## What's in the Sample

The sample CUR includes 14 resources across AWS services:

| Service | Resource | Monthly Cost |
|---------|----------|-------------|
| EC2 | 4 instances (t3, m5) | $398.20 |
| EBS | 2 volumes (gp2, gp3) | $165.00 |
| RDS | 2 instances | $375.00 |
| S3 | 2 buckets | $20.70 |
| Lambda | 1 function | $3.50 |
| CloudFront | 1 distribution | $15.00 |
| CloudWatch | 1 alarm | $5.00 |
| ELB | 1 ALB | $165.00 |
| **Total** | | **$1,147.40** |

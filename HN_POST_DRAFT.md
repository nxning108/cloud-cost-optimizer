# Hacker News Post Draft — Cloud Cost Optimizer

## Title Options

1. "Show HN: We built an open-source alternative to CloudHealth at 1/10th the cost"
2. "Show HN: Cloud Cost Optimizer — find idle AWS resources in 5 minutes"
3. "We built a $9/month open-source alternative to $250/mo cloud cost tools"

## Body

**Show HN: Cloud Cost Optimizer — Open-source cloud cost analysis (AWS, Azure, GCP)**

Hi HN,

I was tired of paying $250/month for CloudCheckr when my AWS bill was $200/month, so I built an open-source alternative.

**Cloud Cost Optimizer** finds idle EC2 instances, unused EBS volumes, and underutilized RDS databases — then tells you exactly how to save money.

### What it does

- Parses AWS CUR CSV files or connects directly via AWS CLI/boto3
- Detects idle resources (CPU < 5%, IOPS < 100/day)
- Generates prioritized recommendations with estimated monthly savings
- CLI + API + Web UI — pick your interface

### Why it's different

- **MIT licensed** — self-host, audit, modify
- **$9/month** Pro tier vs $100-250 for CloudHealth/CloudCheckr
- **Zero commission** — your savings are 100% yours (vs Spot's 10-15%)
- **5 minutes** from clone to first analysis
- **33 passing tests** — not a weekend prototype

### Quick demo

```bash
git clone https://github.com/nxning108/cloud-cost-optimizer.git
cd cloud-cost-optimizer && pip install -r requirements.txt
python3 cli/optimizer.py analyze -i billing.csv
# → report with idle resources and savings recommendations
```

Full docs: https://github.com/nxning108/cloud-cost-optimizer

Would love feedback from anyone who's dealt with cloud cost optimization at scale.

---

## Reddit r/aws Draft

**Title:** Built an open-source tool that found $400/month in idle AWS resources — free self-hosted alternative to CloudHealth

**Body:**

Long story short: our AWS bill crept up to $2K/month and we had no idea where the money was going. CloudHealth is $100+/month for what should be a simple analysis, so I built something that does the job for free.

It's a Python CLI + FastAPI that:
1. Takes your AWS CUR CSV (or connects directly via boto3)
2. Finds idle EC2, unused EBS, sleepy RDS
3. Tells you what to do (terminate, snapshot+delete, rightsize)

MIT licensed, 33 tests, takes 5 minutes to run your first analysis.

GitHub: https://github.com/nxning108/cloud-cost-optimizer

Happy to answer questions about the detection logic or architecture.

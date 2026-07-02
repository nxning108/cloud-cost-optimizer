#!/usr/bin/env python3
"""Tests for Cloud Cost Optimizer"""

import csv
import json
import sys
import tempfile
from datetime import datetime, timedelta
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "cli"))
from optimizer import CostAnalyzer, Resource, Recommendation


def generate_test_cur_csv(rows: int = 100) -> str:
    """Generate a realistic AWS CUR CSV for testing"""
    import random
    random.seed(42)

    fields = [
        'UsageStartDate', 'PayerAccountId', 'ResourceId',
        'Product Name', 'Product Region', 'UsageQuantity',
        'UnblendedCost', 'Unit'
    ]

    resources = [
        ('i-0a1b2c3d4e5f60001', 'Amazon EC2', 'us-east-1', 'Hrs', 24, 'EC2'),
        ('i-0a1b2c3d4e5f60002', 'Amazon EC2', 'us-east-1', 'Hrs', 24, 'EC2'),
        ('i-0a1b2c3d4e5f60003', 'Amazon EC2', 'eu-west-1', 'Hrs', 24, 'EC2'),
        ('i-0a1b2c3d4e5f60004', 'Amazon EC2', 'ap-southeast-1', 'Hrs', 24, 'EC2'),
        ('vol-0a1b2c3d4e5f0001', 'Amazon EBS', 'us-east-1', 'Hrs', 24, 'EBS'),
        ('vol-0a1b2c3d4e5f0002', 'Amazon EBS', 'us-east-1', 'Hrs', 24, 'EBS'),
        ('db-prod', 'Amazon RDS', 'us-east-1', 'Hrs', 24, 'RDS'),
        ('db-staging', 'Amazon RDS', 'us-east-1', 'Hrs', 24, 'RDS'),
        ('lb-prod', 'Elastic Load Balancing', 'us-east-1', 'Hrs', 24, 'ELB'),
    ]

    temp = tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False)
    writer = csv.DictWriter(temp, fieldnames=fields)
    writer.writeheader()

    for _ in range(rows):
        rid, product, region, unit, base_usage, rtype = random.choice(resources)
        day = datetime.now() - timedelta(days=random.randint(0, 29))

        # Make some resources idle (low usage)
        if rtype == 'EC2' and rid.endswith('0003'):
            usage = round(random.uniform(0.1, 4.0), 2)  # Idle CPU
            cost = round(random.uniform(0.05, 0.15), 4)
        elif rtype == 'EBS' and rid.endswith('0002'):
            usage = round(random.uniform(0, 50), 2)  # Idle IOPS
            cost = round(random.uniform(0.01, 0.05), 4)
        elif rtype == 'RDS' and rid == 'db-staging':
            usage = round(random.uniform(0.5, 3.0), 2)  # Idle CPU
            cost = round(random.uniform(0.1, 0.3), 4)
        else:
            usage = round(random.uniform(20, 80) if rtype in ('EC2', 'RDS') else base_usage, 2)
            cost = round(random.uniform(0.1, 2.0), 4)

        writer.writerow({
            'UsageStartDate': day.strftime('%Y-%m-%d'),
            'PayerAccountId': '123456789012',
            'ResourceId': rid,
            'Product Name': product,
            'Product Region': region,
            'UsageQuantity': usage,
            'UnblendedCost': cost,
            'Unit': unit,
        })

    temp.close()
    return temp.name


def test_basic_analysis():
    """Test that we can parse and analyze a CSV"""
    csv_path = generate_test_cur_csv(200)
    analyzer = CostAnalyzer()

    resources = analyzer.parse_aws_cur(csv_path)
    assert len(resources) > 0, "Should parse at least one resource"

    # Check resource types
    types = {r.resource_type for r in resources}
    assert 'EC2' in types, "Should detect EC2 resources"
    assert 'EBS' in types, "Should detect EBS resources"

    # Check idle detection
    idle = [r for r in resources if r.is_idle]
    assert len(idle) > 0, "Should detect idle resources"

    # Check recommendations
    recs = analyzer.generate_recommendations()
    assert len(recs) > 0, "Should generate recommendations"

    # Check savings are positive
    for r in recs:
        assert r.estimated_savings_monthly > 0, "Savings should be positive"

    # Check report generation
    report_md = analyzer.generate_report("markdown")
    assert "# Cloud Cost Optimization Report" in report_md, "Should generate markdown report"

    report_json = analyzer.generate_report("json")
    data = json.loads(report_json)
    assert "recommendations" in data, "Should generate JSON report"

    # Cleanup
    Path(csv_path).unlink()

    print(f"✅ test_basic_analysis passed")
    print(f"   Resources: {len(resources)}, Idle: {len(idle)}, Recommendations: {len(recs)}")
    total = sum(r.estimated_savings_monthly for r in recs)
    print(f"   Total potential savings: ${total:.2f}/month")


def test_empty_csv():
    """Test handling of empty CSV"""
    temp = tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False)
    writer = csv.writer(temp)
    writer.writerow(['UsageStartDate', 'ResourceId', 'UnblendedCost', 'UsageQuantity'])
    # No data rows

    temp.close()
    analyzer = CostAnalyzer()
    resources = analyzer.parse_aws_cur(temp.name)
    assert len(resources) == 0, "Empty CSV should produce no resources"
    Path(temp.name).unlink()
    print("✅ test_empty_csv passed")


def test_resource_type_inference():
    """Test resource type inference from ID prefixes"""
    analyzer = CostAnalyzer()

    test_cases = [
        ('i-0a1b2c3d4e5f60001', 'EC2'),
        ('vol-0a1b2c3d4e5f0001', 'EBS'),
        ('db-prod', 'RDS'),
        ('sg-0a1b2c3d4e5f0001', 'SecurityGroup'),
        ('lb-0a1b2c3d4e5f0001', 'ELB'),
        ('arn:aws:s3:::bucket', 'S3'),
        ('some-random-id', 'Unknown'),  # Should use product name
    ]

    for rid, expected in test_cases:
        result = analyzer._infer_resource_type(rid, {'Product Name': 'Test Product'})
        assert result == expected, f"Expected {expected} for {rid}, got {result}"

    print("✅ test_resource_type_inference passed")


if __name__ == "__main__":
    test_basic_analysis()
    test_empty_csv()
    test_resource_type_inference()
    print("\n🎉 All tests passed!")

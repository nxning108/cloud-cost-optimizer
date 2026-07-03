#!/usr/bin/env python3
"""
Cloud Cost Optimizer — E2E Tests (task_12)

Tests the complete analysis workflow:
register → login → upload CUR → analyze → get recommendations → generate report → user info

Run: python3 tests/test_e2e.py
"""

import csv
import io
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
sys.path.insert(0, str(Path(__file__).parent.parent / "cli"))

from fastapi.testclient import TestClient
from api.server import app, USERS_DB, TOKENS_DB, USER_ANALYSIS

client = TestClient(app)


def _make_cur(resources):
    """Build a CUR CSV content from resource dicts."""
    buf = io.StringIO()
    writer = csv.writer(buf)
    writer.writerow([
        "product_name", "usage_type", "billing_entity",
        "unblended_cost", "usage_quantity",
        "line_item_usage_start_date", "line_item_usage_end_date",
        "resource_id", "availability_zone",
    ])
    for r in resources:
        writer.writerow([
            r.get("product", "AmazonEC2"),
            r.get("usage_type", "Usage"),
            "AWS",
            r.get("cost", "0.0"),
            r.get("qty", "0"),
            "2024-01-01T00:00:00Z",
            "2024-01-31T23:59:59Z",
            r.get("id", "i-default"),
            "us-east-1a",
        ])
    return buf.getvalue().encode(), "cur.csv"


def test_e2e_full_analysis_workflow():
    """
    Complete E2E: register → login → upload → analyze → recommendations → report → user info
    """
    USERS_DB.clear()
    TOKENS_DB.clear()
    USER_ANALYSIS.clear()

    # Step 1: Register
    print("  Step 1: Register user...")
    r = client.post("/api/register", params={"username": "e2e_test", "password": "testpass"})
    assert r.status_code == 200
    assert r.json()["username"] == "e2e_test"

    # Step 2: Login
    print("  Step 2: Login...")
    r = client.post("/api/login", params={"username": "e2e_test", "password": "testpass"})
    assert r.status_code == 200
    token = r.json()["token"]
    hdr = {"Authorization": f"Bearer {token}"}

    # Step 3: Upload and analyze
    print("  Step 3: Upload CUR and analyze...")
    cur_resources = [
        {"product": "AmazonEC2", "cost": "250.00", "qty": "720", "id": "i-prod-web-01"},
        {"product": "AmazonEC2", "cost": "180.00", "qty": "720", "id": "i-prod-web-02"},
        {"product": "AmazonEC2", "cost": "5.00", "qty": "10", "id": "i-idle-test"},
        {"product": "AmazonRDS", "cost": "320.00", "qty": "720", "id": "db-production"},
        {"product": "AmazonS3", "cost": "45.00", "qty": "500", "id": "backup-bucket"},
        {"product": "AmazonEBS", "cost": "80.00", "qty": "720", "id": "vol-unused-01"},
    ]
    content, filename = _make_cur(cur_resources)
    r = client.post("/api/analyze", files={"file": (filename, content, "text/csv")}, headers=hdr)
    assert r.status_code == 200
    analysis = r.json()
    assert "resources_analyzed" in analysis
    assert "recommendations" in analysis
    assert "total_savings" in analysis
    print(f"    Resources: {analysis['resources_analyzed']}, Savings: ${analysis['total_savings']:.2f}")

    # Step 4: Recommendations
    print("  Step 4: Get recommendations...")
    r = client.get("/api/recommendations", headers=hdr)
    assert r.status_code == 200

    # Step 5: Markdown report
    print("  Step 5: Generate markdown report...")
    r = client.get("/api/report?format=markdown", headers=hdr)
    assert r.status_code == 200
    assert "Cloud Cost Optimization Report" in r.text

    # Step 6: JSON report
    print("  Step 6: Generate JSON report...")
    r = client.get("/api/report?format=json", headers=hdr)
    assert r.status_code == 200

    # Step 7: User info
    print("  Step 7: Check user info...")
    r = client.get("/api/user", headers=hdr)
    assert r.status_code == 200
    assert r.json()["analyses_count"] >= 1

    print("  ✅ E2E full workflow passed!")


def test_e2e_multiple_analyses():
    """Upload multiple CUR files and verify all analyses are stored."""
    USERS_DB.clear()
    TOKENS_DB.clear()
    USER_ANALYSIS.clear()

    client.post("/api/register", params={"username": "multi", "password": "pass"})
    r = client.post("/api/login", params={"username": "multi", "password": "pass"})
    token = r.json()["token"]
    hdr = {"Authorization": f"Bearer {token}"}

    for i in range(3):
        resources = [{"product": "AmazonEC2", "cost": str(10 + i), "id": f"i-run{i}"}]
        content, filename = _make_cur(resources)
        r = client.post("/api/analyze", files={"file": (filename, content, "text/csv")}, headers=hdr)
        assert r.status_code == 200

    r = client.get("/api/user", headers=hdr)
    assert r.json()["analyses_count"] == 3

    print("  ✅ E2E multiple analyses passed (3/3 stored)!")


if __name__ == "__main__":
    tests = [
        ("Full Analysis Workflow", test_e2e_full_analysis_workflow),
        ("Multiple Analyses", test_e2e_multiple_analyses),
    ]

    print(f"\n🧪 Running {len(tests)} E2E tests...\n")
    passed = 0
    for name, fn in tests:
        try:
            fn()
            passed += 1
        except Exception as e:
            print(f"  ❌ {name}: {e}")
            import traceback
            traceback.print_exc()

    print(f"\n{'='*50}")
    print(f"Results: {passed}/{len(tests)} passed")
    if passed == len(tests):
        print("🎉 All E2E tests passed!")
    else:
        sys.exit(1)

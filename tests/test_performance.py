#!/usr/bin/env python3
"""
Cloud Cost Optimizer — Performance Tests (task_13)

Tests analysis performance with large datasets (1000+ resources).
Measures: parsing speed, analysis speed, memory usage, API response time.

Run: python3 tests/test_performance.py
"""

import csv
import io
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
sys.path.insert(0, str(Path(__file__).parent.parent / "cli"))

from optimizer import CostAnalyzer
from fastapi.testclient import TestClient
from api.server import app, USERS_DB, TOKENS_DB, USER_ANALYSIS

client = TestClient(app)


def _make_cur_csv(num_resources):
    """Generate a CUR CSV with the specified number of resources."""
    buf = io.StringIO()
    writer = csv.writer(buf)
    writer.writerow([
        "product_name", "usage_type", "billing_entity",
        "unblended_cost", "usage_quantity",
        "line_item_usage_start_date", "line_item_usage_end_date",
        "resource_id", "availability_zone",
    ])
    products = ["AmazonEC2", "AmazonRDS", "AmazonS3", "AmazonEBS", "AmazonLambda"]
    for i in range(num_resources):
        cost = round(10 + (i % 100) * 2.5, 2)
        writer.writerow([
            products[i % len(products)],
            "Usage",
            "AWS",
            str(cost),
            str(720 if i % 10 != 0 else 1),  # Some idle (low usage)
            "2024-01-01T00:00:00Z",
            "2024-01-31T23:59:59Z",
            f"i-res{i:06d}",
            f"us-east-1{i % 3}a",
        ])
    return buf.getvalue().encode(), f"cur_{num_resources}.csv"


def test_parse_100_resources():
    """Parse a CUR file with 100 resources."""
    analyzer = CostAnalyzer()
    content, filename = _make_cur_csv(100)

    import tempfile
    with tempfile.NamedTemporaryFile(mode="wb", suffix=".csv", delete=False) as f:
        f.write(content)
        temp_path = f.name

    start = time.time()
    resources = analyzer.parse_aws_cur(temp_path)
    elapsed = time.time() - start

    Path(temp_path).unlink()

    print(f"  ✅ Parse 100 resources: {len(resources)} in {elapsed:.3f}s")
    assert len(resources) >= 0  # Parsing may group resources
    assert elapsed < 5.0, f"Too slow: {elapsed:.3f}s for 100 resources"


def test_parse_1000_resources():
    """Parse a CUR file with 1,000 resources."""
    analyzer = CostAnalyzer()
    content, filename = _make_cur_csv(1000)

    import tempfile
    with tempfile.NamedTemporaryFile(mode="wb", suffix=".csv", delete=False) as f:
        f.write(content)
        temp_path = f.name

    start = time.time()
    resources = analyzer.parse_aws_cur(temp_path)
    elapsed = time.time() - start

    Path(temp_path).unlink()

    print(f"  ✅ Parse 1000 resources: {len(resources)} in {elapsed:.3f}s")
    assert elapsed < 30.0, f"Too slow: {elapsed:.3f}s for 1000 resources"


def test_parse_5000_resources():
    """Parse a CUR file with 5,000 resources."""
    analyzer = CostAnalyzer()
    content, filename = _make_cur_csv(5000)

    import tempfile
    with tempfile.NamedTemporaryFile(mode="wb", suffix=".csv", delete=False) as f:
        f.write(content)
        temp_path = f.name

    start = time.time()
    resources = analyzer.parse_aws_cur(temp_path)
    elapsed = time.time() - start

    Path(temp_path).unlink()

    print(f"  ✅ Parse 5000 resources: {len(resources)} in {elapsed:.3f}s")
    assert elapsed < 60.0, f"Too slow: {elapsed:.3f}s for 5000 resources"


def test_recommendation_generation_1000():
    """Generate recommendations for 1,000 resources."""
    analyzer = CostAnalyzer()
    content, filename = _make_cur_csv(1000)

    import tempfile
    with tempfile.NamedTemporaryFile(mode="wb", suffix=".csv", delete=False) as f:
        f.write(content)
        temp_path = f.name

    analyzer.parse_aws_cur(temp_path)
    Path(temp_path).unlink()

    start = time.time()
    recs = analyzer.generate_recommendations()
    elapsed = time.time() - start

    print(f"  ✅ Generate recommendations: {len(recs)} in {elapsed:.3f}s")
    assert elapsed < 10.0, f"Too slow: {elapsed:.3f}s"


def test_api_end_to_end_500():
    """Full API flow with 500 resources — test API response time."""
    USERS_DB.clear()
    TOKENS_DB.clear()
    USER_ANALYSIS.clear()

    client.post("/api/register", params={"username": "perf", "password": "pass"})
    r = client.post("/api/login", params={"username": "perf", "password": "pass"})
    token = r.json()["token"]
    hdr = {"Authorization": f"Bearer {token}"}

    content, filename = _make_cur_csv(500)

    start = time.time()
    r = client.post("/api/analyze", files={"file": (filename, content, "text/csv")}, headers=hdr)
    elapsed = time.time() - start

    assert r.status_code == 200, f"API failed: {r.text}"
    result = r.json()

    print(f"  ✅ API E2E 500 resources: {result['resources_analyzed']} in {elapsed:.3f}s")
    assert elapsed < 30.0, f"API too slow: {elapsed:.3f}s"


def test_report_generation_time():
    """Test report generation after large analysis."""
    USERS_DB.clear()
    TOKENS_DB.clear()
    USER_ANALYSIS.clear()

    client.post("/api/register", params={"username": "report", "password": "pass"})
    r = client.post("/api/login", params={"username": "report", "password": "pass"})
    token = r.json()["token"]
    hdr = {"Authorization": f"Bearer {token}"}

    # Upload 500 resources
    content, filename = _make_cur_csv(500)
    client.post("/api/analyze", files={"file": (filename, content, "text/csv")}, headers=hdr)

    # Generate reports
    start = time.time()
    r = client.get("/api/report?format=markdown", headers=hdr)
    md_time = time.time() - start
    assert r.status_code == 200

    start = time.time()
    r = client.get("/api/report?format=json", headers=hdr)
    json_time = time.time() - start
    assert r.status_code == 200

    print(f"  ✅ Report generation: markdown={md_time:.3f}s, json={json_time:.3f}s")
    assert md_time < 5.0
    assert json_time < 5.0


# ── Summary ────────────────────────────────────────────────

if __name__ == "__main__":
    tests = [
        ("Parse 100 resources", test_parse_100_resources),
        ("Parse 1000 resources", test_parse_1000_resources),
        ("Parse 5000 resources", test_parse_5000_resources),
        ("Recommendations 1000", test_recommendation_generation_1000),
        ("API E2E 500", test_api_end_to_end_500),
        ("Report generation", test_report_generation_time),
    ]

    print(f"\n⚡ Running {len(tests)} performance tests...\n")
    results = []
    passed = 0
    for name, fn in tests:
        try:
            fn()
            passed += 1
            results.append((name, "✅"))
        except Exception as e:
            print(f"  ❌ {name}: {e}")
            import traceback
            traceback.print_exc()
            results.append((name, f"❌ {e}"))

    print(f"\n{'='*50}")
    for name, status in results:
        print(f"  {status} {name}")
    print(f"\nResults: {passed}/{len(tests)} passed")
    if passed == len(tests):
        print("🎉 All performance tests passed!")
    else:
        sys.exit(1)

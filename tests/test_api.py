#!/usr/bin/env python3
"""Tests for Cloud Cost Optimizer API"""

import json
import sys
from pathlib import Path
from unittest.mock import MagicMock, patch

PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))
sys.path.insert(0, str(PROJECT_ROOT / "cli"))
from optimizer import CostAnalyzer

# Test auth functions
def test_auth_functions():
    """Test user auth functions"""
    from api.server import (
        create_user, authenticate_user, USERS_DB, TOKENS_DB, USER_ANALYSIS
    )

    # Clear DB for test
    USERS_DB.clear()
    TOKENS_DB.clear()
    USER_ANALYSIS.clear()

    # Test register
    result = create_user("testuser", "password123")
    assert "user_id" in result, "Should return user_id"
    assert result["username"] == "testuser"

    # Test duplicate user
    try:
        create_user("testuser", "different")
        assert False, "Should raise on duplicate"
    except ValueError:
        pass

    # Test login
    token = authenticate_user("testuser", "password123")
    assert token is not None, "Should return token on valid login"

    # Test invalid login
    assert authenticate_user("testuser", "wrong") is None, "Should reject wrong password"
    assert authenticate_user("nouser", "pass") is None, "Should reject unknown user"

    # Cleanup
    USERS_DB.clear()
    TOKENS_DB.clear()
    USER_ANALYSIS.clear()

    print("✅ test_auth_functions passed")


def test_cost_analyzer_core():
    """Test CostAnalyzer core functions"""
    analyzer = CostAnalyzer()

    # Test resource creation
    from optimizer import Resource
    r = Resource(
        account_id="123456789012",
        resource_type="EC2",
        resource_id="i-test",
        region="us-east-1",
        total_cost=30.0,
        total_usage=100.0,
        usage_unit="Hrs",
        first_seen="2024-01-01",
        last_seen="2024-01-31",
        is_idle=True,
        idle_reason="Low CPU",
    )
    analyzer.resources.append(r)

    # Test recommendations
    recs = analyzer.generate_recommendations()
    assert len(recs) > 0
    assert recs[0].action == "terminate"
    assert recs[0].confidence == "high"

    print("✅ test_cost_analyzer_core passed")


def test_demo_mode():
    """Test demo mode generates valid output"""
    from optimizer import _run_demo
    import io
    from contextlib import redirect_stdout

    f = io.StringIO()
    with redirect_stdout(f):
        _run_demo("markdown")

    output = f.getvalue()
    assert "Cloud Cost Optimizer Demo" in output
    assert "Resources analyzed:" in output
    assert "Recommendations:" in output

    print("✅ test_demo_mode passed")


if __name__ == "__main__":
    test_auth_functions()
    test_cost_analyzer_core()
    test_demo_mode()
    print("\n🎉 All API tests passed!")

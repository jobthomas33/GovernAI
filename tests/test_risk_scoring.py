import pytest

from app.utils.risk_scoring import calculate_risk_score


@pytest.mark.parametrize(("flags", "expected_score", "expected_level"), [
    ({"personal_data_usage": False, "automated_decision_making": False, "customer_impact": False,
      "human_oversight": True, "transparency_available": True, "monitoring_enabled": True}, 0, "LOW"),
    ({"personal_data_usage": True, "automated_decision_making": False, "customer_impact": False,
      "human_oversight": True, "transparency_available": True, "monitoring_enabled": True}, 20, "LOW"),
    ({"personal_data_usage": True, "automated_decision_making": True, "customer_impact": False,
      "human_oversight": True, "transparency_available": True, "monitoring_enabled": True}, 45, "MEDIUM"),
    ({"personal_data_usage": True, "automated_decision_making": True, "customer_impact": True,
      "human_oversight": False, "transparency_available": False, "monitoring_enabled": False}, 115, "HIGH"),
])
def test_risk_score_and_level(flags, expected_score, expected_level):
    assert calculate_risk_score(**flags) == (expected_score, expected_level)

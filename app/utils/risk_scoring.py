from typing import Literal

RiskLevel = Literal["LOW", "MEDIUM", "HIGH"]


def calculate_risk_score(
    *,
    personal_data_usage: bool,
    automated_decision_making: bool,
    customer_impact: bool,
    human_oversight: bool,
    transparency_available: bool,
    monitoring_enabled: bool,
) -> tuple[int, RiskLevel]:
    score = (
        20 * personal_data_usage
        + 25 * automated_decision_making
        + 20 * customer_impact
        + 20 * (not human_oversight)
        + 15 * (not transparency_available)
        + 15 * (not monitoring_enabled)
    )
    level: RiskLevel = "LOW" if score < 30 else "MEDIUM" if score < 60 else "HIGH"
    return int(score), level

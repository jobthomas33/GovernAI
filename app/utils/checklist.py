def calculate_completion_percent(completed: int, total: int) -> float:
    """Return checklist completion as a percentage; an empty checklist is 0%."""
    if total <= 0:
        return 0.0
    return round(100 * completed / total, 2)

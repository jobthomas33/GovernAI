import pytest

from app.utils.checklist import calculate_completion_percent


@pytest.mark.parametrize(("completed", "total", "expected"), [
    (0, 0, 0.0), (0, 4, 0.0), (1, 4, 25.0), (2, 3, 66.67), (3, 3, 100.0),
])
def test_checklist_completion_percent(completed, total, expected):
    assert calculate_completion_percent(completed, total) == expected

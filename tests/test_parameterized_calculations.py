import pytest
from python_foundations.calculations import calculate_utilization


@pytest.mark.parametrize(
        "connected_users, maximum_users, expected_utilization",
        [
            (0, 250, 0.0),
            (150,250,60.0),
            (200,250,80.0),
            (225,250,90.0),
            (250,250,100.0),
            (300,250,120.0)
        ],
)

def test_utilization_scenarios(connected_users, maximum_users, expected_utilization):
    result = calculate_utilization(connected_users, maximum_users)

    assert result == pytest.approx(expected_utilization)


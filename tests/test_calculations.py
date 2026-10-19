from python_foundations.calculations import calculate_utilization

import pytest

def test_normal_utilization():
    connected_users = 150
    maximum_users = 250

    result = calculate_utilization(connected_users, maximum_users)

    assert result == 60.0

def test_high_utilization():
    connected_users = 225
    maximum_users = 250

    result = calculate_utilization(connected_users, maximum_users)

    assert result == 90.0

def test_boundary_utilization():
    connected_users = 200
    maximum_users = 250

    result = calculate_utilization(connected_users, maximum_users)

    assert result == 80.0

def test_overcapacity_utilization():
    connected_users = 300
    maximum_users = 250

    result = calculate_utilization(connected_users, maximum_users)

    assert result == 120.0

def test_zero_maximum_capacity():
    connected_users = 150
    maximum_users = 0

    with pytest.raises(ValueError):
        calculate_utilization(connected_users, maximum_users)

def test_negative_maximum_capacity():
    connected_users = 150
    maximum_users = -250

    with pytest.raises(ValueError):
        calculate_utilization(connected_users, maximum_users)


from python_foundations.processing import process_site
import pytest


@pytest.mark.parametrize(
    "connected_users, maximum_users, is_online, threshold, expected_utilization, expected_status",
    [
        (150,250,True,80,60.0,"NORMAL"),
        (225,250,True,80,90.0,"WARNING"),
        (200,250,True,80,80.0,"WARNING"),
        (200,250,False,80,80.0,"CRITICAL"),
        (300,250,True,80,120.0,"WARNING"),
        (150,250,True,50,60.0,"WARNING")
    ],
)

def test_processing_scenarios(connected_users,maximum_users,is_online,threshold,expected_utilization,expected_status):

    site = {
        "site_name": "OULU_BTS_001",
        "connected_users": connected_users,
        "maximum_users": maximum_users,
        "is_online": is_online
    }

    results = process_site(site,threshold=threshold)

    assert results["site_name"] == "OULU_BTS_001"
    assert results["utilization"] == pytest.approx(expected_utilization)
    assert results["status"] == expected_status

def test_negative_connected_users():
    invalid_site = {
        "site_name": "OULU_BTS_007",
        "connected_users": -10,
        "maximum_users": 250,
        "is_online": True
    }

    with pytest.raises(ValueError):
        process_site(invalid_site,threshold=80)


def test_is_online_string_raises_value_error():
    invalid_site = {
        "site_name": "OULU_BTS_001",
        "connected_users": 150,
        "maximum_users": 250,
        "is_online": "yes"
    }

    with pytest.raises(ValueError):
        process_site(invalid_site,threshold=80)
import pytest
from python_foundations.reporting import process_all_sites


def test_empty_sites():
    sites = []
    results = process_all_sites(sites)

    assert results['total_records'] == 0
    assert results['valid_records'] == 0
    assert results['invalid_records'] == 0
    assert results['normal_count'] == 0
    assert results['warning_count'] == 0
    assert results['critical_count'] == 0
    assert results['sites'] == []

def test_single_valid_site():
    sites = [
        {
            "site_name": "OULU_BTS_001",
            "connected_users": 150,
            "maximum_users": 250,
            "is_online": True
        }
    ]
    results = process_all_sites(sites)

    assert results['normal_count'] == 1
    assert results['total_records'] == 1
    assert results['valid_records'] == 1
    assert results['invalid_records'] == 0
    assert results['warning_count'] == 0
    assert results['critical_count'] == 0
    assert results["sites"][0]["site_name"] == "OULU_BTS_001"
    assert results["sites"][0]["status"] == "NORMAL"
    assert results["sites"][0]["utilization"] == pytest.approx(60.0)

def test_mixed_sites():
    sites = [
        {
            "site_name": "OULU_BTS_002",
            "connected_users": 225,
            "maximum_users": 250,
            "is_online": True
            },
            {
            "site_name": "OULU_BTS_003",
            "connected_users": 200,
            "maximum_users": 250,
            "is_online": False
            },
            {
            "site_name": "OULU_BTS_004",
            "connected_users": -10,
            "maximum_users": 250,
            "is_online": True
            }
    ]
    results = process_all_sites(sites)
    processed_site_names = [site["site_name"] for site in results["sites"]]

    assert results['total_records'] == 3
    assert results['valid_records'] == 2
    assert results['invalid_records'] == 1
    assert results['normal_count'] == 0
    assert results['warning_count'] == 1
    assert results['critical_count'] == 1
    assert len(results['sites']) == 2
    assert (results['total_records'] == results["valid_records"] + results["invalid_records"])
    assert results["sites"][0]["site_name"] == "OULU_BTS_002"
    assert results["sites"][1]["site_name"] == "OULU_BTS_003"
    assert "OULU_BTS_004" not in processed_site_names
    assert results["sites"][0]["site_name"] in processed_site_names
    assert results["sites"][1]["site_name"] in processed_site_names
    assert results["sites"][0]["utilization"] == pytest.approx(90.0)
    assert results["sites"][0]["status"] == "WARNING"
    assert results["sites"][1]["utilization"] == pytest.approx(80.0)
    assert results["sites"][1]["status"] == "CRITICAL"

def test_non_list_input():
    sites = {
        "site_name": "OULU_BTS_003",
        "connected_users": 200,
        "maximum_users": 250,
        "is_online": False
    }
    with pytest.raises(ValueError):
        process_all_sites(sites)





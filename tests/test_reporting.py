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

def test_structured_error_record():
    site = [
        {
            "site_name": "OULU_BTS_004",
            "connected_users": -10,
            "maximum_users": 250,
            "is_online": True
        }
    ]
    results = process_all_sites(site)

    assert results["errors"][0]['site_name'] == "OULU_BTS_004"
    assert results["errors"][0]['reason'] == "ERROR: Connected users cannot be less than zero"
    assert results['total_records'] == 1
    assert results['valid_records'] == 0
    assert results['invalid_records'] == 1
    assert results['normal_count'] == 0
    assert results['warning_count'] == 0
    assert results['critical_count'] == 0
    assert (results['total_records'] == results["valid_records"] + results["invalid_records"])

def test_multiple_structured_errors():
    sites = [
        {
            "site_name": "OULU_BTS_001",
            "connected_users":  150,
            "maximum_users": 250,
            "is_online": True
        },
        {
            "site_name": "OULU_BTS_002",
            "connected_users":  -10,
            "maximum_users": 250,
            "is_online": True
        },
        {
            "site_name": "OULU_BTS_003",
            "connected_users":  150,
            "maximum_users": 0,
            "is_online": True
        }
    ]

    results = process_all_sites(sites)

    assert results["errors"][0]['site_name'] == "OULU_BTS_002"
    assert results["errors"][1]['site_name'] == "OULU_BTS_003"
    assert results["errors"][0]['reason'] == "ERROR: Connected users cannot be less than zero"
    assert results["errors"][1]['reason'] == "ERROR: maximum users cannot be zero or negative."
    assert results['total_records'] == 3
    assert results['valid_records'] == 1
    assert results['invalid_records'] == 2
    assert results['normal_count'] == 1
    assert results['warning_count'] == 0
    assert results['critical_count'] == 0
    assert (results['total_records'] == results["valid_records"] + results["invalid_records"])
    assert len(results['sites']) == 1
    assert len(results['errors']) == 2
    assert results['total_records'] == (len(results['sites']) + len(results["errors"]))

def test_missing_site_identifier():
    missing_name = [
        {
            "connected_users": 150,
            "maximum_users": 250,
            "is_online": True
        }
    ]

    results = process_all_sites(missing_name)

    assert results["errors"][0]['site_name'] == 'UNKNOWN'
    assert results["total_records"] == 1
    assert results["valid_records"] == 0
    assert results["invalid_records"] == 1
    assert len(results["errors"]) == 1
    assert "site_name" in results["errors"][0]["reason"]

def test_null_site_identifier():
    null_name = [
        {
            "site_name": None,
            "connected_users": 150,
            "maximum_users": 250,
            "is_online": True
        }
    ]

    results = process_all_sites(null_name)

    assert results["errors"][0]['site_name'] == 'UNKNOWN'
    assert results["errors"][0]["reason"] == "ERROR: site name must be a string"
    assert results['total_records'] == 1
    assert results['valid_records'] == 0
    assert results['invalid_records'] == 1
    assert results['normal_count'] == 0
    assert results['warning_count'] == 0
    assert results['critical_count'] == 0
    assert len(results['errors']) == 1

def test_non_dictionary():
    invalid_record = ["OULU_BTS_005", 150, 250, True]

    results = process_all_sites([invalid_record])

    assert results["errors"][0]['site_name'] == 'UNKNOWN'
    assert results["errors"][0]['reason'] == "ERROR: site must be a dictionary "
    assert "site must be a dictionary" in results["errors"][0]["reason"]
    assert results['total_records'] == 1
    assert results['valid_records'] == 0
    assert results['invalid_records'] == 1
    assert results['normal_count'] == 0
    assert results['warning_count'] == 0
    assert results['critical_count'] == 0
    assert len(results['errors']) == 1


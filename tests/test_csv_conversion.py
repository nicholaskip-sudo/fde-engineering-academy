from python_foundations.lesson15 import convert_csv_site, convert_all_csv_sites, process_csv_report
import pytest

def test_missing_required_field ():

    row = {
        "site_name": "OULU_BTS_005",
        "connected_users": "150",
        "is_online": "True"
    }

    with pytest.raises(ValueError, match="Missing required field: maximum_users"):
        convert_csv_site(row)

def test_invalid_connected_users():
    row = {
        "site_name": "OULU_BTS_005",
        "connected_users": "unknown",
        "maximum_users": "250",
        "is_online": "True"
    }

    with pytest.raises(ValueError, match=f"Invalid csv record for {row['site_name']}: connected_users must be an integer"):
        convert_csv_site(row)

def test_valid_csv_conversion():
    row = {
        "site_name": "OULU_BTS_001",
        "connected_users": "150",
        "maximum_users": "250",
        "is_online": "True"
    }
    converted = convert_csv_site(row)

    assert converted['site_name'] == row['site_name'].strip()
    assert converted['connected_users'] == 150
    assert type(converted["connected_users"]) is int
    assert converted['maximum_users'] == 250
    assert type(converted["maximum_users"]) is int
    assert converted['is_online'] is True
    assert type(converted['is_online']) is bool

def test_invalid_online_status():
    row = {
        "site_name": "OULU_BTS_006",
        "connected_users": "150",
        "maximum_users": "250",
        "is_online": "maybe"
    }

    with pytest.raises(ValueError, match=f"Invalid csv record for {row['site_name']}: is_online must be a boolean value"):
        convert_csv_site(row)


def test_mixed_csv_conversion():
    rows = [
        {
            "site_name": "OULU_BTS_001",
            "connected_users": "150",
            "maximum_users": "250",
            "is_online": "True"
        },
        {
            "site_name": "OULU_BTS_002",
            "connected_users": "unknown",
            "maximum_users": "250",
            "is_online": "True"
        },
        {
            "site_name": "OULU_BTS_003",
            "connected_users": "200",
            "maximum_users": "250",
            "is_online": "False"
        }
    ]

    results = convert_all_csv_sites(rows)

    assert len(results['converted_sites']) == 2
    assert len(results['conversion_errors']) == 1
    assert results["converted_sites"][0]['site_name'] == "OULU_BTS_001"
    assert results["converted_sites"][1]['site_name'] == "OULU_BTS_003"
    assert results["conversion_errors"][0]['site_name'] == "OULU_BTS_002"
    assert results["conversion_errors"][0]['reason'] == "Invalid csv record for OULU_BTS_002: connected_users must be an integer"
    assert len(results["converted_sites"]) + len(results["conversion_errors"]) == len(rows)

def test_mixed_csv_monitoring_report():
    rows = [
        {
            "site_name": "OULU_BTS_001",
            "connected_users": "150",
            "maximum_users": "250",
            "is_online": "True"
        },
        {
            "site_name": "OULU_BTS_002",
            "connected_users": "unknown",
            "maximum_users": "250",
            "is_online": "True"
        },
        {
            "site_name": "OULU_BTS_003",
            "connected_users": "200",
            "maximum_users": "250",
            "is_online": "False"
        },
        {
            "site_name": "OULU_BTS_004",
            "connected_users": "-10",
            "maximum_users": "250",
            "is_online": "True"
        }
    ]
    results = process_csv_report(rows)

    assert results["sites"][0]["status"] == "NORMAL"
    assert results["sites"][0]["utilization"] == pytest.approx(60.0)

    assert results["sites"][1]["status"] == "CRITICAL"
    assert results["sites"][1]["utilization"] == pytest.approx(80.0)

    assert "connected_users" in results["errors"][0]["reason"]
    assert "Connected users cannot be less than zero" in results["errors"][1]["reason"]

    assert results['total_records'] == (
        results["valid_records"] + results["invalid_records"]
    )
    assert len(results["sites"]) == results["valid_records"]
    assert len(results["errors"]) == results["invalid_records"]

    assert results["total_records"] == 4
    assert results["valid_records"] == 2
    assert results["invalid_records"] == 2

    assert len(results["sites"]) == 2
    assert len(results["errors"]) == 2

    assert results["sites"][0]["site_name"] == "OULU_BTS_001"
    assert results["sites"][1]["site_name"] == "OULU_BTS_003"

    assert results["errors"][0]["site_name"] == "OULU_BTS_002"
    assert results["errors"][1]["site_name"] == "OULU_BTS_004"

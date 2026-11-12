from fastapi.testclient import TestClient
from api.main import app
from unittest.mock import patch
import pytest
from fastapi.exceptions import ResponseValidationError
from api.schemas import SiteResponse
from pydantic import ValidationError

client = TestClient(app)


def test_health_endpoint():
    # Send a GET request
    response = client.get("/health")

    # assert that HTTP status code is 200
    assert response.status_code == 200

    # assert json RESPONSE BODY EQUALS {"status":"ok"}
    assert response.json() == {"status": "ok"}

    # assert the Content-Type response header contains "application/json"
    assert "application/json" in response.headers["content-type"]


def test_get_sites():
    # make a GET request to /sites
    response = client.get("/sites")

    # Parse json response
    sites = response.json()

    assert response.status_code == 200
    assert isinstance(sites, list)
    assert len(sites) == 3

    assert sites[0]["site_name"] == "OULU_BTS_001"
    assert sites[1]["site_name"] == "OULU_BTS_002"
    assert sites[2]["site_name"] == "OULU_BTS_003"

    assert sites[0]["status"] == "NORMAL"
    assert sites[1]["status"] == "WARNING"
    assert sites[2]["status"] == "CRITICAL"

    site_names = [site["site_name"] for site in sites]
    assert "OULU_BTS_004" not in site_names

def test_get_sites_missing_file():
    # Mock the loader
    with patch("api.main.load_sites") as mock_loader:
        mock_loader.return_value = None

        # call the endpoint
        response = client.get("/sites")

        # 1. Verify that the HTTP status code is 500
        assert response.status_code == 500

        # 2. Verify that the response body equals the expected error details
        assert response.json() == {"detail": "Unable to load site monitoring data"}

        # 3. Verify that the mocked loader was called exactly once
        mock_loader.assert_called_once()

def test_get_sites_invalid_structure():
    # Mock the loader
    with patch("api.main.load_sites") as mock_loader:
        mock_loader.return_value = {
            "site_name": "OULU_BTS_001"
        }

        # call the endpoint
        response = client.get("/sites")

        # Verify that the HTTP status code is 500
        assert response.status_code == 500

        # the response JSON contains the exact message "Site monitoring data must be a list"
        assert response.json() == {"detail":"Site monitoring data must be a list"}

        # verify the loader was called once.
        mock_loader.assert_called_once()

def test_get_summary():
    # make a GET request to /summary
    response = client.get("/summary")

    # Parse json response
    summary = response.json()

    # assert HTTP status == 200
    assert response.status_code == 200

    # assert total_records == 4
    assert summary["total_records"] == 4

    # assert valid_records == 3
    assert summary["valid_records"] == 3

    # assert invalid_records == 1
    assert summary["invalid_records"] == 1

    # assert normal_count == 1
    assert summary["normal_count"] == 1

    # assert warning_count == 1
    assert summary["warning_count"] == 1

    # assert critical_count == 1
    assert summary["critical_count"] == 1

    # check that response does not contain detailed sites or erros
    assert "sites" not in summary
    assert "errors" not in summary

    # report invariants
    assert summary["total_records"] == (
        summary["valid_records"] + summary["invalid_records"]
    )

    assert summary["valid_records"] == (
        summary["normal_count"]
        + summary["warning_count"]
        + summary["critical_count"]
    )
    assert len(summary) == 6


def test_sites_response_validation():

    # patch get_monitoring_report function where endpoint looks it up
    with patch("api.main.get_monitoring_report") as mock_report:
        # Use '=' instead of ':' to assign the return_value
        mock_report.return_value = {
            "sites": [
                {
                    "site_name": "OULU_BTS_001",
                    "utilization": "unknown",
                    "status": "NORMAL",
                }
            ]
        }

        # Step B — Assert the exception
        with pytest.raises(ResponseValidationError):
            client.get("/sites")

        # Step C — Verify the mock was called
        mock_report.assert_called_once()

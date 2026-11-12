from api.schemas import SiteResponse
from pydantic import ValidationError
import pytest

def test_site_response_accepts_utilization_above_100():
    site = SiteResponse(
        site_name="OULU_BTS_001",
        utilization=120.0,
        status="CRITICAL"
    )

    assert site.utilization == 120.0

def test_site_response_rejects_negative_utilization():
    with pytest.raises(ValidationError):
        SiteResponse(
            site_name="OULU_BTS_001",
            utilization=-10.0,
            status="NORMAL"
        )

def test_site_response_rejects_invalid_status():
    with pytest.raises(ValidationError):
        SiteResponse(
            site_name="OULU_BTS_001",
            utilization=50.0,
            status="BROKEN"
        )

def test_site_response_rejects_empty_name():
    with pytest.raises(ValidationError):
        SiteResponse(
            site_name="",
            utilization=60.0,
            status="NORMAL"
        )

def test_site_response_accepts_zero_utilization():
    site = SiteResponse(
        site_name="OULU_BTS_003",
        utilization=0.0,
        status="WARNING"
    )

    assert site.utilization == 0.0

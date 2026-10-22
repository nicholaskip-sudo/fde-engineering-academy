from python_foundations.validation import validate_site
import pytest

def test_valid_site():
    site= {
        "site_name": "OULU_BTS_001",
        "connected_users": 150,
        "maximum_users": 250,
        "is_online": True,
    }

    assert validate_site(site) is True

def test_non_dictionary():
    sites = [
        {
            "site_name": "OULU_BTS_001",
            "connected_users": 150,
            "maximum_users": 250,
            "is_online" : True
        }
    ]
    with pytest.raises(ValueError) as execution_results:
        validate_site(sites)

    assert "ERROR: site must be a dictionary " in str(execution_results.value)

def test_missing_field():
    site= {
        "connected_users": 150,
        "maximum_users": 250,
        "is_online": True,
    }
    with pytest.raises(ValueError) as execution_results:
        validate_site(site)

    assert "Missing required fields" in str(execution_results.value) # .value grabs actual message txt string
    assert "site_name" in str(execution_results.value)

def test_empty_name():
    site= {
        "site_name": "",
        "connected_users": 150,
        "maximum_users": 250,
        "is_online": True,
    }
    with pytest.raises(ValueError) as execution_results:
        validate_site(site)

    assert "Site name must not be empty" in str(execution_results.value)

def test_whitespace_name():
    site= {
        "site_name": "   ",
        "connected_users": 150,
        "maximum_users": 250,
        "is_online": True,
    }
    with pytest.raises(ValueError) as execution_results:
        validate_site(site)

    assert "Site name must not be empty" in str(execution_results.value)

def test_negative_users():
    site= {
        "site_name": "OULU_BTS_001",
        "connected_users": -10,
        "maximum_users": 250,
        "is_online": True,
    }
    with pytest.raises(ValueError) as execution_results:
        validate_site(site)

    assert "Connected users cannot be less than zero" in str(execution_results.value)

def test_zero_capacity():
    site= {
        "site_name": "OULU_BTS_001",
        "connected_users": 150,
        "maximum_users": 0,
        "is_online": True,
    }
    with pytest.raises(ValueError) as execution_results:
        validate_site(site)

    assert "maximum users cannot be zero or negative." in str(execution_results.value)

def test_invalid_online_status():
    site= {
        "site_name": "OULU_BTS_001",
        "connected_users": 150,
        "maximum_users": 250,
        "is_online": "yes",
    }
    with pytest.raises(ValueError) as execution_results:
        validate_site(site)

    assert "Online status must be True or False" in str(execution_results.value)

def test_boolean_user_count():
    site= {
        "site_name": "OULU_BTS_001",
        "connected_users": True,
        "maximum_users": 250,
        "is_online": True,
    }
    with pytest.raises(ValueError) as execution_results:
        validate_site(site)

    assert "connected users must be an integer number" in str(execution_results.value)





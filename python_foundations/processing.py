"""
validate input before processing it, and allow errors to propagate when the caller is responsible for handling them
"""

from python_foundations.validation import validate_site
from python_foundations.calculations import calculate_utilization

def process_site(site, threshold=80):

    validate_site(site)

    utilization = calculate_utilization(site['connected_users'], site['maximum_users'])

    if not site['is_online']:
        status = "CRITICAL"
    elif utilization >= threshold:
        status = "WARNING"
    else:
        status = "NORMAL"

    results = {
        "site_name": site['site_name'],
        "utilization": utilization,
        "status": status
    }

    return results

def main():

    site = {
        "site_name": "OULU_BTS_002",
        "connected_users": 215,
        "maximum_users": 250,
        "is_online": True
    }

    execution_results = process_site(site)

    print(execution_results)


if __name__ == "__main__":
    main()
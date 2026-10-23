from python_foundations.processing import process_site

def process_all_sites(sites):
    processed_sites = []
    normal_count = warning_count = critical_count = invalid_count = 0

    if not isinstance(sites, list):
        raise ValueError("Input data must be a list of dictionaries")

    for site in sites:
        try:
            result = process_site(site)
        except ValueError as error:
            invalid_count += 1  # skip invalid recorsd and increment counter.
            continue

        if result["status"] == "NORMAL":
            normal_count += 1
        elif result["status"] == "WARNING":
            warning_count += 1
        elif result["status"] == "CRITICAL":
            critical_count += 1
        else:
            raise ValueError(f"Unexpected operational status: {result['status']}")

        processed_sites.append(result)

    total_records = len(sites)
    valid_records = normal_count + warning_count + critical_count

    execution_result = {
        "total_records":total_records,
        "valid_records":valid_records,
        "invalid_records":invalid_count,
        "normal_count":normal_count,
        "warning_count":warning_count,
        "critical_count":critical_count,
        "sites":processed_sites
        }
    return execution_result

def main():
    sites = [
        {
        "site_name": "OULU_BTS_001",
        "connected_users": 150,
        "maximum_users": 250,
        "is_online": True
        },
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

    execution_results = process_all_sites(sites)
    print(execution_results)

if __name__ == "__main__":
    main()
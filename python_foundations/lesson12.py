"""
Dictionary comprehension.   -> {key: value for key,value in iteration  condition}
"""
from python_foundations.calculations import calculate_utilization

def main():

    sites = [
        {
            "site_name": "OULU_BTS_001",
            "connected_users": 150,
            "maximum_users": 250
        },
        {
            "site_name": "OULU_BTS_002",
            "connected_users": 225,
            "maximum_users": 250
        },
        {
            "site_name": "OULU_BTS_003",
            "connected_users": 200,
            "maximum_users": 250
        },
        {
            "site_name": "OULU_BTS_004",
            "connected_users": 300,
            "maximum_users": 250
        }
    ]

    utilization_by_site = {site['site_name']:calculate_utilization(site['connected_users'],site['maximum_users']) for site in sites }
    high_utilization_sites = { site_name:utilization for site_name,utilization in utilization_by_site.items()  if utilization >=80.0}

    print("\n ------- UTILIZATION PER SITE-------")
    print(utilization_by_site)
    print("\n -------HIGH UTILIZATION SITES-------")
    print(high_utilization_sites)

    report = {
        "total_records": 3,
        "valid_records": 3,
        "invalid_records": 0,
        "sites": [
            {
                "site_name": "OULU_BTS_001",
                "utilization": 60.0,
                "status": "NORMAL"
            },
            {
                "site_name": "OULU_BTS_002",
                "utilization": 90.0,
                "status": "WARNING"
            },
            {
                "site_name": "OULU_BTS_003",
                "utilization": 80.0,
                "status": "CRITICAL"
            }
        ]
    }

    status_by_site = { site['site_name']:site['status'] for site in report['sites'] }
    print("\n ------- STATUS PER SITE-------")
    print(status_by_site)

    attention_sites = { site['site_name']:site['status'] for site in report['sites'] if site['status'] in ("WARNING", "CRITICAL") }
    print("\n ------- ATTENTION SITES DUE TO STATUS-------")
    print(attention_sites)

    attention_utilization = { site['site_name']:site['utilization'] for site in report['sites']  if site['utilization'] in range(80,100)}
    print("\n ------- ATTENTION SITES DUE TO UTILIZATION-------")
    print(attention_utilization)


if __name__ == "__main__":
    main()
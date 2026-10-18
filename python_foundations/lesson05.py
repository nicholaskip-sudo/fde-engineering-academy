"""
separate the decision-making logic from the presentation logic.
"""
from calculations import calculate_utilization


def main():
    sites = [
        {
            "site_name": "OULU_BTS_001",
            "connected_users": 150,
            "maximum_users": 250,
            "is_online" : True
        },
        {
            "site_name": "OULU_BTS_002",
            "connected_users": 225,
            "maximum_users": 250,
            "is_online" : True
        },
        {
            "site_name": "OULU_BTS_003",
            "connected_users": 200,
            "maximum_users": 250,
            "is_online" : False
        },
        {
            "site_name": "OULU_BTS_004",
            "connected_users": 300,
            "maximum_users": 250,
            "is_online" : True
        }
    ]

    threshold = 80
    print("\n")

    for site in sites:
        utilization = calculate_utilization (site["connected_users"],site["maximum_users"] )

        if not site["is_online"]:
            status = "CRITICAL"
        elif utilization >= threshold:
            status = "WARNING"
        else:
            status = "NORMAL"

        print(f"Site: {site['site_name']}")
        print(f"Utilization: {utilization:.2f}%")
        print(f"Status: {status}\n")

    return

if __name__ == "__main__":
    main()







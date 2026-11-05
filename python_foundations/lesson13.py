"""
Type annotations describe expected types; runtime validation checks actual values.
Type hints: describe what a function expects.
TypeDict: describe expected data structure.
Runtime validation checks whether actual values are acceptable whiole the program runs.
Pyright: static type checker. examines type annotations and reports potential type incompatibilities.
"""

from python_foundations.calculations import calculate_utilization
from typing import TypedDict

class SiteRecord(TypedDict):
    site_name: str
    connected_users: int
    maximum_users: int
    status: str

def get_site_name(site: SiteRecord) -> str:
    return site['site_name']

def is_high_utilization(utilization: float) -> bool:
    return utilization >= 80.0

def get_attention_sites(sites: list[ SiteRecord]) -> list[str]:
    """
    Accepts a list of dictionaries
    """
    return [
        site['site_name']
        for site in sites
        if site['status'].strip() in ('WARNING', 'CRITICAL')
    ]

def main():

    sites: list[SiteRecord] = [

        {
            "site_name": "OULU_BTS_001",
            "connected_users": 150,
            "maximum_users": 250,
            "status": "CRITICAL"
        },
        {
            "site_name": "OULU_BTS_002",
            "connected_users": 225,
            "maximum_users": 250,
            "status": " WARNING"
        }
    ]

    utilization_by_site = {
        site['site_name']:calculate_utilization(site['connected_users'],site['maximum_users'])
        for site in sites
        }

    print(utilization_by_site)

    print("\n ---- Calling functions ---- ")
    print("\n ---- Get site name function ----")
    print(f"The site name is: {get_site_name(sites[1])}")

    print("\n ---- Utilization high function ----")
    print(f"HIGH UTILIZATION status: {is_high_utilization(utilization_by_site['OULU_BTS_001'])}")

    print("\n ---- Get attention sites function ----")
    print(f"ATTENTION SITES: {get_attention_sites(sites)}")

if __name__ == "__main__":
    main()
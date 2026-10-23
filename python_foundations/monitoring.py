"""
separation of concerns.
regression testing during refactoring.
dependency injection
"""

from python_foundations.processing import process_site
from python_foundations.lesson06 import load_sites
from pathlib import Path

def main(json_path=None): # dependency injection

    if json_path is None:
        project_root = Path(__file__).resolve().parent.parent
        json_path = project_root / "data" / "sites.json"

    sites = load_sites(json_path)

    if sites is None:
        print("Unable to continue: data loading failed\n")
        return

    if not isinstance(sites, list):
        raise ValueError("Input data must be a list of dictionaries")

    normal_count = warning_count = critical_count = invalid_count = 0

    for site in sites:
        try:
            result = process_site(site)
        except ValueError as error:
            print(f"Invalid record : {error}")
            invalid_count += 1
            continue

        if result["status"] == "NORMAL":
            normal_count += 1
        elif result["status"] == "WARNING":
            warning_count += 1
        elif result["status"] == "CRITICAL":
            critical_count += 1
        else:
            raise ValueError(f"Unexpected operational status: {result['status']}")

        print("\n ---------PRINTING SITE DETAILS-------------")
        print(f"Site name:                 {result['site_name']}")
        print(f"Utilization:               {result['utilization']:.2f}%")
        print(f"Operational status:        {result["status"]}\n")

    total_records = len(sites)
    valid_records = normal_count + warning_count + critical_count

    print("\n ---------COUNTERS SUMMARY-------------")
    print(f"TOTAL RECORD:       {total_records}")
    print(f"VALID RECORD:       {valid_records}\n")
    print(f"Invalid count:      {invalid_count}")
    print(f"Normal count:       {normal_count}")
    print(f"Warning count:      {warning_count}")
    print(f"Critical count:     {critical_count}")

if __name__ == "__main__":
    main()

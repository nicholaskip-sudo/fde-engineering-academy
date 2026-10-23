"""
separation of concerns.
regression testing during refactoring.
dependency injection
"""

from python_foundations.reporting import process_all_sites
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

    results = process_all_sites(sites)

    for site in results['sites']:
        print("\n ---------PRINTING SITE DETAILS-------------")
        print(f"Site name:            {site['site_name']}")
        print(f"Utilization:          {site['utilization']:.2f}%")
        print(f"Operational status:   {site["status"]}\n")

    print(f"TOTAL RECORD:          {results['total_records']}")
    print(f"VALID RECORDS:         {results['valid_records']}")
    print(f"INVALID RECORDS:       {results['invalid_records']}")
    print(f"NORMAL RECORDS:        {results['normal_count']}")
    print(f"WARNING RECORDS:       {results['warning_count']}")
    print(f"CRITICAL RECORDS:      {results['critical_count']}")

if __name__ == "__main__":
    main()

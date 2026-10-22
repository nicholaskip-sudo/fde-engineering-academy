from python_foundations.calculations import calculate_utilization
from python_foundations.validation import validate_site
from python_foundations.lesson06 import load_sites
from pathlib import Path


def main(json_path=None):

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

    threshold = 80

    for site in sites:
        try:
            validate_site(site)
        except ValueError as error:
            print(f"Invalid record : {error}")
            invalid_count += 1
            continue

        utilization = calculate_utilization(site["connected_users"],site["maximum_users"] )

        if not site['is_online']:
            critical_count += 1
            status = "CRITICAL"
        elif utilization >= threshold:
            warning_count += 1
            status = "WARNING"
        else:
            normal_count +=1
            status="NORMAL"

        print("\n ---------PRINTING SITE DETAILS-------------")
        print(f"Site name:                 {site['site_name']}")
        print(f"Connected users:           {site['connected_users']}")
        print(f"Maximum users:             {site['maximum_users']}")
        print(f"Site online status:        {site['is_online']}")
        print(f"Utilization:               {utilization:.2f}%")
        print(f"Operational status:        {status}\n")

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

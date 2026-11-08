"""
converting data and validating business rules are separate responsibilities.
"""
import csv
import json
from pathlib import Path
from python_foundations.reporting import process_all_sites

def load_csv_sites(csv_path: Path) -> list[dict[str,str]]:

    try:
        with open(csv_path, "r", encoding="utf-8", newline="") as file:
            reader = csv.DictReader(file)

            return list(reader)

    except FileNotFoundError:
        print(f"ERROR: The file at {csv_path} was not found")
        return []

def parse_boolean(value: str) -> bool:
    normalized = value.strip().lower()

    if normalized == "true":
        return True

    if normalized == "false":
        return False

    raise ValueError("Invalid boolean value")

def convert_csv_site(row: dict[str, str]) -> dict:

    required_fields = (
        "site_name",
        "connected_users",
        "maximum_users",
        "is_online"
    )

    for field in required_fields:
        if field not in row or row[field] is None:
            raise ValueError(f"Missing required field: {field}")

    site_name = row["site_name"].strip()

    if not site_name:
        raise ValueError("Invalid CSV record:site name cannot be blank")

    try:
        connected_users = int(row["connected_users"].strip())
    except ValueError as error:
        raise ValueError(
            f"Invalid csv record for {site_name}: connected_users must be an integer"
        ) from error # preserves original exception as the cause i.e. stack trace

    try:
        maximum_users = int(row["maximum_users"].strip())
    except ValueError as error:
        raise ValueError (
            f"Invalid csv record for {site_name}: maximum_users must be an integer"
        ) from error

    try:
        is_online = parse_boolean(row["is_online"])
    except ValueError as error:
        raise ValueError(
            f"Invalid csv record for {site_name}: is_online must be a boolean value"
        ) from error

    return {
        "site_name": site_name,
        "connected_users": connected_users,
        "maximum_users": maximum_users,
        "is_online": is_online
    }

def convert_all_csv_sites(rows: list[dict[str,str]]) -> dict:

    converted_sites = []
    conversion_errors = []

    for row in rows:
        try:
            site = convert_csv_site(row)
            converted_sites.append(site)
        except ValueError as error:
            conversion_errors.append (
                {
                    "site_name": row.get("site_name") or "UNKNOWN",
                    "reason": str(error)
                }
            )

    return {
        "converted_sites": converted_sites,
        "conversion_errors": conversion_errors
    }

def process_csv_report(rows: list[dict[str, str]]) -> dict:

    conversion_results = convert_all_csv_sites(rows)

    monitoring_report = process_all_sites(
        conversion_results['converted_sites']
        )

    return {
        'total_records': len(rows),
        'valid_records': monitoring_report['valid_records'],
        'invalid_records': (
            monitoring_report['invalid_records']
            + len(conversion_results['conversion_errors'])
        ),
        'sites': monitoring_report['sites'],
        'errors': (
            conversion_results["conversion_errors"]
            + monitoring_report['errors']
        )
    }

def main():

    file_path = Path('data') / "sites.csv"

    sites = load_csv_sites(file_path)


    execution_results = process_csv_report(sites)

    print(json.dumps(execution_results, indent=4))

if __name__ == "__main__":
    main()

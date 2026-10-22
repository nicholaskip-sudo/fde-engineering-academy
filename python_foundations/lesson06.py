import json
from pathlib import Path

def load_sites(json_path):
    print(f"\nLooking for JSON file at: {json_path}")
    print(f"File exists: {json_path.exists()}")

    try:
        with open(json_path, "r", encoding="utf-8") as file:
            sites= json.load(file)
            return sites
    except FileNotFoundError:
        print("ERROR: JSON file not found.")
        return None
    except json.JSONDecodeError:
        print("ERROR: Invalid JSON format.")
        return None

def main():
    project_root = Path(__file__).resolve().parent.parent
    json_path = project_root / "data" / "sites.json"

    sites = load_sites(json_path)

    if sites is None:
        print("Unable to continue: data loading failed")
        return

    print("\n--------------PARSING JSON FILE---------------")

    print(f"The total number of sites: {len(sites)}\n")

    for site in sites:
        try:
            if site.get("site_name") is None:
                print("Skipping record: site name is missing or null.\n")
                continue # skip current iteration

            print(f"Site name:         {site['site_name']}")
            print(f"Connected users:   {site['connected_users']}")
            print(f"Maximum users:     {site['maximum_users']}\n")

        except KeyError as error:
            print(f"ERROR: Missing required field: {error}\n")

if __name__ == "__main__":
    main()






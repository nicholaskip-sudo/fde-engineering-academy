
import json
from python_foundations.lesson06 import load_sites

def test_valid_json_loading(tmp_path):
    file_path = tmp_path / "sites.json"

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
        }
    ]

    file_path.write_text(json.dumps(sites), encoding="utf-8")

    loaded = load_sites(file_path)

    assert loaded==sites


def test_empty_json_array(tmp_path):
    file_path = tmp_path / "empty.json"

    empty = []

    file_path.write_text(json.dumps(empty), encoding="utf-8")

    loaded = load_sites(file_path)

    assert loaded == empty

def test_missing_file(tmp_path):
    file_path = tmp_path / "this_file_is_non-existing.json"

    loaded = load_sites(file_path)

    assert loaded is None

def test_malformed_json_file(tmp_path):
    file_path = tmp_path / "malformed.json"

    invalid_json_text = '{"site_name": "OULU_BTS_001", "connected_users": 150' # missing closing bracket

    file_path.write_text(invalid_json_text, encoding="utf-8")

    loaded = load_sites(file_path)

    assert loaded is None






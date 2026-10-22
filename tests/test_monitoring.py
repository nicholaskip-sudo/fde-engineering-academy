import json
from python_foundations.monitoring import main

def test_missing_monitoring_file(tmp_path,capsys):
    file_path = tmp_path / "non_existent.json"

    main(file_path)

    captured = capsys.readouterr()

    assert "Unable to continue: data loading failed" in captured.out


def test_successful_monitoring(tmp_path,capsys):
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
    file_path = tmp_path / "success.json"
    file_path.write_text(json.dumps(sites), encoding="utf-8")
    main(file_path)
    captured= capsys.readouterr()

    assert "OULU_BTS_001" in captured.out
    assert "OULU_BTS_002" in captured.out
    assert "60.00" in captured.out
    assert "90.00" in captured.out
    assert "NORMAL" in captured.out
    assert "WARNING" in captured.out
    assert "INVALID" not in captured.out
    assert "VALID RECORD:       2" in captured.out
    assert "Invalid count:      0" in captured.out


def test_mixed_valid_invalid_records(tmp_path,capsys):
    file_path = tmp_path / "mixed_valid_invalid.json"
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
            "connected_users": -10,
            "maximum_users": 250,
            "is_online" : True
        }
    ]
    file_path.write_text(json.dumps(sites), encoding="utf-8")
    main(file_path)
    captured= capsys.readouterr()
    output_lines = [" ".join(line.split()) for line in captured.out.splitlines()]

    assert "OULU_BTS_001" in captured.out
    assert "OULU_BTS_002" in captured.out
    assert "OULU_BTS_003" in captured.out
    assert "OULU_BTS_004" not in captured.out
    assert "60.00" in captured.out
    assert "90.00" in captured.out
    assert "80.00" in captured.out
    assert "NORMAL" in captured.out
    assert "WARNING" in captured.out
    assert "CRITICAL" in captured.out
    assert "Invalid" in captured.out
    assert "Invalid record : ERROR: Connected users cannot be less than zero" in captured.out
    assert "TOTAL RECORD: 4" in output_lines
    assert "VALID RECORD: 3" in output_lines
    assert "Invalid count: 1" in output_lines
    assert "Normal count: 1" in output_lines
    assert "Warning count: 1" in output_lines
    assert "Critical count: 1" in output_lines


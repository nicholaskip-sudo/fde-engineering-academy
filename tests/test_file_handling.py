from python_foundations.lesson14 import write_log, append_log, read_log, display_log
from pathlib import Path
import pytest

def test_write_log(tmp_path: Path):

    log_path = tmp_path / "test_monitoring_log.txt"

    records = [
        "OULU_BTS_001: NORMAL",
        "OULU_BTS_002: WARNING"
    ]
    write_log(log_path, records)

    assert log_path.exists() # verify file existence.
    assert read_log(log_path) == records # verify that reading returns original two records.

def test_append_log(tmp_path: Path):

    log_path = tmp_path / "test_monitoring_log.txt"
    inititial_record = ["OULU_BTS_003: CRITICAL"]

    write_log(log_path, inititial_record) # start with a file containing one record.

    append_log(log_path, "OULU_BTS_002: WARNING")
    append_log(log_path, "OULU_BTS_001: NORMAL")

    assert log_path.exists() # verify existence

    expected_records = [
        "OULU_BTS_003: CRITICAL",
        "OULU_BTS_002: WARNING",
        "OULU_BTS_001: NORMAL"
    ]
    assert read_log(log_path) == expected_records

def test_read_empty_file(tmp_path):

    log_path = tmp_path / "test_empty_log.txt"
    log_path.touch()

    assert read_log(log_path) == []

def test_overwrite_log(tmp_path):

    log_file = tmp_path / "test_overwrite.txt"

    records = [
        "OULU_BTS_001: NORMAL",
        "OULU_BTS_002: WARNING"
    ]
    write_log(log_file, records)
    replacement_record = ["OULU_BTS_003: CRITICAL"]
    write_log(log_file, replacement_record) # truncates existing contents

    assert read_log(log_file) == replacement_record

def test_missing_file(tmp_path):

    log_file = tmp_path / "non-existent_log.txt"

    assert not log_file.exists()
    assert read_log(log_file) == []
    assert not log_file.exists()

def test_read_directory_raises_error(tmp_path, capsys):

    directory_path = tmp_path / "directory_instead_of_file"
    directory_path.mkdir()

    with pytest.raises(IsADirectoryError):
        read_log(directory_path)

def test_display_missing_log(tmp_path, capsys):

    file_path = tmp_path / "non-existent_log.txt"

    assert not file_path.exists()
    display_log(file_path)

    captured = capsys.readouterr()

    assert "No log records found" in captured.out

def test_display_directory_error(tmp_path, capsys):

    directory_path = tmp_path / "test_directory"
    directory_path.mkdir()
    display_log(directory_path)

    captured = capsys.readouterr()

    assert "ERROR: The supplied log path is a directory, not a file." in captured.out

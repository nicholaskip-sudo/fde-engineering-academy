from pathlib import Path

def write_log(log_path: Path, records: list[str]) -> None:
    """ Safely creates directories and writes log records to a file"""
    log_path.parent.mkdir(parents=True, exist_ok=True)

    with log_path.open("w", encoding="utf-8") as file:
        for record in records:
            clean_record = record if record.endswith("\n") else f"{record}\n"
            file.write(clean_record)

def append_log(log_path: Path, record: str) -> None:
    """ Open file in append mode and add record with newline"""
    log_path.parent.mkdir(parents=True, exist_ok=True)

    with log_path.open("a", encoding="utf-8") as file:
        clean_record = record if record.endswith("\n") else f"{record}\n"
        file.write(clean_record)

def read_log (log_path: Path) -> list[str]:
    """ Read a file and return its lines as a list of strings without newline characters"""

    try:
        with log_path.open("r", encoding="utf-8") as file:
            contents = file.read()
            lines_list = contents.splitlines() # converts into a list

            return lines_list
    except FileNotFoundError:
        return []

def display_log(log_path: Path) -> None:
    try:
        file_contents = read_log(log_path)
        if file_contents:
            print("\n---- Parsed File Contents ----")
            print(f"\n{file_contents}")
            print(f"The total count of logs in file: {len(file_contents)}")
        else:
            print("No log records found")
    except IsADirectoryError:
        print("ERROR: The supplied log path is a directory, not a file.")


def main():

    log_path = Path("data") / "monitoring_log.txt"

    records = [
        "OULU_BTS_001: NORMAL",
        "OULU_BTS_002: WARNING"
    ]

    # call to write log
    write_log(log_path, records)

    # call to append log
    append_log(log_path, "OULU_BTS_003: CRITICAL")

    # call to display_log(log_path)
    display_log(log_path)

if __name__ == "__main__":
    main()

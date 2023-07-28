import csv
import glob
from typing import List


def list_files(path: str) -> List[str]:
    return glob.glob(path, recursive=True)


def read_csv_as_dict(file_url, encoding="UTF-8", skip_rows=0, delimiter=";"):
    transactions = []
    with open(file_url, "r", encoding=encoding) as f:
        for i in range(skip_rows):
            next(f)
        for row in csv.DictReader(f, delimiter=delimiter):
            transactions.append({**row, "file_url": file_url})
    return transactions


def read_files_into_dict(path: str, skip_lines: int = 0, encoding: str = "utf-8") -> List[dict]:
    data = []
    for file in list_files(path=path):
        data += read_csv_as_dict(file_url=file, encoding=encoding, skip_rows=skip_lines)

    return data


def load_norisbank():
    pass


def load_vblh():
    pass

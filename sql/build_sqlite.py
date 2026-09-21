"""Build the local SQLite practice database from the synthetic Excel lab."""

from __future__ import annotations

import csv
from datetime import datetime, timedelta
import sqlite3
import zipfile
from pathlib import Path
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
WORKBOOK = ROOT / "water_prep_excel_lab.xlsx"
DATABASE = ROOT / "sql" / "cloud_billing.db"
CSV_FILE = ROOT / "data" / "cloud_billing.csv"
NS = {"x": "http://schemas.openxmlformats.org/spreadsheetml/2006/main"}


def read_shared_strings(archive: zipfile.ZipFile) -> list[str]:
    if "xl/sharedStrings.xml" not in archive.namelist():
        return []
    root = ET.fromstring(archive.read("xl/sharedStrings.xml"))
    return ["".join(node.text or "" for node in item.findall(".//x:t", NS)) for item in root.findall("x:si", NS)]


def cell_value(cell: ET.Element, shared_strings: list[str]) -> str:
    value = cell.find("x:v", NS)
    if cell.get("t") == "inlineStr":
        return "".join(node.text or "" for node in cell.findall(".//x:t", NS))
    if value is None:
        return ""
    if cell.get("t") == "s":
        return shared_strings[int(value.text)]
    return value.text or ""


def column_index(reference: str) -> int:
    letters = "".join(character for character in reference if character.isalpha())
    index = 0
    for letter in letters:
        index = index * 26 + ord(letter.upper()) - ord("A") + 1
    return index - 1


def optional_float(value: str) -> float | None:
    return float(value) if value else None


def optional_int(value: str) -> int | None:
    return int(float(value)) if value else None


def excel_date(value: str) -> str:
    return (datetime(1899, 12, 30) + timedelta(days=float(value))).date().isoformat()


def read_raw_billing() -> tuple[list[str], list[list[str]]]:
    with zipfile.ZipFile(WORKBOOK) as archive:
        shared_strings = read_shared_strings(archive)
        root = ET.fromstring(archive.read("xl/worksheets/sheet1.xml"))
        rows: list[list[str]] = []
        for row in root.findall(".//x:sheetData/x:row", NS):
            values = [""] * 16
            for cell in row.findall("x:c", NS):
                values[column_index(cell.get("r", "A1"))] = cell_value(cell, shared_strings)
            if values[0] and values[0] != "month":
                values[0] = excel_date(values[0])
            rows.append(values)
    return rows[0], rows[1:]


def main() -> None:
    headers, rows = read_raw_billing()
    expected_headers = [
        "month", "cloud_provider", "account", "business_unit", "cost_center",
        "chargeback_owner", "environment", "service", "resource_id", "region",
        "owner", "usage_hours", "monthly_cost", "cpu_utilization_pct", "storage_gb",
        "tags_complete",
    ]
    if headers != expected_headers:
        raise ValueError(f"Unexpected Raw Billing headers: {headers}")
    if len(rows) != 540:
        raise ValueError(f"Expected 540 synthetic records, found {len(rows)}")

    CSV_FILE.parent.mkdir(exist_ok=True)
    with CSV_FILE.open("w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(headers)
        writer.writerows(rows)

    if DATABASE.exists():
        DATABASE.unlink()
    connection = sqlite3.connect(DATABASE)
    try:
        connection.execute("""
            CREATE TABLE cloud_billing (
                month TEXT NOT NULL, cloud_provider TEXT NOT NULL, account TEXT NOT NULL,
                business_unit TEXT NOT NULL, cost_center TEXT, chargeback_owner TEXT NOT NULL,
                environment TEXT NOT NULL, service TEXT NOT NULL, resource_id TEXT NOT NULL,
                region TEXT NOT NULL, owner TEXT, usage_hours INTEGER,
                monthly_cost REAL NOT NULL, cpu_utilization_pct REAL,
                storage_gb INTEGER, tags_complete TEXT NOT NULL
            )
        """)
        typed_rows = [
            (row[0], row[1], row[2], row[3], row[4] or None, row[5], row[6], row[7],
             row[8], row[9], row[10] or None, optional_int(row[11]), float(row[12]),
             optional_float(row[13]), optional_int(row[14]), row[15])
            for row in rows
        ]
        connection.executemany(
            "INSERT INTO cloud_billing VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
            typed_rows,
        )
        connection.execute("CREATE INDEX idx_billing_month ON cloud_billing(month)")
        connection.execute("CREATE INDEX idx_billing_environment ON cloud_billing(environment)")
        record_count, total_cost = connection.execute(
            "SELECT COUNT(*), ROUND(SUM(monthly_cost), 2) FROM cloud_billing"
        ).fetchone()
        connection.commit()
    finally:
        connection.close()

    print(f"Created {DATABASE.relative_to(ROOT)} with {record_count} synthetic records.")
    print(f"Wrote {CSV_FILE.relative_to(ROOT)}. Total monthly cost: ${total_cost:,.2f}")


if __name__ == "__main__":
    main()

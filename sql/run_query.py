"""A small read-only SQLite prompt for the Cloud Billing SQL lab."""

from __future__ import annotations

import sqlite3
from pathlib import Path

DATABASE = Path(__file__).with_name("cloud_billing.db")
MAX_DISPLAY_ROWS = 50
ALLOWED_PREFIXES = ("select", "with", "pragma", "explain")


def print_rows(cursor: sqlite3.Cursor) -> None:
    columns = [description[0] for description in cursor.description or []]
    rows = cursor.fetchmany(MAX_DISPLAY_ROWS + 1)
    if not columns:
        print("Query completed.")
        return
    widths = [len(column) for column in columns]
    for row in rows[:MAX_DISPLAY_ROWS]:
        widths = [max(width, len("" if value is None else str(value))) for width, value in zip(widths, row)]
    print(" | ".join(column.ljust(width) for column, width in zip(columns, widths)))
    print("-+-".join("-" * width for width in widths))
    for row in rows[:MAX_DISPLAY_ROWS]:
        print(" | ".join(("" if value is None else str(value)).ljust(width) for value, width in zip(row, widths)))
    if len(rows) > MAX_DISPLAY_ROWS:
        print(f"Showing first {MAX_DISPLAY_ROWS} rows.")


def main() -> None:
    if not DATABASE.exists():
        raise SystemExit("Database missing. Run: python sql/build_sqlite.py")
    print("Cloud Billing SQL Lab - type a SELECT query, or 'exit' to leave.")
    print("Try: SELECT cloud_provider, monthly_cost FROM cloud_billing LIMIT 5;")
    connection = sqlite3.connect(DATABASE)
    try:
        while True:
            try:
                query = input("sql> ").strip()
            except (EOFError, KeyboardInterrupt):
                print()
                break
            if query.lower() in {"exit", "quit", ".exit", ".quit"}:
                break
            if not query:
                continue
            if not query.lower().startswith(ALLOWED_PREFIXES):
                print("Read-only lab: start with SELECT, WITH, PRAGMA, or EXPLAIN.")
                continue
            try:
                print_rows(connection.execute(query))
            except sqlite3.Error as error:
                print(f"SQL error: {error}")
    finally:
        connection.close()


if __name__ == "__main__":
    main()

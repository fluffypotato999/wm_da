"""Walmart sales analysis using SQLite.

Loads Walmart weekly sales data into SQLite and queries
the top 5 stores by total sales across all weeks.
"""

import csv
import sqlite3
from typing import Iterator


DATA_PATH = "/Users/fluffy/code/data/walmart/Walmart.csv"
DB_PATH = ":memory:"


def create_connection(db_path: str) -> sqlite3.Connection:
    """Create and return a SQLite connection.

    Args:
        db_path: Path to the SQLite database file, or ':memory:'.

    Returns:
        A sqlite3.Connection instance.
    """
    return sqlite3.connect(db_path)


def create_table(conn: sqlite3.Connection) -> None:
    """Create the sales table if it does not exist.

    Args:
        conn: An active SQLite connection.
    """
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS sales (
            store       INTEGER,
            date        TEXT,
            weekly_sales REAL,
            holiday_flag INTEGER,
            temperature  REAL,
            fuel_price   REAL,
            cpi          REAL,
            unemployment REAL
        )
        """
    )
    conn.commit()


def read_csv_rows(path: str) -> Iterator[tuple]:
    """Yield rows from the Walmart CSV as tuples.

    Skips the header row.

    Args:
        path: Path to the CSV file.

    Yields:
        A tuple of (store, date, weekly_sales, holiday_flag,
        temperature, fuel_price, cpi, unemployment).
    """
    with open(path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            yield (
                int(row["Store"]),
                row["Date"],
                float(row["Weekly_Sales"]),
                int(row["Holiday_Flag"]),
                float(row["Temperature"]),
                float(row["Fuel_Price"]),
                float(row["CPI"]),
                float(row["Unemployment"]),
            )


def load_data(conn: sqlite3.Connection, path: str) -> int:
    """Load CSV data into the sales table.

    Args:
        conn: An active SQLite connection.
        path: Path to the CSV file.

    Returns:
        Number of rows inserted.
    """
    rows = list(read_csv_rows(path))
    conn.executemany(
        """
        INSERT INTO sales
            (store, date, weekly_sales, holiday_flag,
             temperature, fuel_price, cpi, unemployment)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """,
        rows,
    )
    conn.commit()
    return len(rows)


def query_top_stores(conn: sqlite3.Connection, n: int = 5) -> list[tuple]:
    """Query the top N stores by total weekly sales.

    Args:
        conn: An active SQLite connection.
        n: Number of top stores to return.

    Returns:
        A list of (store, total_sales) tuples ordered descending by total_sales.
    """
    cursor = conn.execute(
        """
        SELECT store, SUM(weekly_sales) AS total_sales
        FROM sales
        GROUP BY store
        ORDER BY total_sales DESC
        LIMIT ?
        """,
        (n,),
    )
    return cursor.fetchall()


def format_results(results: list[tuple]) -> str:
    """Format query results as a readable string.

    Args:
        results: List of (store, total_sales) tuples.

    Returns:
        A formatted string representation of the results.
    """
    header = f"{'Rank':<6}{'Store':<10}{'Total Sales':>20}"
    separator = "-" * len(header)
    rows = "\n".join(
        f"{rank:<6}{store:<10}{sales:>20,.2f}"
        for rank, (store, sales) in enumerate(results, start=1)
    )
    return "\n".join([header, separator, rows])


def main() -> None:
    """Run the Walmart sales analysis pipeline."""
    conn = create_connection(DB_PATH)
    create_table(conn)

    row_count = load_data(conn, DATA_PATH)
    print(f"Loaded {row_count:,} rows into SQLite.\n")

    top_stores = query_top_stores(conn, n=5)
    print("Top 5 Stores by Total Sales\n")
    print(format_results(top_stores))

    conn.close()


if __name__ == "__main__":
    main()

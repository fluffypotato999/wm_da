"""Walmart sales analysis using SQLite.

Loads Walmart weekly sales and store metadata into SQLite and queries
the top 5 stores by total sales across all weeks.
"""

import csv
import sqlite3
from typing import Iterator


SALES_DATA_PATH = "/Users/fluffy/code/data/walmart/Walmart.csv"
STORES_DATA_PATH = "/Users/fluffy/code/data/walmart/stores.csv"
DB_PATH = ":memory:"


def create_connection(db_path: str) -> sqlite3.Connection:
    """Create and return a SQLite connection.

    Args:
        db_path: Path to the SQLite database file, or ':memory:'.

    Returns:
        A sqlite3.Connection instance.
    """
    return sqlite3.connect(db_path)


def create_tables(conn: sqlite3.Connection) -> None:
    """Create the sales and stores tables if they do not exist.

    Args:
        conn: An active SQLite connection.
    """
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS sales (
            store        INTEGER,
            date         TEXT,
            weekly_sales REAL,
            holiday_flag INTEGER,
            temperature  REAL,
            fuel_price   REAL,
            cpi          REAL,
            unemployment REAL
        )
        """
    )
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS stores (
            store INTEGER PRIMARY KEY,
            type  TEXT,
            size  INTEGER
        )
        """
    )
    conn.commit()


def read_sales_rows(path: str) -> Iterator[tuple]:
    """Yield rows from the Walmart sales CSV as tuples.

    Args:
        path: Path to the sales CSV file.

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


def read_stores_rows(path: str) -> Iterator[tuple]:
    """Yield rows from the Walmart stores CSV as tuples.

    Args:
        path: Path to the stores CSV file.

    Yields:
        A tuple of (store, type, size).
    """
    with open(path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            yield (
                int(row["Store"]),
                row["Type"],
                int(row["Size"]),
            )


def load_sales(conn: sqlite3.Connection, path: str) -> int:
    """Load sales CSV data into the sales table.

    Args:
        conn: An active SQLite connection.
        path: Path to the sales CSV file.

    Returns:
        Number of rows inserted.
    """
    rows = list(read_sales_rows(path))
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


def load_stores(conn: sqlite3.Connection, path: str) -> int:
    """Load stores CSV data into the stores table.

    Args:
        conn: An active SQLite connection.
        path: Path to the stores CSV file.

    Returns:
        Number of rows inserted.
    """
    rows = list(read_stores_rows(path))
    conn.executemany(
        "INSERT INTO stores (store, type, size) VALUES (?, ?, ?)",
        rows,
    )
    conn.commit()
    return len(rows)


def query_top_stores(conn: sqlite3.Connection, n: int = 5) -> list[tuple]:
    """Query the top N stores by total weekly sales, joined with store metadata.

    Args:
        conn: An active SQLite connection.
        n: Number of top stores to return.

    Returns:
        A list of (store, type, size, total_sales_millions) tuples
        ordered descending by total_sales.
    """
    cursor = conn.execute(
        """
        SELECT
            s.store,
            st.type,
            st.size,
            ROUND(SUM(s.weekly_sales) / 1000000.0, 2) AS total_sales_millions
        FROM sales s
        JOIN stores st ON s.store = st.store
        GROUP BY s.store
        ORDER BY total_sales_millions DESC
        LIMIT ?
        """,
        (n,),
    )
    return cursor.fetchall()


def format_results(results: list[tuple]) -> str:
    """Format query results as a readable string.

    Args:
        results: List of (store, type, size, total_sales_millions) tuples.

    Returns:
        A formatted string representation of the results.
    """
    header = f"{'Rank':<6}{'Store':<8}{'Type':<8}{'Size (sqft)':>14}{'Total Sales ($M)':>18}"
    separator = "-" * len(header)
    rows = "\n".join(
        f"{rank:<6}{store:<8}{stype:<8}{size:>14,}{sales:>18.2f}"
        for rank, (store, stype, size, sales) in enumerate(results, start=1)
    )
    return "\n".join([header, separator, rows])


def main() -> None:
    """Run the Walmart sales analysis pipeline."""
    conn = create_connection(DB_PATH)
    create_tables(conn)

    sales_count = load_sales(conn, SALES_DATA_PATH)
    stores_count = load_stores(conn, STORES_DATA_PATH)
    print(f"Loaded {sales_count:,} sales rows and {stores_count} store records.\n")

    top_stores = query_top_stores(conn, n=5)
    print("Top 5 Stores by Total Sales\n")
    print(format_results(top_stores))

    conn.close()


if __name__ == "__main__":
    main()

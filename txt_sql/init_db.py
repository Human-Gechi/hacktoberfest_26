import sqlite3
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parents[1]
EXAMPLE_DIR = ROOT_DIR / "examples"
SQL_PATH = EXAMPLE_DIR / "init.sql"
DB_PATH = EXAMPLE_DIR / "sample.db"


def init_database():
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)

    if not SQL_PATH.exists():
        raise FileNotFoundError(f"SQL file not found at: {SQL_PATH}")

    sql_script = SQL_PATH.read_text(encoding="utf-8")

    print(f"Initializing database at: {DB_PATH}")
    with sqlite3.connect(DB_PATH) as conn:
        conn.executescript(sql_script)

        cursor = conn.cursor()
        tables = ["customers", "orders", "students"]
        for table in tables:
            cursor.execute(f"SELECT COUNT(*) FROM {table}")
            count = cursor.fetchone()[0]
            print(f" - Table '{table}': {count} rows")

    print("Database successfully initialized!")


if __name__ == "__main__":
    init_database()

import sqlite3
import time

from txt_sql.config import settings


def run(
    sql,
    db_path,
    timeout=settings.timeout_s,
    max_rows=settings.max_rows,
):
    conn = sqlite3.connect(f"file:{db_path}?mode=ro", uri=True)
    conn.execute("PRAGMA query_only = ON")

    start = time.time()
    try:
        cur = conn.execute(sql)
        columns = [c[0] for c in cur.description]
        rows = [list(row) for row in cur.fetchmany(max_rows)]

        if len(rows) > max_rows:
            raise RuntimeError("Result too large")

        duration = time.time() - start
    except Exception as e:
        duration = time.time() - start
        raise type(e)(str(e) + f" [spent {duration:.3f}s]")
    finally:
        conn.close()

    return columns, rows

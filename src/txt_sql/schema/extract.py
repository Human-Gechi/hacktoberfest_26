import sqlite3


def extract_tables(db_path):
    conn = sqlite3.connect(f"file:{db_path}?mode=ro", uri=True)
    cur = conn.cursor()

    schema = {}
    query = """
            SELECT 
                name 
            from sqlite_schema 
            WHERE type='table'
            AND name != "sqlite_sequence"
            """

    for (name, ) in cur.execute(query).fetchall():
        columns = [{"name": r[1], "type": r[2], "pk": r[5]}for r in cur.execute(f"PRAGMA table_info({name})")]
        foreign_keys = [{"from": r[3], "to": r[4], "table": r[2]} for r in cur.execute(f"PRAGMA foreign_key_list({name})")]
        schema[name] = {"columns": columns, "foreign_keys": foreign_keys}
    return schema
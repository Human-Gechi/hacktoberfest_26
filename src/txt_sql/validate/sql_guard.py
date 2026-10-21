import sqlglot

def clean_sql():
    pass

def validate(sql, allowed_tables, dialect="sqlite", max_rows=200):
    try:
        parsed = sqlglot.parse_one(sql, read=dialect)
    except sqlglot.errors.ParseError as e:
        raise ValueError(f"Invalid SQL syntax: {e}")
    
    if not isinstance(parsed, sqlglot.exp.Select):
        raise ValueError("Only SELECT queries are allowed")
    

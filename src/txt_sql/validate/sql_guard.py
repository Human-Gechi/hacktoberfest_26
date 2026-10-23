import re

import sqlglot
from sqlglot import exp, parse_one


def clean_sql(response: str) -> str:
    response = re.sub(r"<think>.*?</think>", "", response, flags=re.DOTALL)
    response = re.sub(r"```(?:sql)?\s*\n?(.*?)```", r"\1", response, flags=re.DOTALL)
    return response.strip().rstrip(";")


def validate(sql, allowed_tables, dialect="sqlite", max_rows=200):
    try:
        parsed = parse_one(sql, read=dialect)
    except sqlglot.errors.ParseError as e:
        raise ValueError(f"Invalid SQL syntax: {e}")

    if not isinstance(parsed, (exp.Select, exp.Union)):
        raise TypeError("Only SELECT queries are allowed")

    cte_names = set()
    for cte in parsed.find_all(exp.CTE):
        cte_names.add(cte.alias.lower())

    tables_used = {t.name.lower() for t in parsed.find_all(exp.Table)}
    allowed = {t.lower() for t in allowed_tables}
    unauthorized = tables_used - allowed - cte_names

    if unauthorized:
        raise ValueError(f"Access denied for table(s): {unauthorized}")

    if not parsed.find(exp.Limit):
        parsed = parsed.limit(max_rows)

    return parsed.sql(pretty=True)

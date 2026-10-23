def format_schema(schema):
    for tables, info in schema.items():
        columns = info["columns"]
        foreign_keys = info["foreign_keys"]

        columns_str = ", ".join(
            col["name"] + " " + col["type"] + " " + ("PRIMARY KEY" if col["pk"] else "")
            for col in columns
        )
        fk_str = " ".join(
            f'FOREIGN KEY (" {fk["from"]}") REFERENCES "{fk["table"]}"("{fk["to"]}")'
            for fk in foreign_keys
        )

        return f"""CREATE TABLE "{tables}" ({columns_str} {fk_str})"""

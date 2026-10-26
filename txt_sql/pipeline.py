import json
from pathlib import Path

from txt_sql.config import settings
from txt_sql.execute.runner import run
from txt_sql.llm.ollama import OllamaLLM
from txt_sql.schema.extract import extract_tables
from txt_sql.schema.format import format_schema
from txt_sql.validate.sql_guard import clean_sql, validate

PROMPTS = Path(__file__).parent / "prompts"


class Pipeline:
    def __init__(
        self,
    ):
        self.settings = settings
        self.llm = OllamaLLM()
        self.schema = extract_tables(db_path=self.settings.db_path)
        self.tables = set(self.schema)
        self.formatted = format_schema(schema=self.schema)
        self.schema_text = self.formatted
        self.template = (PROMPTS / "system.txt").read_text()
        lines = (PROMPTS / "examples.jsonl").read_text().splitlines()
        self.examples = "\n\n".join(
            f"Q: {e['question']}\nSQL: {e['sql']}"
            for e in map(json.loads, filter(None, lines))
        )

    def _system(self):
        return self.template.format(
            dialect=settings.dialect,
            schema=self.schema_text,
            examples=self.examples,
        )

    def ask(self, question, retries=2):
        system = self._system()
        prompt, last_error = question, None
        for attempt in range(1, retries + 2):
            text = clean_sql(self.llm.generate(system, prompt))

            try:
                sql = validate(text, self.tables, settings.dialect, settings.max_rows)
                columns, rows = run(
                    sql, settings.db_path, settings.max_rows, settings.timeout_s
                )
                return {
                    "sql": sql,
                    "attempts": attempt,
                    "columns": columns,
                    "rows": rows,
                }
            except Exception as e:
                last_error = str(e)
                prompt = (
                    f"{question}\n\nYour previous SQL failed.\n"
                    f"SQL: {text}\nError: {last_error}\n"
                    "Return one corrected SELECT query only."
                )
        return {"error": last_error, "attempts": retries + 1}

# ask-sqlite

> Ask questions about your SQLite database in plain English and get answers as validated SQL and formatted tables.

[![Python Version](https://img.shields.io/badge/python-3.10%2B-blue.svg)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Code style: ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)
[![Powered by Ollama](https://img.shields.io/badge/LLM-Ollama-black?logo=ollama)](https://ollama.ai)

---

## Overview

**ask-sqlite** is a local-first, privacy-focused text-to-SQL CLI tool that bridges natural language questions and SQLite databases. Powered by local LLMs through **Ollama** (defaulting to `qwen2.5-coder:3b`), it allows you to query your database conversationally without writing a single line of SQL.

Unlike standard text-to-SQL tools that blindly execute LLM output, **ask-sqlite** features an **AST-based SQL guard**, **strict read-only database enforcement**, and an **automatic self-healing retry loop** that corrects failed queries on the fly.

---

## Features

- **100% Local and Private**: Runs entirely on your machine using Ollama. No third-party API keys, paid subscriptions, or remote data leakage.
- **Multi-Layered Security Guard**:
  - **AST-level SQL Parsing** (via `sqlglot`): Strictly permits `SELECT` and `UNION` queries. Blocks destructive statements like `DROP`, `DELETE`, `UPDATE`, `INSERT`, `ALTER`, or `PRAGMA`.
  - **Table Whitelist Verification**: Validates queries against your database schema and Common Table Expressions (CTEs) to block unauthorized table access.
  - **Auto-Limit Injection**: Automatically appends a configurable `LIMIT` clause if omitted to protect against large memory allocations.
  - **Read-Only SQLite Engine**: Connects via SQLite URI read-only mode (`?mode=ro`) and locks the session with `PRAGMA query_only = ON`.
- **Self-Healing Error Correction**: If a query fails syntax validation or database execution, `ask-sqlite` captures the exact error and prompts the LLM to self-correct (up to 2 retries).
- **Thinking Tag and Markdown Sanitization**: Automatically strips model chain-of-thought blocks (`<think>...</think>`) and markdown fences for full compatibility with reasoning models (DeepSeek-R1, Qwen 2.5 Coder, etc.).
- **Interactive Terminal Interface**: Built with `typer` and `rich`, featuring SQL syntax highlighting, live status spinners, auto-aligned table columns, and formatted execution statistics.
- **Dynamic Schema Introspection**: Reads tables, columns, primary keys, and foreign keys directly from SQLite system pragmas on startup.
- **Configurable Environment**: Fully customizable via `.env` and `pydantic-settings` (model, temperature, timeout limits, max rows, DB path).

---

## Architecture and Pipeline

```text
┌─────────────────────────────────────────────────────────────────────┐
│                        Natural Language Query                       │                                  
│                                                                     |
└──────────────────────────────────┬──────────────────────────────────┘
                                   │
                                   ▼
┌─────────────────────────────────────────────────────────────────────┐
│                    Interactive CLI (Typer / Rich)                   │
└──────────────────────────────────┬──────────────────────────────────┘
                                   │
                                   ▼
┌─────────────────────────────────────────────────────────────────────┐
│                        Pipeline Orchestrator                        │
│  • Introspects SQLite schema (tables, columns, primary/foreign keys)│
│  • Assembles prompt with few-shot examples and schema context       │
└──────────────────────────────────┬──────────────────────────────────┘
                                   │
                                   ▼
┌─────────────────────────────────────────────────────────────────────┐
│                         Local LLM (Ollama)                          │
│                Model: qwen2.5-coder:3b (temp = 0.0)                 │
└──────────────────────────────────┬──────────────────────────────────┘
                                   │ Raw output
                                   ▼
┌─────────────────────────────────────────────────────────────────────┐
│                          Output Sanitizer                           │
│  • Strips <think>...</think> reasoning blocks                       │
│  • Removes ```sql markdown code fences                              │
└──────────────────────────────────┬──────────────────────────────────┘
                                   │ Clean SQL
                                   ▼
┌─────────────────────────────────────────────────────────────────────┐
│                          SQLGlot AST Guard                          │
│  • Syntactic verification via AST parsing                           │
│  • Enforces read-only statements (SELECT / UNION only)              │
│  • Verifies table access whitelist against schema & CTEs            │
│  • Injects automatic LIMIT clause if omitted                        │
└──────────────┬──────────────────────────────────────┬───────────────┘
               │                                      │
       Invalid / Blocked                       Valid Read-Only
               │                                      │
               ▼                                      ▼
┌──────────────────────────────┐      ┌────────────────────────────────┐
│      Self-Healing Retry      │      │  Safe SQLite Execution Engine  │
│                              │      │                                │
│  Captures error & sends it   │      │  • URI read-only (?mode=ro)    │
│  back to LLM for correction  │      │  • PRAGMA query_only = ON      │
│  (Up to 2 automatic retries) │      │  • Query timeout guard (15s)   │
│                              │      │  • Max rows enforcement (100)  │
└──────────────┬───────────────┘      └───────────────┬────────────────┘
               │                                      │
               │ (retry query)                        ├── (Runtime Error) ──┐
               ▼                                      │                     │
      [ Re-prompt LLM ] ◄─────────────────────────────┴─────────────────────┘
                                                      │
                                                      │ (Query Success)
                                                      ▼
                                      ┌────────────────────────────────┐
                                      │     Rich Terminal Display      │
                                      │                                │
                                      │  • ANSI syntax-highlighted SQL │
                                      │  • Auto-aligned data table     │
                                      │  • Row count summary           │
                                      └────────────────────────────────┘
```

---

## Quickstart

### 1. Prerequisites

- **Python 3.10+**
- **[Ollama](https://ollama.ai/)** installed and running.
- Pull your preferred code generation model (default is `qwen2.5-coder:3b`):

```bash
ollama pull qwen2.5-coder:3b
```

### 2. Installation

Clone this repository and navigate into the project directory:

```bash
git clone https://github.com/Human-Gechi/txt_sql.git
cd txt_sql
```

Create and activate a virtual environment:

```bash
# Linux / macOS
python3 -m venv venv
source venv/bin/activate

# Windows (PowerShell)
python -m venv venv
.\venv\Scripts\Activate.ps1
```

Install the package:

```bash
pip install -e .
```

For development and testing tools:

```bash
pip install -e ".[dev]"
```

### 3. Initialize the Sample Database (Optional)

A sample SQLite database containing `customers`, `orders`, and `students` tables is provided in `examples/sample.db`. You can re-initialize it at any time using:

```bash
python txt_sql/init_db.py
```

### 4. Configure Environment

Copy the example configuration file:

```bash
cp .env.example .env
```

### 5. Run the CLI

Start the interactive terminal session:

```bash
ask-sqlite
```

---

## Using Your Own SQLite Database

You can easily replace the sample database with your own SQLite database file:

### Option 1: Configure in `.env` (Recommended)

Open `.env` and set `DATABASE_URL` to point to your SQLite file:

```env
# Relative path from project root
DATABASE_URL=sqlite:///./path/to/your/database.db

# Absolute path on Linux / macOS
DATABASE_URL=sqlite:////home/username/data/production.db

# Absolute path on Windows
DATABASE_URL=sqlite:///C:/Users/username/data/production.db
```

### Option 2: Pass as Environment Variable

Set the environment variable in your terminal session before launching:

```bash
# Linux / macOS
export DATABASE_URL="sqlite:////absolute/path/to/database.db"
ask-sqlite

# Windows (PowerShell)
$env:DATABASE_URL="sqlite:///C:/absolute/path/to/database.db"
ask-sqlite
```

### Automatic Schema Discovery

When you connect your own database, you **do not** need to provide schemas, migrations, or DDL files:

- `ask-sqlite` inspects your database's `sqlite_schema`, `PRAGMA table_info`, and `PRAGMA foreign_key_list` upon startup.
- All table names, column types, primary keys, and foreign key relationships are dynamically detected and injected into the LLM context.
- The SQL guard automatically creates an allowlist from your database tables to block any hallucinated or unauthorized table names.

---

## CLI Usage Example
<img width="933" height="452" alt="image" src="https://github.com/user-attachments/assets/be80f88b-8039-46ad-a3f1-d17026f60310" />

Type `exit`, `quit`, or `q` (or press `Ctrl+C`) to exit.

---

## Configuration Reference

All settings can be configured via environment variables or inside your `.env` file:

| Variable | Type | Default | Description |
| :--- | :--- | :--- | :--- |
| `DATABASE_URL` | `str` | `sqlite:///./examples/sample.db` | URI/Path to the target SQLite database. |
| `OLLAMA_BASE_URL` | `str` | `http://localhost:11434` | URL where your local Ollama server is running. |
| `OLLAMA_MODEL` | `str` | `qwen2.5-coder:3b` | The model used for generating SQL queries. |
| `LLM_TEMPERATURE` | `float` | `0.0` | Sampling temperature (`0.0` ensures deterministic SQL output). |
| `SQL_QUERY_TIMEOUT_SECONDS` | `int` | `15` | Maximum execution time in seconds before query cancellation. |
| `SQL_MAX_ROWS_RETURNED` | `int` | `100` | Safety limit on rows fetched and rendered. |
| `DIALECT` | `str` | `sqlite` | SQL dialect for parsing and syntax generation (powered by `sqlglot`). |

---

## Security and Guardrails

Running LLM-generated SQL queries against local databases requires strict protection. `ask-sqlite` implements multi-layer defense:

1. **Read-Only SQLite Connection**:
   Connections are opened in read-only mode using URI parameters (`?mode=ro`), preventing file write access at the SQLite C-library layer.
2. **SQLite Query-Only Pragma**:
   `conn.execute("PRAGMA query_only = ON")` is executed on connection setup to prevent side effects.
3. **AST Inspection**:
   Using `sqlglot`, the generated query is parsed into an Abstract Syntax Tree (AST). If the root operation is not `SELECT` or `UNION` (e.g., `DROP`, `DELETE`, `ALTER`, `ATTACH`), execution is rejected with a `TypeError`.
4. **Table Whitelist Enforcement**:
   Every table referenced in the query must match an authorized table discovered in the database schema or a local Common Table Expression (CTE).
5. **Enforced Result Limits**:
   If the LLM omits a `LIMIT` clause, the AST is automatically modified to add `LIMIT <SQL_MAX_ROWS_RETURNED>` before execution.

---

## Project Structure

```text
txt_sql/
├── .github/
│   └── workflows/
│       └── ci.yml             # GitHub Actions CI workflow (Ruff & Pytest)
├── examples/
│   ├── init.sql               # Schema and seed data for sample database
│   └── sample.db              # Pre-seeded SQLite sample database
├── tests/
│   └── test_validate.py       # Unit tests for the SQL guardrail and parser
├── txt_sql/
│   ├── execute/
│   │   └── runner.py          # Read-only SQLite execution engine
│   ├── llm/
│   │   ├── base.py            # Abstract LLM client interface
│   │   └── ollama.py          # Ollama client implementation
│   ├── prompts/
│   │   ├── examples.jsonl     # Few-shot prompt pairs (Q -> SQL)
│   │   └── system.txt         # System instruction prompt template
│   ├── schema/
│   │   ├── extract.py         # Introspects tables, columns, and foreign keys
│   │   └── format.py          # Formats schema metadata for prompt injection
│   ├── validate/
│   │   └── sql_guard.py       # AST validation, cleaning, & auto-limiting
│   ├── cli.py                 # Interactive Typer + Rich REPL terminal interface
│   ├── config.py              # Pydantic Settings and environment configuration
│   ├── init_db.py             # Database creation script for examples/sample.db
│   └── pipeline.py            # End-to-end orchestration and self-correction loop
├── .env.example               # Example configuration file
├── pyproject.toml             # Project metadata, dependencies, and entrypoints
├── LICENSE                    # MIT License
└── README.md                  # Project documentation
```

---

## Testing and Code Quality

To run the test suite and verify linting:

```bash
# Run unit tests
pytest -v

# Run code style and lint checks with Ruff
ruff check txt_sql/
ruff format --check txt_sql/
```

---

## Contributing

1. Fork the repository.
2. Create a feature branch: `git checkout -b feature/your-feature-name`.
3. Commit your changes: `git commit -m "Add feature"`.
4. Ensure tests pass and code style is clean:
   ```bash
   ruff check txt_sql/
   ruff format txt_sql/
   pytest
   ```
5. Push to the branch: `git push origin feature/your-feature-name`.
6. Open a Pull Request.

---

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

Maintained by [Human-Gechi](https://github.com/Human-Gechi).

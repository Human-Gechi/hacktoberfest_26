import typer
from rich.console import Console
from rich.syntax import Syntax
from rich.table import Table

from txt_sql.pipeline import Pipeline

app = typer.Typer()
console = Console()


def render_result(result: dict) -> None:
    console.print(Syntax(result["sql"], "sql", theme="ansi_dark", word_wrap=True))

    columns = result["columns"]
    rows = result["rows"]

    if not rows:
        console.print("[yellow]No rows returned.[/yellow]")
        return

    table = Table(show_lines=False, header_style="bold cyan")

    for i, col in enumerate(columns):
        is_numeric = isinstance(rows[0][i], (int, float))
        table.add_column(
            str(col),
            justify="right" if is_numeric else "left",
            style="magenta" if is_numeric else "green",
        )

    for row in rows:
        table.add_row(*["NULL" if cell is None else str(cell) for cell in row])

    console.print(table)
    console.print(f"[dim]{len(rows)} row(s)[/dim]")


@app.command()
def main():
    typer.secho("Welcome to ask-sqlite CLI", fg=typer.colors.GREEN)
    typer.secho(
        "Ask any SQL-related question and get instant answers!",
        fg=typer.colors.BRIGHT_BLUE,
    )
    typer.echo("")

    pipeline = Pipeline()

    while True:
        try:
            query = typer.prompt("You", prompt_suffix="> ", show_default=False).strip()

            if not query:
                continue

            if query.lower() in ["exit", "quit", "q"]:
                typer.secho("Goodbye!", fg="cyan")
                break

            with console.status("[bold green]Thinking...[/bold green]"):
                result = pipeline.ask(query)

            render_result(result)

        except (KeyboardInterrupt, typer.Abort):
            typer.secho("\nGoodbye!", fg="cyan")
            break
        except Exception as e:
            typer.secho(f"Error: {e}", fg="red")
            


if __name__ == "__main__":
    app()

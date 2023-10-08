import typer
import analysis as az
import sys

app = typer.Typer()


@app.command()
def scan_directory(directory: str, only_critical: bool = False):
    if only_critical:
        az.ONLY_CRITICAL = True
    az.analyze_path(directory)
    if only_critical and az.errors_found:
        sys.exit(1)


if __name__ == "__main__":
    app()

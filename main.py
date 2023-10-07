import typer
import analyzer as az

app = typer.Typer()

@app.command()
def scan(directory: str):
    az.analyze(directory)

if __name__ == "__main__":
    app()
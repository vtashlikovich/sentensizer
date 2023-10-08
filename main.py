import typer
import analysis as az
import sys

app = typer.Typer()

# TODO: adde exception handler


@app.command()
def scan_directory(directory: str, only_critical: bool = False):
    if only_critical:
        az.ONLY_CRITICAL = True
    az.analyze_path(directory)
    if only_critical and az.errors_found:
        print(f'Found {az.critical_files} critical files.')
        sys.exit(1)
    else:
        print(f'Analyzed {az.files_analyzed_num} files.\n'
              f'Found {az.total_sentences_num} sentences.\n'
              f'Critical {az.critical_files} files.\n')


if __name__ == "__main__":
    app()
